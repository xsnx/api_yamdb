from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from api.models import *
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

User = get_user_model()


class CategoriesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    slug = serializers.CharField(max_length=200, validators=[
        UniqueValidator(queryset=Categories.objects.all())])

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    slug = serializers.CharField(max_length=200, validators=[
        UniqueValidator(queryset=Genres.objects.all())])

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    def validate(self, attrs):
        author = self.context["request"].user.id,
        title = self.context["view"].kwargs.get("title_id")
        message = 'Author review already exist'
        if not self.instance and Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError(message)
        return attrs

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(read_only=True, max_digits=10,
                                      decimal_places=1, coerce_to_string=False)
    category = CategoriesSerializer(read_only=True, many=True)
    genre = GenresSerializer(read_only=True, many=True)


    def validate(self, attrs):
        title = self.context["view"].kwargs.get("title_id")
        author = self.context["request"].user
        message = 'Author review already exist'
        if Review.objects.filter(title=title, author=author).exists():
            raise serializers.ValidationError(message)
        return attrs

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'category',
                  'genre')
        #fields = '__all__'
        model = Titles


# class UpdateTitlesSerializer(serializers.Serializer):
#     name = serializers.CharField(max_length=200)
#
#     class Meta:
#         fields = ('id', 'name')
#         model = Titles
#
#         def create(self, validated_data):
#             return Titles(**validated_data)
#
#         def update(self, instance, validated_data):
#             instance.name = validated_data.get('name', instance.name)
#             return instance

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )
    # comment = serializers.SlugRelatedField(
    #     many=False,
    #     read_only=True,
    #     slug_field='comment'
    # )
    #review = serializers.SlugRelatedField(slug_field='review', read_only=True)

    class Meta:
        #fields = '__all__'
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    username = serializers.CharField(
        required=False,
        default=None,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ('username', 'role', 'email', 'first_name', 'last_name', 'bio')
