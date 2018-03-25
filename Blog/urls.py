"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
#from django.urls import path
#
from django.conf.urls import url, include
from myblog.feeds import  AllPostsRssFeed
urlpatterns = [
    #path('admin/', admin.site.urls),
    url('admin/', admin.site.urls),
    url(r'', include('myblog.urls')),
    url(r'', include('comments.urls')),
    #: 记得在顶部引入AllPostsRssFeed
    url(r'^all/rss/$', AllPostsRssFeed(), name='rss'),
    #: 全文搜索
    url(r'^search/', include('haystack.urls')),
]
