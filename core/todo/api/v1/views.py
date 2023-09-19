from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .serializers import PostSerializer, CategorySerializer
from ...models import Post, Category
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import GenericAPIView, ListCreateAPIView, ListAPIView, RetrieveAPIView , RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .filters import PostFilters
from .paginations import DefaultPagination


class PostModelViewset(viewsets.ModelViewSet):
    """A Simple Viewset for listing or retrieving users"""
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'status', 'author']
    search_fields = ['title', 'content']
    ordering_fields = ['published_date']
    filterset_class = PostFilters
    pagination_class = DefaultPagination


class CategoryModelViewset(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
        
