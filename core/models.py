from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return "{}".format(self.name)


class SubCategory(models.Model):
    name = models.CharField(max_length=255)
    subcategory = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.name)

class Drink(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    inStock = models.IntegerField()
    emergencyNumber = models.IntegerField()
    emergencyNotification = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {} ({} in stock)".format(self.name, self.category, self.inStock)


class History(models.Model):
    date = models.CharField(max_length=20)

    def __str__(self):
        return "{}".format(self.date)


class Transaction(models.Model):
    bartender = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.ForeignKey(History, on_delete=models.CASCADE)
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    change = models.IntegerField()

    def __str__(self):
        return "{} ({}) by {} on {} ".format(self.drink.name, self.change, self.bartender.first_name, self.date)


class CheckIn(models.Model):
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE)
    history = models.ForeignKey(History, on_delete=models.CASCADE)
    inStockOld = models.IntegerField()
    inStockNew = models.IntegerField()

    def __str__(self):
        return "{} | Old Stock: {} | New Stock: {} | ({})".format(self.drink.name, self.inStockOld, self.inStockNew, self.history.date)
