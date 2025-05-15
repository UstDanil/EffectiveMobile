from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dogs.models import Breed, Dog


class BreedsApiTestCase(APITestCase):
    def setUp(self):
        self.breed = Breed.objects.create(name='Питбуль', size='Small', friendliness=1,
                                       trainability=1, shedding_amount=1, exercise_needs=1)

    def test_get_all_breeds(self):
        url = reverse('breed-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))

    def test_create_breed(self):
        url = reverse('breed-list')
        data = {
            'name': 'Пудель',
            'size': 'Small',
            'friendliness': 2,
            'trainability': 2,
            'shedding_amount': 2,
            'exercise_needs': 2,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_breed(self):
        url = reverse('breed-detail', args=[self.breed.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Питбуль')

    def test_update_breed(self):
        url = reverse('breed-detail', args=[self.breed.pk])
        data = {
            'name': 'Такса',
            'size': 'Small',
            'friendliness': 3,
            'trainability': 3,
            'shedding_amount': 3,
            'exercise_needs': 3,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        breed = Breed.objects.get(pk=self.breed.pk)
        self.assertEqual(breed.name, 'Такса')

    def test_delete_breed(self):
        url = reverse('breed-detail', args=[self.breed.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Breed.objects.filter(pk=self.breed.pk).exists())


class DogsApiTestCase(APITestCase):
    def setUp(self):
        self.breed = Breed.objects.create(name='Питбуль', size='Small', friendliness=1,
                                       trainability=1, shedding_amount=1, exercise_needs=1)
        self.dog = Dog.objects.create(name='Маня', age=2, breed=self.breed, gender='f',
                                   color='Серый', favorite_food='Курица', favorite_toy='Мяч')

    def test_get_all_dogs(self):
        url = reverse('dog-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))

    def test_create_dog(self):
        url = reverse('dog-list')
        data = {
            'name': 'Петя',
            'age': 2,
            'gender': 'm',
            'color': 'Серый',
            'favorite_food': 'Корм',
            'favorite_toy': 'Утка',
            'breed': self.breed.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_dog(self):
        url = reverse('dog-detail', args=[self.dog.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Маня')

    def test_update_dog(self):
        url = reverse('dog-detail', args=[self.dog.pk])
        data = {
            'name': 'Степа',
            'age': 2,
            'gender': 'm',
            'color': 'Белый',
            'favorite_food': 'Кость',
            'favorite_toy': 'Подушка',
            'breed': self.breed.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        dog = Dog.objects.get(pk=self.dog.pk)
        self.assertEqual(dog.name, 'Степа')

    def test_delete_dog(self):
        url = reverse('dog-detail', args=[self.dog.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Dog.objects.filter(pk=self.dog.pk).exists())

