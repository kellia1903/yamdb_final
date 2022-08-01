from django.db.models import Avg
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.pagination import (
    LimitOffsetPagination, PageNumberPagination
)
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import (
    Category, Genre, Review, Title, User, CONFIRMATION_CODE_LENGTH
)
from api_yamdb.settings import DEFAULT_FROM_EMAIL
from .filters import TitlesFilter
from .permissions import (
    AdminOnly, AdminOrReadOnly, AuthorOrModeratorOrReadOnly
)
from .serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    GetTitleSerializer, ReviewSerializer, TitleSerializer,
    SignUpSerializer, GetTokenSerializer, UserSerializer
)


@api_view(['POST'])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(
            email=serializer.validated_data.get('email'),
            username=serializer.validated_data.get('username'),
        )
    except IntegrityError:
        return Response(
            'Этот email или username уже занят',
            status=status.HTTP_400_BAD_REQUEST
        )
    user.confirmation_code = get_random_string(length=CONFIRMATION_CODE_LENGTH)
    user.save()
    send_mail(
        subject='Код регистрации',
        message=f'Код подтверждения: {user.confirmation_code}',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email, ],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    if ((user.confirmation_code
            == serializer.validated_data['confirmation_code'])
            and user.confirmation_code):
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token.access_token)}, status=status.HTTP_200_OK)
    user.confirmation_code = ''
    user.save()
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AdminOnly, )
    filter_backends = (filters.SearchFilter, )
    filterset_fields = ('username', )
    search_fields = ('=username', )
    lookup_field = 'username'

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(IsAuthenticated, ), url_path='me')
    def me(self, request):
        user = self.request.user
        if request.method == 'GET':
            return Response(UserSerializer(user).data,
                            status=status.HTTP_200_OK)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly, AuthorOrModeratorOrReadOnly
    )

    def get_object_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_object_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_object_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly, AuthorOrModeratorOrReadOnly
    )

    def get_object_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_object_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review_id=self.get_object_review().id
        )


class CategoryGenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    pagination_class = LimitOffsetPagination
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.prefetch_related('reviews').all().
        annotate(rating=Avg('reviews__score'))
    )
    serializer_class = GetTitleSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitlesFilter
    ordering_fields = ('name', )

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return GetTitleSerializer
        return TitleSerializer
