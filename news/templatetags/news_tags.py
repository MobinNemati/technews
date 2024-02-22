from django import template
from news.models import Post, Category, Comment

register = template.Library()


@register.inclusion_tag('news/news-category.html')
def categories():
    posts = Post.objects.filter(status=1)
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name]=posts.filter(category=name).count()
    return {'categories':cat_dict}

@register.inclusion_tag('news/news-latestposts.html')
def latestposts():
    posts = Post.objects.filter(status=1).order_by('-published_date')[0:3]
    return {'posts':posts}

@register.inclusion_tag('news/news-popular.html')
def popularposts():
    posts = Post.objects.filter(status=1).order_by('-counted_view')[0:3]
    return {'posts':posts}

@register.simple_tag(name='comments_count')
def function(pid):
    return Comment.objects.filter(post=pid, approved=True).count()