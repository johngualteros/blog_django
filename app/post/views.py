"""
Views for recipe app
"""
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiExample, OpenApiTypes
from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Post, Comment

from post import serializers


@extend_schema_view(
    list=extend_schema(
        description='List all posts',
    ),
)
class PostViewSet(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = serializers.PostDetailSerializer
    queryset = Post.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        queryset = self.queryset
        return queryset.filter(user=self.request.user).order_by('-id').distinct()

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'list':
            return serializers.PostSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)


class BasePostAttrViewSet(mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base view set for user owned recipe attributes"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        assigned_only = bool(int(self.request.query_params.get('assigned_only', 0)))
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(post__isnull=False)
        return queryset.filter(user=self.request.user).order_by('-title').distinct()


class CommentViewSet(BasePostAttrViewSet):
    """Manage comments in the database"""
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()
