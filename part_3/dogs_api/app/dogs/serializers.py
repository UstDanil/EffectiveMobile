from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from dogs.models import Dog, Breed


class DogsSerializer(ModelSerializer):
    class Meta:
        model = Dog
        fields = '__all__'


class DogsListSerializer(ModelSerializer):
    avg_breed_age = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)

    class Meta:
        model = Dog
        fields = ('id', 'name', 'age', 'breed', 'gender', 'color',
                  'favorite_food', 'favorite_toy', 'avg_breed_age')


class DogsDetailSerializer(ModelSerializer):
    breed_dogs_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dog
        fields = ('id', 'name', 'age', 'breed', 'gender', 'color',
                  'favorite_food', 'favorite_toy', 'breed_dogs_count')


class BreedsSerializer(ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'


class BreedsListSerializer(ModelSerializer):
    dogs_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Breed
        fields = ('id', 'name', 'size', 'friendliness', 'trainability',
                  'shedding_amount', 'exercise_needs', 'dogs_count')

