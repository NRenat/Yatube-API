from rest_framework import viewsets, filters, pagination, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly, \
    IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from posts.models import Post, Group, Comment, Follow
from . import serializers, permissions


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.AuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.AuthorOrReadOnly,)

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_id'])

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        author = self.request.user
        serializer.save(post_id=post_id, author=author)


class CreateListViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass


class FollowViewSet(CreateListViewSet):
    serializer_class = serializers.FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            following_user = serializer.validated_data['following']
            serializer.save(user=self.request.user, following=following_user)
