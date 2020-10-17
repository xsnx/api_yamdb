from django.contrib.auth.tokens import default_token_generator
<<<<<<< HEAD
from django.db.models import Avg
from django.shortcuts import get_list_or_404
=======
>>>>>>> a97b56982a67d5f79dc37082d7b088307db66ede
from rest_framework import viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, BasePermission, \
<<<<<<< HEAD
    AllowAny, IsAuthenticatedOrReadOnly
=======
    AllowAny
>>>>>>> a97b56982a67d5f79dc37082d7b088307db66ede
from rest_framework.views import APIView
from rest_framework import viewsets, filters, mixins
from api.serializers import *
from api.permissions import *
from api.models import *
from rest_framework.response import Response
from rest_framework.decorators import action


class UserViewSet(viewsets.ModelViewSet):
<<<<<<< HEAD
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    #permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated, BasePermission]
    lookup_field = 'username'

=======
    #serializer_class = CreateUserSerializer
    #queryset = User.objects.all()
    #permission_classes = [AllowAny]
    #permission_classes = [IsAuthenticated, UserPermission]
    lookup_field = "username"

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

#
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = CreateUserSerializer
#     lookup_field = 'username'
#
#     def get_permissions(self):
#         if self.action in ['get', 'patch', 'delete']:
#             permission_classes = [IsAuthenticated]
#         else:
#             permission_classes = [IsAdminOrReadOnly]
#         return [permission() for permission in permission_classes] \
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
#         serializer = CreateUserSerializer(user, data=request.data,
#                                           partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
>>>>>>> a97b56982a67d5f79dc37082d7b088307db66ede


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


<<<<<<< HEAD
#class CategoryAPIView(viewsets.ModelViewSet):
 #   queryset = Categories.objects.all()
 #   serializer_class = CategoriesSerializer
 #   filter_backends = [filters.SearchFilter]
 #   search_fields = ['=name']
 #   permission_classes = [IsAdminOrReadOnly]
 #   pagination_class = PageNumberPagination


class CategoryAPIView(mixins.DestroyModelMixin, mixins.CreateModelMixin,
                      mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    def destroy(self, request, slug=None):
        genre = self.queryset.filter(slug=slug)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenresAPIView(mixins.DestroyModelMixin, mixins.CreateModelMixin,
                    mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination

    def destroy(self, request, slug):
        del_genre = self.queryset.filter(slug=slug)
        del_genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitlesAPIView(viewsets.ModelViewSet):
    #queryset = Titles.objects.all()
    queryset = Titles.objects.annotate(rating=Avg('review__score'))
    serializer_class = TitlesSerializer
=======
class CategoryAPIView(viewsets.ModelViewSet):
    #queryset = Categories.objects.all()
    #serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    #permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


class GenresAPIView(viewsets.ModelViewSet):
    #queryset = Genres.objects.all()
   # serializer_class = GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


class TitlesAPIView(viewsets.ModelViewSet):
    #queryset = Titles.objects.all()
   # serializer_class = TitlesSerializer
>>>>>>> a97b56982a67d5f79dc37082d7b088307db66ede
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination


<<<<<<< HEAD

class ReviewAPIView(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewCommentPermission]
=======
class ReviewAPIView(viewsets.ModelViewSet):
    #serializer_class = ReviewSerializer
    permission_classes = [OnlyCreatorPermission, IsAdminOrReadOnly]
       #IsAuthorOrIsStaffPermission, IsAuthPostPermission, ReadOnly]
>>>>>>> a97b56982a67d5f79dc37082d7b088307db66ede
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

<<<<<<< HEAD

class CommentsAPIView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    #permission_classes = [ReviewCommentPermission]
    #permission_classes = [AllowAny]
    pagination_class = PageNumberPagination
    #queryset = Comments.objects.all()
    permission_classes = [ReviewCommentPermission]
=======
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
    #serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = [IsAuthenticated, ReviewCommentPermission]
    pagination_class = PageNumberPagination
>>>>>>> a97b56982a67d5f79dc37082d7b088307db66ede

    def get_queryset(self):
        queryset = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
<<<<<<< HEAD
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
=======
            title=self.kwargs.get("title__id"), )
        return queryset.comments.all()
>>>>>>> a97b56982a67d5f79dc37082d7b088307db66ede
