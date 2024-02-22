
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from website.sitemaps import StaticViewSitemap
from news.sitemaps import NewsSitemap
from django.views.generic import TemplateView




sitemaps = {
    "static": StaticViewSitemap,
    "News": NewsSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('news/', include('news.urls')),
    path('accounts/', include('accounts.urls')),
    path('sitemap.xml/', sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path('robots.txt/', include('robots.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('captcha/', include('captcha.urls')),

    path('custom_404/', TemplateView.as_view(template_name='404.html'), name='custom_404'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)