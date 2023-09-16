from django.urls import path, include
from rest_framework import routers

from .views import PostViewSet, GroupsViewSet, CommentViewSet, FollowViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'posts', PostViewSet)
router_v1.register(r'groups', GroupsViewSet)
router_v1.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                   basename='comment')

urlpatterns = [
    path('v1/follow/',
         FollowViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='follow'),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/', include(router_v1.urls))
]
