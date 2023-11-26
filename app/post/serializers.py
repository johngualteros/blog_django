from rest_framework import serializers
from core.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment objects"""

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id',)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post objects"""
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'title', 'created_at', 'updated_at', 'comments')
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create a new post"""
        post = Post.objects.create(**validated_data)
        auth_user = self.context['request'].user
        return post

    def update(self, instance, validated_data):
        """Update a post"""
        comments = validated_data.pop('comments')
        post = super().update(instance, validated_data)
        post.comments.clear()
        user = self.context['request'].user
        for comment in comments:
            comment_object, created = Comment.objects.get_or_create(
                user=user,
                content=comment['content']
            )
            post.comments.add(comment_object)
        return post


class PostDetailSerializer(PostSerializer):
    """Serializer for post detail"""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')
