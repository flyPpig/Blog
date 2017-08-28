# coding: UTF-8

"""Blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from blog.feeds import AllPostRssFeed
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(
        url='/static/images/favicon.ico', permanent=True)),

    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('users.urls')),
    # 将auth 应用中的urls 模块包含进来
    url(r'^users/', include('django.contrib.auth.urls')),

    url(r'', include('blog.urls')),
    url(r'', include('comments.urls')),

    url(r'^all/rss/$', AllPostRssFeed(), name='rss'),
]
