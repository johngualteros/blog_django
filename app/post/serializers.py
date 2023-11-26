from rest_framework import serializers
from core.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment objects"""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'updated_at', 'user', 'post')
        read_only_fields = ('id', 'user')

    def create(self, validated_data):
        """Create a new comment"""
        post_id = validated_data.pop('post')
        auth_user = self.context['request'].user

        comment = Comment.objects.create(user=auth_user, **validated_data)

        post = Post.objects.get(id=post_id, user=auth_user)
        post.comments.add(comment)

        return comment



class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ('id', 'title', 'created_at', 'updated_at', 'comments')
        read_only_fields = ('id',)

    def create(self, validated_data):
        comments_data = validated_data.pop('comments', [])
        post = Post.objects.create(**validated_data)
        auth_user = self.context['request'].user

        post.comments.set(
            Comment.objects.create(user=auth_user, **comment_data)
            for comment_data in comments_data
        )

        return post

    def update(self, instance, validated_data):
        comments_data = validated_data.pop('comments', [])
        post = super().update(instance, validated_data)

        auth_user = self.context['request'].user
        post.comments.clear()
        post.comments.set(
            Comment.objects.create(user=auth_user, **comment_data)
            for comment_data in comments_data
        )

        return post



class PostDetailSerializer(PostSerializer):
    """Serializer for post detail"""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'user', 'created_at', 'updated_at', 'comments')
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')
