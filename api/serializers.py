from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.models import Categories, Genres, Titles, Review, Comments
from rest_framework.validators import UniqueValidator

User = get_user_model()


class CategoriesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    slug = serializers.CharField(max_length=100, validators=[
        UniqueValidator(queryset=Categories.objects.all())])

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    slug = serializers.CharField(max_length=100, validators=[
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
        if not self.instance and Review.objects.filter(title=title,
                                                       author=author).exists():
            raise serializers.ValidationError(message)
        return attrs

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(read_only=True, max_digits=10,
                                      decimal_places=1, coerce_to_string=False)
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(many=True)

    class Meta:
 #       fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
 #                 'category')
        fields = '__all__'
        model = Titles


 #   rating = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=1, coerce_to_string=False)
    #category = CategoriesSerializer()
  #  category = CategoriesSerializer(read_only=True) #, many=True)
  #  genre = GenresSerializer(many=True) #read_only=True) #, many=True)
    #genre = GenresSerializer()

 #   class Meta:
        #fields = '__all__'
  #      fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        #fields = ('id', 'name', 'category', 'genre', 'year', 'rating') #name', 'year', 'rating', 'description', 'genre', 'category')
   #     model = Titles


class UpdateTitlesSerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(read_only=True, max_digits=10,
                                      decimal_places=1, coerce_to_string=False)

    category = serializers.SlugRelatedField(
        queryset=Categories.objects.all(),
        slug_field='slug',
        required=False,
    )
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True,
        required=False,
        )

    class Meta:
     #   fields = '__all__'
        fields = ('id', 'name', 'genre', 'category', 'rating', 'year', 'description') #, 'rating', 'description',  'category' 'year',)
        model = Titles





 #   rating = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=1, coerce_to_string=False)
 #   category = serializers.SlugRelatedField(many=True,  slug_field='slug', queryset=Categories.objects.all(),) #queryset=Categories.objects.all(),
 #   genre = serializers.SlugRelatedField(many=True,  slug_field='slug', queryset=Genres.objects.all(), required=False,) #, many=True) queryset=Genres.objects.all(),

 #   class Meta:
 #       model = Titles
 #       fields = ('id', 'name', 'year', 'rating', 'description',  'genre', 'category')
        #fields = '__all__'


#        def create(self, validated_data):
#            return Titles(**validated_data)

#        def update(self, instance, validated_data):
#            instance.name = validated_data.get('name', instance.name)
#            return instance



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments
