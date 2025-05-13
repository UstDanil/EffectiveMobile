from rest_framework.viewsets import ModelViewSet

from dogs.models import Dog, Breed
from dogs.serializers import DogsSerializer, BreedsSerializer


class DogViewSet(ModelViewSet):
    queryset = Dog.objects.all()
    serializer_class = DogsSerializer


class BreedViewSet(ModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedsSerializer
