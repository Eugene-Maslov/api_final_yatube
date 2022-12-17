from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


from posts.models import Comment, Follow, Group, Post, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(),
        slug_field='username', default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(queryset=User.objects.all(),
        slug_field='username')

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны!'
            )
        ]

    #def validate_following(self, value):
    #    if value == self.context['user'].user:
    #        raise serializers.ValidationError('Нельзя подписаться на самого себя!')
    #    return value
