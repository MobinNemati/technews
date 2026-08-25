"""Class-based views of the news app."""

from django.contrib import messages
from django.db.models import Count, F, Prefetch, Q
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin

from news.forms import CommentForm
from news.models import Comment, Post


class PublishedPostMixin:
    """Single definition of "which posts are visible to a visitor"."""

    model = Post

    def get_published_posts(self):
        """Return the plain queryset of posts that are online right now."""
        return Post.objects.filter(
            status=True,
            published_date__lt=timezone.now(),
        )


class PostListView(PublishedPostMixin, ListView):
    """News feed, optionally narrowed down by category, tag or author."""

    template_name = 'news/home.html'
    paginate_by = 3

    #: URL keyword -> ORM lookup. Only keywords present in the URL apply.
    filter_lookups = {
        'cat_name': 'category__name',
        'tag_name': 'tags__name',
        'author_username': 'author__username',
    }
    #: Lookups spanning a many-to-many relation, which can duplicate rows.
    multivalued_lookups = frozenset({'category__name', 'tags__name'})

    def get_queryset(self):
        """Build the feed in a fixed number of queries.

        ``home.html`` renders the author, the categories and the number of
        approved comments of every post, so all three are resolved up front
        instead of once per row.
        """
        queryset = (
            self.get_published_posts()
            .select_related('author')
            .prefetch_related('category')
            .annotate(
                comments_count=Count(
                    'comment',
                    filter=Q(comment__approved=True),
                    distinct=True,
                ),
            )
            # Grouped queries ignore Meta.ordering, so repeat it here: the
            # paginator needs a deterministic order, and ``id`` breaks ties.
            .order_by(*Post._meta.ordering, 'id')
        )
        filters = {
            lookup: self.kwargs[keyword]
            for keyword, lookup in self.filter_lookups.items()
            if self.kwargs.get(keyword)
        }
        queryset = queryset.filter(**filters)
        if filters.keys() & self.multivalued_lookups:
            queryset = queryset.distinct()
        return queryset

    def paginate_queryset(self, queryset, page_size):
        """Serve a valid page instead of a 404 for a bogus ``?page=``."""
        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        page_number = self.kwargs.get(self.page_kwarg) or self.request.GET.get(
            self.page_kwarg
        )
        page = paginator.get_page(page_number)
        return paginator, page, page.object_list, page.has_other_pages()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # The template iterates ``posts`` *and* reads pagination attributes
        # off it, so it has to be the page object while pagination is on.
        # An empty page is falsy, hence the explicit ``is None``.
        page = context.get('page_obj')
        context['posts'] = context['object_list'] if page is None else page
        return context


class PostSearchView(PostListView):
    """The same feed, narrowed down by the ``?s=`` search term."""

    #: The search page has always listed every match on a single page.
    paginate_by = None
    search_param = 's'

    def get_queryset(self):
        queryset = super().get_queryset()
        term = self.request.GET.get(self.search_param, '').strip()
        if term:
            queryset = queryset.filter(content__icontains=term)
        return queryset


class PostDetailView(PublishedPostMixin, FormMixin, DetailView):
    """A single news item together with its comments and comment form."""

    template_name = 'news/single.html'
    context_object_name = 'posts'
    pk_url_kwarg = 'pid'
    form_class = CommentForm

    def get_queryset(self):
        """Fetch the post, its author, categories, tags and comments."""
        return (
            self.get_published_posts()
            .select_related('author')
            .prefetch_related(
                'category',
                'tags',
                Prefetch(
                    'comment_set',
                    queryset=Comment.objects.filter(approved=True),
                    to_attr='approved_comments',
                ),
            )
        )

    def get_object(self, queryset=None):
        """Return the post and count the visit with one atomic UPDATE."""
        post = super().get_object(queryset)
        if self.request.method == 'GET':
            Post.objects.filter(pk=post.pk).update(
                counted_view=F('counted_view') + 1,
            )
            # Mirror the new value so the template shows this visit too.
            post.counted_view += 1
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Deliberately not self.get_queryset(): the neighbours only need an
        # id, a title and an image, not the prefetched relations.
        published_posts = self.get_published_posts()
        context.update(
            comments=self.object.approved_comments,
            next_post=published_posts.filter(
                id__gt=self.object.id,
            ).order_by('id').first(),
            prev_post=published_posts.filter(
                id__lt=self.object.id,
            ).order_by('-id').first(),
        )
        return context

    def post(self, request, *args, **kwargs):
        """Take a new comment, then redirect back to the post."""
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        # The post is taken from the URL, never from the submitted payload.
        comment.post = self.object
        comment.save()
        messages.success(self.request, 'Your comment was submitted '
                                       'successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Your comment could not be submitted.')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return self.object.get_absolute_url()
