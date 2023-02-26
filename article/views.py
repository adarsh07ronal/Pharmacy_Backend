from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser

from article.models import Article
from article.serializers import ArticleSerializer
from rest_framework import viewsets, filters
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend

class ArticleViewSet(viewsets.ModelViewSet):
	queryset = Article.objects.all()
	serializer_class = ArticleSerializer
	parser_classes = (MultiPartParser,)
	filter_backends = (DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
	ordering_fields=("created_at","updated_at","title","article")
	search_fields=['title','description']
