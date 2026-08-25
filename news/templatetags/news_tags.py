from django import template
from django.db.models import Count, Q

from news.models import Category, Comment, Post


register = template.Library()


@register.inclusion_tag('news/news-category.html')
def categories():
    """Map every category to its number of published posts in one query."""
    annotated_categories = Category.objects.annotate(
        published_posts=Count('post', filter=Q(post__status=True),
                              distinct=True),
    )
    return {
        'categories': {
            category: category.published_posts
            for category in annotated_categories
        },
    }


@register.inclusion_tag('news/news-latestposts.html')
def latestposts():
    posts = Post.objects.filter(status=True).order_by('-published_date')[:3]
    return {'posts': posts}


@register.inclusion_tag('news/news-popular.html')
def popularposts():
    posts = Post.objects.filter(status=True).order_by('-counted_view')[:3]
    return {'posts': posts}


@register.simple_tag(name='comments_count')
def comments_count(pid):
    """Count the approved comments of a single post.

    Prefer annotating the queryset in the view when a whole list of posts is
    rendered, otherwise this runs one query per row.
    """
    return Comment.objects.filter(post=pid, approved=True).count()
