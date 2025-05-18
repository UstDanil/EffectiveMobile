from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from dogs.models import Dog, Breed


class DogsSerializer(ModelSerializer):
    """Default serializer for Dog model."""
    class Meta:
        model = Dog
        fields = '__all__'


class DogsListSerializer(ModelSerializer):
    """Serializer for Dog model (list api method)."""
    avg_breed_age = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)

    class Meta:
        model = Dog
        fields = ('id', 'name', 'age', 'breed', 'gender', 'color',
                  'favorite_food', 'favorite_toy', 'avg_breed_age')


class DogsDetailSerializer(ModelSerializer):
    """Serializer for Dog model (detail api method)."""
    breed_dogs_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dog
        fields = ('id', 'name', 'age', 'breed', 'gender', 'color',
                  'favorite_food', 'favorite_toy', 'breed_dogs_count')


class BreedsSerializer(ModelSerializer):
    """Default serializer for Breed model."""
    class Meta:
        model = Breed
        fields = '__all__'


class BreedsListSerializer(ModelSerializer):
    """Serializer for Breed model (list api method)."""
    dogs_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Breed
        fields = ('id', 'name', 'size', 'friendliness', 'trainability',
                  'shedding_amount', 'exercise_needs', 'dogs_count')

