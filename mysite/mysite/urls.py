"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.dom.minidom import Document
from django.urls import path, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSiteMap
from magazine.sitemaps import IssueSiteMap
from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
    'posts' : PostSiteMap,
    'issues': IssueSiteMap,
}



urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('blog.urls', namespace='blog')),
    path('magazine/', include('magazine.urls', namespace='magazine')),
    path('', include('editors.urls', namespace='editors')),
    #path('dashboard/', include(("editors.urls", 'editors'), namespace="editors")),
    path('', include('account.urls')),
    path('device-info/', include('devices.urls')),
    path('search/', include('search.urls')),
    path('sitemap.xml', sitemap, {'sitemaps' : sitemaps},
         name = 'django.contrib.sitemaps.views.sitemap'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)