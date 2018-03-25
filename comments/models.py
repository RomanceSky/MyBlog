from django.db import models

# Create your models here.
from django.utils.six import python_2_unicode_compatible

#: python_2_unicode_compatible 装饰器用于兼容 Python2
@python_2_unicode_compatible
class Comment(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=255)
	url = models.URLField(blank=True)
	text = models.TextField()
	creted_time = models.DateTimeField(auto_now_add=True)
    #: 设置外键
	post = models.ForeignKey('myblog.Post', on_delete=models.CASCADE)

	def __str__(self):
		return self.text[:20]

