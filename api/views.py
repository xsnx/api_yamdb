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
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination



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
