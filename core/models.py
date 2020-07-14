from django.conf import settings
from django.db import models

# Create your models here.


class Recipe(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class OrderRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    price = models.FloatField()

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    recipes = models.ManyToManyField(OrderRecipe)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
