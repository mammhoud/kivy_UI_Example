from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    quantity_in_stock = models.IntegerField()
    brand = models.CharField(max_length=100)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    cost = models.FloatField()
