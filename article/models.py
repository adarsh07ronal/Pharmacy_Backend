from __future__ import unicode_literals
from django.db import models

# Create your models here.

# Both the models are not functional anywhere

class Category(models.Model):
	parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=20)
	slug = models.CharField(max_length=50,null=True, blank=True, unique=True)
	description = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Article(models.Model):
	article = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='article', null=True, blank=True)
	title = models.CharField(max_length=20)
	description = models.TextField(null=True, blank=True)
	image = models.ImageField(upload_to='article')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title


