from django.contrib.auth.tokens import default_token_generator
from rest_framework import viewsets, generics
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, BasePermission, \
    AllowAny
from rest_framework.views import APIView
from rest_framework import viewsets, filters, mixins
from api.serializers import *
from api.permissions import *
from api.models import *
from rest_framework.response import Response
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, UserPermission]
    lookup_field = "username"

    @action(methods=["GET"], detail=True)
    def get_self_profile(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        serializer = CreateUserSerializer(user)
        return Response(serializer.data)

    @action(methods=["PATCH"], detail=True)
    def update_profile(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        serializer = CreateUserSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class RegisterUsersView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.data.get("email", )
        user, created = User.objects.get_or_create(email=email)
        confirmation_code = default_token_generator.make_token(user)
        #send_mail_to_user(email, confirmation_code)
        return Response({"email": email})


class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


class GenresAPIView(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


class TitlesAPIView(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


class ReviewAPIView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [OnlyCreatorPermission, IsAdminOrReadOnly]
       #IsAuthorOrIsStaffPermission, IsAuthPostPermission, ReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(
            Titles,
            id=self.kwargs.get('title_id')
        )
        return title.review.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Titles,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title
        )

    # def partial_update(self, request, *args, **kwargs):
    #     title = get_object_or_404(
    #         Titles,
    #         id=self.kwargs.get('title_id')
    #     )
    #     get_object_or_404(
    #         Titles.reviews,
    #         pk=self.kwargs.get('pk'),
    #         title=title
    #     )
    #     return super().partial_update(request, *args, **kwargs)


class CommentsAPIView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAuthenticated, ReviewCommentPermission]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title=self.kwargs.get("title__id"), )
        return queryset.comments.all()


