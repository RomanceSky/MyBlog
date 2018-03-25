# -*- coding: utf-8 -*-
from django import template
from ..models import Post, Category, Tag

from django.db.models.aggregates import Count
from myblog.models import Category

register = template.Library()

#: 最新文章模板标签
#: 注册这个函数为模板标签
@register.simple_tag
def get_recent_posts(num=5):
	return Post.objects.all().order_by('-created_time')[:num]

#: 归档模板标签
@register.simple_tag
def archives():
	return Post.objects.dates('created_time', 'month', order='DESC')
@register.simple_tag
def get_categories():
    # 记得在顶部引入 count 函数
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
"""
@register.simple_tag
#: 分类模板标签
#: 自定义了一个模板标签函数 get_categories
def get_categories():
	#: Count 计算分类下的文章数， 其接受的参数为需要计数的模型的名称
	#return Category.objects.all()
	return Category.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)
"""
#: 定义一个get_tags 模板标签
@register.simple_tag
def get_tags():
	return Tag.objects.annotate(num_posts=Count('post')).filter(num_posts__gt=0)