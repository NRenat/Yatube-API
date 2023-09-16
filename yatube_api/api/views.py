from rest_framework import viewsets, filters, pagination, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

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


class CreateListViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FollowSerializer
    permission_classes = (permissions.FollowPermission,)
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search_param = request.query_params.get('search')
        if search_param:
            queryset = queryset.filter(following__username=search_param)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if serializer.is_valid():
            following_user = serializer.validated_data['following']
            serializer.save(user=self.request.user, following=following_user)
