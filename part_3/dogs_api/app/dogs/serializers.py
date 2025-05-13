from rest_framework.serializers import ModelSerializer
from dogs.models import Dog, Breed


class DogsSerializer(ModelSerializer):
    class Meta:
        model = Dog
        fields = '__all__'


class BreedsSerializer(ModelSerializer):
    class Meta:
        model = Breed
        fields = '__all__'
