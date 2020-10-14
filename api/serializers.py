from django.contrib.auth import get_user_model
from rest_framework import serializers, viewsets
from api.models import *
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

User = get_user_model()


class CategoriesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    slug = serializers.CharField(max_length=200)

    class Meta:
        model = Categories
        fields = '__all__'


class GenresSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    slug = serializers.CharField(max_length=200)

    class Meta:
        model = Genres
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username', many=False
    )
    title = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='description')

    class Meta:
        model = Review
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title']
            )
        ]


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(read_only=True, max_digits=10,
                                      decimal_places=1, coerce_to_string=False)
    category = CategoriesSerializer(read_only=True)
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
        model = Titles


class UpdateTitlesSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)

    class Meta:
        fields = ('id', 'name')
        model = Titles

        def create(self, validated_data):
            return Titles(**validated_data)

        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            return instance

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )
    comment = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='id'
    )

    class Meta:
        fields = '__all__'
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
        #fields = ("email",)
        fields = '__all__'
        model = User
