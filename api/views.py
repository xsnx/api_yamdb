from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_list_or_404
from rest_framework import viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, BasePermission, \
    AllowAny, IsAuthenticatedOrReadOnly
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
    #permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated, BasePermission]
    lookup_field = 'username'

    # @action(methods=["GET"], detail=True)
    # def get_self_profile(self, request):
    #     user = get_object_or_404(User, username=self.request.user.username)
    #     serializer = CreateUserSerializer(user)
    #     return Response(serializer.data)
    #
    # @action(methods=["PATCH"], detail=True)
    # def update_profile(self, request):
    #     user = get_object_or_404(User, username=self.request.user.username)
    #     serializer = CreateUserSerializer(
    #         user, data=request.data, partial=True
    #     )
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data)


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = CreateUserSerializer
#     lookup_field = 'username'
#
#     def get_permissions(self):
#         if self.action in ['get', 'patch', 'delete']:
#             permission_classes = [IsAuthenticated]
#         else:
#             permission_classes = [ReviewCommentPermission]
#         return [permission() for permission in permission_classes]
#
#     @action(detail=True, methods=['patch', 'get', 'delete'])
#     def get(self, request):
#         user_email = request.user.email
#         user = get_object_or_404(User, email=user_email)
#         serializer = CreateUserSerializer(user, many=False)
#         return Response(serializer.data)
#
#     def patch(self, request):
#         user_email = request.user.email
#         user = get_object_or_404(User, email=user_email)
#         serializer = CreateUserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
    #queryset = Titles.objects.all()
    queryset = Titles.objects.annotate(rating=Avg('review__score'))
    serializer_class = TitlesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    # def check_exists(self):  # проверка наличия жанра и категории в базе
    #     category = self.request.data.get("category", None)
    #     #genre = self.request.data.getlist("genres", None)
    #     self.cat_obj = None
    #     self.gen_objects = []
    #     #genre = self.request.data.get("genre", None)
    #     if 'multipart/form-data' in self.request.content_type:
    #         genre = self.request.data.getlist("genre", None)
    #     else:
    #         genre = self.request.data.get("genre", None)
    #     if isinstance(genre, str):
    #         genre = self.request.data.getlist("genre", None)
    #     if (category is None) and (genre is None):
    #         exists_status = True
    #     else:
    #         try:
    #             if category:
    #                 self.cat_obj = Categories.objects.get(slug=category)
    #             if genre:
    #                 self.gen_objects = Genres.objects.filter(slug__in=genre)
    #             exists_status = True
    #         except:
    #             exists_status = False
    #     return self.cat_obj, self.gen_objects, exists_status


class ReviewAPIView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewCommentPermission]
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


class CommentsAPIView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    #permission_classes = [ReviewCommentPermission]
    #permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    #queryset = Comments.objects.all()
    permission_classes = [ReviewCommentPermission]

    def get_queryset(self):
        queryset = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title=self.kwargs.get("title_id"), )
        return queryset.comments.all()

    # def get_queryset(self):
    #     comments = get_list_or_404(Comments, reviews=self.kwargs.get('review_id'))
    #     return comments

    def perform_create(self, serializer):
        reviews = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title=self.kwargs.get("title_id"), )
        #     Review,
        #     id=self.kwargs.get('review_id')
        # )
        serializer.save(
            author=self.request.user,
            reviews=reviews
        )

