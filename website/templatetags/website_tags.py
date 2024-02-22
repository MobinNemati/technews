from django import template
from news.models import Post, Category
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone


register = template.Library()

@register.inclusion_tag('website/latestposts.html')
def latestposts(request):
    now1=timezone.now()
    posts = Post.objects.filter(published_date__lt=now1, status=1).order_by('-created_date')[:6]
    return {'posts': posts}