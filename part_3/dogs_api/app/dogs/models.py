from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator



class Breed(models.Model):
    SIZES = {
        "Tiny": "Tiny",
        "Small": "Small",
        "Medium": "Medium",
        "Large": "Large",
    }
    name = models.CharField(max_length=255, verbose_name=_("Название породы"))
    size = models.CharField(max_length=10, choices=SIZES, verbose_name=_("Размер"))
    friendliness = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    trainability = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    shedding_amount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    exercise_needs = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


class Dog(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Кличка"))
    age = models.IntegerField(verbose_name=_("Возраст"))
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, verbose_name=_("Порода"))
    gender = models.CharField(max_length=30, verbose_name=_("Пол"))
    color = models.CharField(max_length=50, verbose_name=_("Цвет"))
    favorite_food = models.CharField(max_length=255, verbose_name=_("Любимое блюдо"))
    favorite_toy = models.CharField(max_length=255, verbose_name=_("Любимая игрушка"))