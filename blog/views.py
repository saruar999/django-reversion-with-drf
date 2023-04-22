from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, ListModelMixin
from blog.models import Blog
from blog.serializers import BlogSerializer
from blog.revision.views import CustomRevisionMixin


class BlogViewSet(CustomRevisionMixin, UpdateModelMixin, RetrieveModelMixin, ListModelMixin, CreateModelMixin, GenericViewSet):

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
