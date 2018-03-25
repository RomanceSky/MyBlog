#: -*- coding: utf-8 -*-
from django.db import models
from django.utils.html import strip_tags
#: 
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
import markdown

#: Create your models here.
#: ：需要 3 个表格：文章（Post）、分类（Category）以及标签（Tag）
#: 创建分类数据表
class Category(models.Model):
	name = models.CharField(max_length=100)
""":
	Category 就是一个标准的 Python 类，
	它继承了 models.Model 类，类名为 Category 。
	Category 类有一个属性 name，它是 models.CharField 的一个实例。
	：
"""

class Tag(models.Model):
	"""
	标签Tag 也比较简单， 和Category 一样
	再次强调一定要继承 models.Model 类!
	"""
	name = models.CharField(max_length=100)

@python_2_unicode_compatible
class Post(models.Model):
	"""
	文章的数据库稍微复杂一点， 主要是涉及的字段更多。
	"""
	#: 自定义get_absoulte_url方法
	#: 记得从django.urls中导入reverse函数
	def get_absolute_url(self):
		return reverse('myblog:detail', kwargs={'pk': self.pk})

	Tags = models.ManyToManyField('Tag')
	#: 文章标题
	title = models.CharField(max_length=70)
	#: 文章正文
	body = models.TextField()

	#: 文章摘要
	excerpt = models.CharField(max_length=200, blank=True)

	#: 文章的创建时间和最后一次修改时间
	created_time = models.DateTimeField()
	modified_time = models.DateTimeField()

	#: 文章摘要，指定CharField的blank=True 参数值后可以允许空值
	excerpt = models.CharField(max_length=200, blank=True)
	#:把文章对应的数据库表和分类、标签对应的数据库表关联了起来
	category = models.ForeignKey('Category',  on_delete=models.CASCADE)
	#:category = models.ForeignKey(Category, on_delete=models.CASCADE)
	#:tags = models.ManyToManyField(Tag, blank=True)

	#: 文章作者
	#: 这里User 是从django.contrib.auth.models导入的
	#: 通过ForeignKey把文章和User关联起来
	#: 这里我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	#:新增字段——阅读量
	views = models.PositiveIntegerField(default=0)
	#Tags = models.ManyToManyField('Tag')


#: 这里的方法是先将md文本渲染成html，用md.convert方法渲染，
#: 然后再取前54个给excerpt，最后保存到数据库中
	#: 复写save()方法
	def save(self, *args, **kwargs):
		#: 如果没有填写摘要
		if not self.excerpt:
			#: 首先实例化一个Markdown类， 用于渲染 body 的文本
			md = markdown.Markdown(extensions=[
				'markdown.extensions.extra',
				'markdown.extensions.codehilite,'
				])
			#: 先将 Markdown 文本渲染成HTML 文本
			#: strip_tags 去掉HTML 文本的全部  HTML标签
			#: 从文本摘取前54 个字符赋给excerpt
			self.excerpt = strip_tags(md.convert(self.body))[:54]
		#: 调用父类的 save()方法将数据保存到数据库中
		super(Post, self).save(*args, **kwargs)

	#: 增加阅读量的模型方法
	def increase_views(self):
		self.views += 1
		self.save(update_fields=['views'])
	class Meta:
		ordering = ['-created_time']

#class Tag(models.Model):
	#name = models.CharField(max_length=100)

	





















