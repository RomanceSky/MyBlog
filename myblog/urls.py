# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

app_name = 'myblog'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    #  <网站域名>/post/2/ ,数据库中 Post 记录的 id 值,依照这个规则来绑定 URL 和视图
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', views.archives, name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tag'),
    #url(r'^search/$', views.search, name='search'),
    

]

