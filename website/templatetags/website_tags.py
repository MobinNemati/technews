from django import template
from django.utils import timezone

from news.models import Post


register = template.Library()


@register.inclusion_tag('website/latestposts.html')
def latestposts(request):
    """The six newest published posts, authors included to avoid N+1."""
    posts = (
        Post.objects.filter(status=True, published_date__lt=timezone.now())
        .select_related('author')
        .order_by('-created_date')[:6]
    )
    return {'posts': posts}
