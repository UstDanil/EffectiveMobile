from django.test import TestCase

from dogs.models import Breed, Dog
from dogs.serializers import DogsSerializer, BreedsSerializer



class BreedsSerializerTestCase(TestCase):
    """Tests for BreedsSerializer."""
    def test_breeds_serializer(self):
        """Test BreedsSerializer.data corresponds Breed model data.
        Args:
        Returns:
        Raises:
        """
        breed_1 = Breed.objects.create(name='Питбуль', size='Small', friendliness=1,
                                       trainability=1, shedding_amount=1, exercise_needs=1)
        data = BreedsSerializer(breed_1).data
        expected_data = {
            'id': breed_1.id,
            'name': 'Питбуль',
            'size': 'Small',
            'friendliness': 1,
            'trainability': 1,
            'shedding_amount': 1,
            'exercise_needs': 1,
        }
        self.assertEqual(data, expected_data)


class DogsSerializerTestCase(TestCase):
    """Tests for DogsSerializer."""
    def test_dogs_serializer(self):
        """Test DogsSerializer.data corresponds Dog model data.
        Args:
        Returns:
        Raises:
        """
        breed_1 = Breed.objects.create(name='Питбуль', size='Small', friendliness=1,
                                       trainability=1, shedding_amount=1, exercise_needs=1)
        dog_1 = Dog.objects.create(name='Ванек', age=2, breed=breed_1, gender='f',
                                   color='Серый', favorite_food='Курица', favorite_toy='Мяч')
        data = DogsSerializer(dog_1).data
        expected_data = {
            'id': dog_1.id,
            'name': 'Ванек',
            'age': 2,
            'gender': 'f',
            'color': 'Серый',
            'favorite_food': 'Курица',
            'favorite_toy': 'Мяч',
            'breed': breed_1.id
        }
        self.assertEqual(data, expected_data)
