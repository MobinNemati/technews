from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm
from django.contrib import messages




def news_view(request, cat_name=None, tag_name=None, author_username=None):
    now = timezone.now()
    posts = Post.objects.filter(status=1, published_date__lt=now)  

    if cat_name:
        posts = posts.filter(category__name=cat_name)
    if tag_name:
        posts = posts.filter(tags__name__in=[tag_name])
    if author_username:
        posts = posts.filter(author__username=author_username)

    posts = Paginator(posts, 3)
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
        
    return render(request, 'news/home.html', {'posts': posts})


def news_single(request, pid):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'your commnet submitted successfully')
        else:
            messages.error(request, 'your commnet didnt submited')

    now = timezone.now()
    posts = get_object_or_404(Post, status=1, published_date__lt=now, id=pid)
    posts.counted_view += 1
    posts.save()

    comments = Comment.objects.filter(post=posts.id, approved=True)

    next_post = Post.objects.filter(published_date__lt=now, status=1, id__gt=pid).order_by('id').first()
    prev_post = Post.objects.filter(published_date__lt=now, status=1, id__lt=pid).order_by('-id').first()

    form = CommentForm()
    context = {'posts':posts, 'next_post':next_post, 'prev_post':prev_post, 'comments':comments, 'form':form}
    return render(request, 'news/single.html', context)


def news_search(request):
    posts = Post.objects.filter(status=1)
    if request.method == 'GET':
        if request.GET.get('s'):
            posts = posts.filter(content__contains=request.GET.get('s'))
    context = {'posts': posts}
    return render(request, 'news/home.html', context)  
