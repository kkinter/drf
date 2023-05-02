from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from core.abstract.viewsets import AbstractViewSet
from core.post.models import Post
from core.post.serializers import PostSerializer
from core.auth.permissions import UserPermission

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema_view
from drf_spectacular.utils import extend_schema


class PostViewSet(AbstractViewSet):
    http_method_names = ('post', 'get', 'put', 'delete')
    permission_classes = (UserPermission, )
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    def get_object(self):
        obj = Post.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        request=PostSerializer,
        responses={200: PostSerializer},
        parameters=[
            OpenApiParameter(
                name='pk',
                description='Public ID of the post being liked',
                type=OpenApiTypes.STR
            )
        ],
        examples=[
            OpenApiExample(
                'Successful Like',
                summary='Successful like of a post',
                value={
                    'id': '1',
                    'title': 'My Post',
                    'content': 'This is my post',
                    'likes': 1
                }
            )
        ],
        description='Like a post with the specified public ID'
    )
    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user
        user.like(post)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=None,
        responses={200: PostSerializer},
        parameters=[
            OpenApiParameter(
                name='pk',
                description='Public ID of the post to remove like from',
                type=OpenApiTypes.STR
            )
        ],
        examples=[
            OpenApiExample(
                'Successful Remove Like',
                summary='Successful removal of like from a post',
                value={
                    'id': '1',
                    'title': 'My Post',
                    'content': 'This is my post',
                    'likes': 0
                }
            )
        ],
        description='Remove a like from the post with the specified public ID'
    )
    @action(methods=['post'], detail=True)
    def remove_like(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user
        user.remove_like(post)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
