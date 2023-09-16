from rest_framework import serializers, validators

from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault(),
        source='author.username')

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault(),
        source='author.username')
    post = serializers.PrimaryKeyRelatedField(
        read_only=True, required=False)

    class Meta:
        model = Comment
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        exclude = ('id',)

        class Meta:
            validators = [
                validators.UniqueTogetherValidator(
                    queryset=Follow.objects.all(),
                    fields=('user', 'following'))
            ]

    def validate_following(self, following):
        user = self.context['request'].user
        if user == following:
            raise serializers.ValidationError("You can't follow yourself")
        return following
