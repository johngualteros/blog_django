from rest_framework import serializers
from core.models import Post


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post objects"""

    class Meta:
        model = Post
        fields = ('id', 'title', 'created_at', 'updated_at')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create a new post"""
        post = Post.objects.create(**validated_data)
        auth_user = self.context['request'].user
        return post

    def update(self, instance, validated_data):
        """Update a post"""
        post = super().update(instance, validated_data)
        user = self.context['request'].user
        return post


class PostDetailSerializer(PostSerializer):
    """Serializer for post detail"""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')
