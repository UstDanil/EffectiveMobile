from django.db.models import Avg, F, Window, Count, Subquery, OuterRef, Func
from rest_framework.viewsets import ModelViewSet

from dogs.models import Dog, Breed
from dogs.serializers import (DogsSerializer, BreedsSerializer, BreedsListSerializer,
                              DogsListSerializer, DogsDetailSerializer)


class DogViewSet(ModelViewSet):
    """Views for Dog API /api/dogs/ (GET, POST), /api/dogs/<int:iD> (GET, PUT, DELETE)."""
    queryset = Dog.objects.all()
    serializer_class = DogsSerializer
    list_serializer_class = DogsListSerializer
    detail_serializer_class = DogsDetailSerializer

    def get_serializer_class(self):
        """Returns serializer for certain view
        Args:
        Returns:
            serializer: DogsSerializer, DogsListSerializer or DogsDetailSerializer
        Raises:
        """
        if self.action == 'list':
            if hasattr(self, 'list_serializer_class'):
                return self.list_serializer_class

        if self.action == 'retrieve':
            if hasattr(self, 'detail_serializer_class'):
                return self.detail_serializer_class

        return super(DogViewSet, self).get_serializer_class()

    def get_queryset(self):
        """Get objects set for certain view
        Args:
        Returns:
            queryset: objects of Dog model
        Raises:
        """
        if self.action == 'list':
            queryset = Dog.objects.all().annotate(
                avg_breed_age=Window(
                    expression=Avg("age"),
                    partition_by=[F("breed")],
                ),
            )
            return queryset
        if self.action == 'retrieve':
            breed_dogs_count = Dog.objects.filter(
                breed=OuterRef('breed'),
            ).order_by().annotate(
                count=Func(F('id'), function='Count')
            ).values('count')
            queryset = Dog.objects.all().annotate(
                breed_dogs_count=Subquery(breed_dogs_count)
            )
            return queryset
        return Dog.objects.all()


class BreedViewSet(ModelViewSet):
    """Views for Breed API /api/breeds/ (GET, POST), /api/breeds/<int:iD> (GET, PUT, DELETE)."""
    queryset = Breed.objects.all()
    serializer_class = BreedsSerializer
    list_serializer_class = BreedsListSerializer

    def get_serializer_class(self):
        """Returns serializer for certain view
        Args:
        Returns:
            serializer: BreedsSerializer or BreedsListSerializer
        Raises:
        """
        if self.action == 'list':
            if hasattr(self, 'list_serializer_class'):
                return self.list_serializer_class
        return super(BreedViewSet, self).get_serializer_class()

    def get_queryset(self):
        """Get objects set for certain view
        Args:
        Returns:
            queryset: objects of Breed model
        Raises:
        """
        if self.action == 'list':
            queryset = Breed.objects.all().annotate(dogs_count=Count("dogs"))
            return queryset
        return Breed.objects.all()
