# -*- coding:utf-8 -*-

import markdown
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from comments.forms import CommentForm
# 首页视图函数:涉及到数据库
from .models import Post, Category

from django.views.generic import ListView, DetailView
from django.db.models.aggregates import Count

from myblog.models import Tag

#: 美化标题的锚点

from django.utils.text import slugify
from markdown.extensions.toc import TocExtension

#: 全文搜索
from django.db.models import Q

#: js与Django交互

import json



#: Count 计算分类下的文章数， 其接受的参数为需要计算的模型的名称
tag_list = Tag.objects.annotate(num_posts=Count('post'))

#: 查找含有搜索关键词的文章
def  search(request):
	q = request.GET.get('q')
	error_msg = ''

	if not q:
		error_msg = "请输入关键词"
		return render(request, 'myblog/index.html', {'error_msg': error_msg})

	post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
	return render(request, 'blog/index.html', {'error_msg': error_msg,
												'post_list': post_list})



def index(request):
	post_list = Post.objects.all().order_by('-created_time')
	return render(request, 'blog/index.html', context={'post_list': post_list})

#:将 index 视图函数改写为类视图
class IndexView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_oject_name = 'post_list'
	#: 指定 paginate_by 属性后开启分页功能，其值代表每一页包含多少文章
	paginate_by = 10


	#:扩展Pagination
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		paginator = context.get('paginator')
		page = context.get('page_obj')
		is_paginated = context.get('is_paginated')

		#: 调用自己写的pagination_data方法获得显示分页导航条所需额数据
		pagination_data = self.pagination_data(paginator, page, is_paginated)
		#: 将分页导航条的模板变量更新到context中， 注意paginator_data方法返回的也是一个字典
		context.update(pagination_data)
		return context

	def pagination_data(self, paginator, page, is_paginated):
		if not is_paginated:
			return {}

		left = []
		right = []
		left_has_more = False
		right_has_more = False
		first = False
		last = False
		page_number = page.number
		total_pages = paginator.num_pages
		page_range = paginator.page_range

		if page_number == 1:
			 right = page_range[page_number:page_number + 2]
			 if right[-1] < total_pages - 1:
			 	right_has_more =True

			 if right[-1] < total_pages:
			 	last = True

		elif page_number == total_pages:
			left = page_range[(page_number - 3) if (page_numer - 3) > 0 else 0:page_number - 1]
			right = page_range[page_number:page_number + 2]

			if right[-1] < total_pages - 1:
				right_has_more = True
			if right[-1] < total_pages:
				last  = True

			if left[0] > 2:
				left_has_more = True
			if left[0] > 1:
				first = True

		data = {
			'left': left,
			'right': right,
			'left_has_more': left_has_more,
			'right_has_more': right_has_more,
			'first': first,
			'last': last,
		}

		return data

#: 标签视图函数
class TagView(ListView):
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'

	def get_queryset(self):
		tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
		return super(TagView, self).get_queryset().filter(tags=tag)


#:将 category 视图函数改写为类视图
class CategoryView(IndexView):
	"""
	model = post
	template_name = 'blog/index.html'
	context_object_name = 'post_list'
"""
	def get_queryset(self):
		cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
		return super(CategoryView, self).get_queryset().filter(category=cate)
#: 博客详情页视图函数
def detail(request, pk):
	post = get_object_or_404(Post, pk=pk)
	# 记得在顶部引入 markdown 模块
	post.body = markdown.markdown(post.body,
		                          extensions=[
		                              'markdown.extensions.extra',
		                              'markdown.extensions.codehilite',
		                              'markdown.extensions.toc',
		                          ])
	form = CommentForm()
	comment_list = post.comment_set.all()

	context = {'post': post,
	           'form': form,
	           'comment_list': comment_list
}
    #:return render(request, 'blog/detail.html', context=context)
	return render(request, 'blog/detail.html', context=context)
#： Detail类视图
#: 将detail 视图函数转换为等价的类视图 PostDetailView
class PostDetailView(DetailView):
	#: 这些属性的含义同ListView
	model = Post
	template_name = 'blog/detail.html'

	context_object_name = 'post'
    #: 覆写 get 方法
	def get(self, request, *args, **kwargs):
		response = super(PostDetailView, self).get(request, *args, **kwargs)

		#: 将文章阅读量 +1
		#: 注意 self.object 的值就是被访问的文章post
		self.object.increase_views()
		# 视图必须返回一个 HttpResponse 对象
		return response

	def get_object(self, queryset=None):
		#: get_obkect方法——需要对post的body值进行渲染
		# 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
		post = super(PostDetailView, self).get_object(queryset=None)
		md = markdown.Markdown(extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
			#'markdown.extensions.toc',
			TocExtension(slugify=slugify),
		])
		post.body = md.convert(post.body)
		post.toc = md.toc
		return post

	def get_context_data(self, **kwargs):
		context = super(PostDetailView, self).get_context_data(**kwargs)
		form  = CommentForm()
		comment_list = self.object.comment_set.all()
		context.update({
			'form': form,
			'comment_list': comment_list
			})
		return context

def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})
#: 文章归档
def  archives(request, year, month):
	 post_list = Post.objects.filter(created_time__year=year,
	 	                             created_time__month=month,
	 	                            ).order_by('-created_time')
	 return render(request, 'blog/index.html', context={'post_list': post_list})

return HttpResponse("欢迎访问我的博客首页!")
"""
#: js与Django交互
def home(request):
	List = ['自强学堂', '渲染Json到模板']
	Dict = {'site': '自强学堂', 'author': '李俊'}
	return render(request, 'blog/index.html', {
		'List': json.dumps(List),
		'Dict': json.dumps(Dict)

		})