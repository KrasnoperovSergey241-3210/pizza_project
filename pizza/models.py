from django.db import models
from django.utils import timezone
from abc import ABC, abstractmethod

class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    password = models.CharField(max_length=255)
    registration_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    loyalty_points = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    permissions = models.CharField(max_length=255, default="full")
    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.username


class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient_name = models.CharField(max_length=100)
    price = models.FloatField()
    is_available = models.BooleanField(default=True)
    unit = models.CharField(max_length=20, default="шт")
    category = models.CharField(max_length=30, choices=[
        ('base', 'Основа'), ('sauce', 'Соус'), ('cheese', 'Сыр'), ('topping', 'Топпинг')
    ])

    def __str__(self):
        return f"{self.ingredient_name} ({self.price} ₽)"


class Pizza(models.Model):
    pizza_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    base_price = models.FloatField()
    is_available = models.BooleanField(default=True)
    category = models.CharField(max_length=50, default="Классическая")
    ingredients = models.ManyToManyField(Ingredient, through='PizzaIngredient')

    def __str__(self):
        return self.name


class PizzaIngredient(models.Model):
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class CustomPizza(models.Model):
    custom_pizza_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    custom_price = models.FloatField()
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    composition = models.JSONField(default=dict)

    def __str__(self):
        return f"Кастомная пицца #{self.custom_pizza_id}"


class CustomPizzaIngredient(models.Model):
    custom_pizza = models.ForeignKey(CustomPizza, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


class Order(models.Model):
    STATUS_CHOICES = [
        ('Принят', 'Принят'),
        ('Готовится', 'Готовится'),
        ('В печи', 'В печи'),
        ('Передан курьеру', 'Передан курьеру'),
        ('Доставлен', 'Доставлен'),
        ('Отменен', 'Отменен'),
    ]
    
    STATUS_FOR_DELIVERY = ['Принят', 'Готовится', 'В печи', 'Передан курьеру', 'Доставлен']
    STATUS_FOR_PICKUP = ['Принят', 'Готовится', 'В печи', 'Доставлен']
    
    order_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    courier = models.ForeignKey('Courier', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Принят')
    delivery_type = models.CharField(max_length=20, choices=[('delivery', 'Доставка'), ('pickup', 'Самовывоз')])
    amount = models.FloatField()
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def get_next_status(self):
        if self.delivery_type == 'delivery':
            statuses = self.STATUS_FOR_DELIVERY
        else:
            statuses = self.STATUS_FOR_PICKUP
        try:
            idx = statuses.index(self.status)
            if idx < len(statuses) - 1:
                return statuses[idx + 1]
        except ValueError:
            pass
        return None

    def __str__(self):
        return f"Заказ #{self.order_id} — {self.status}"


class Courier(models.Model):
    courier_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    status = models.CharField(max_length=30, default="Свободен")

    def __str__(self):
        return self.name


class OrderStatusHistory(models.Model):
    status_history_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    changed_at = models.DateTimeField(default=timezone.now)


class OrderNotification(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    observer_type = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.observer_type} - Заказ #{self.order.order_id}"


class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=100, blank=True)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, null=True, blank=True)
    custom_pizza = models.ForeignKey(CustomPizza, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)