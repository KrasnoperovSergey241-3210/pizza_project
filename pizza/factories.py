from abc import ABC, abstractmethod
from .models import Ingredient

class PizzaStyleFactory(ABC):
    @abstractmethod
    def create_base(self): pass
    @abstractmethod
    def create_sauce(self): pass
    @abstractmethod
    def create_cheese(self): pass


class ClassicPizzaFactory(PizzaStyleFactory):
    def create_base(self):
        return Ingredient.objects.get_or_create(ingredient_name="Тонкое тесто", category='base', defaults={'price': 120})[0]
    def create_sauce(self):
        return Ingredient.objects.get_or_create(ingredient_name="Кетчуп", category='sauce', defaults={'price': 50})[0]
    def create_cheese(self):
        return Ingredient.objects.get_or_create(ingredient_name="Моцарелла", category='cheese', defaults={'price': 90})[0]


class MeatLoversFactory(PizzaStyleFactory):
    def create_base(self):
        return Ingredient.objects.get_or_create(ingredient_name="Толстое тесто", category='base', defaults={'price': 150})[0]
    def create_sauce(self):
        return Ingredient.objects.get_or_create(ingredient_name="Соус Барбекю", category='sauce', defaults={'price': 60})[0]
    def create_cheese(self):
        return Ingredient.objects.get_or_create(ingredient_name="Моцарелла", category='cheese', defaults={'price': 90})[0]


class CheeseLoversFactory(PizzaStyleFactory):
    def create_base(self):
        return Ingredient.objects.get_or_create(ingredient_name="Толстое тесто", category='base', defaults={'price': 150})[0]
    def create_sauce(self):
        return Ingredient.objects.get_or_create(ingredient_name="Сырный соус", category='sauce', defaults={'price': 70})[0]
    def create_cheese(self):
        return Ingredient.objects.get_or_create(ingredient_name="Чеддер", category='cheese', defaults={'price': 100})[0]


class VeggieFactory(PizzaStyleFactory):
    def create_base(self):
        return Ingredient.objects.get_or_create(ingredient_name="Тонкое тесто", category='base', defaults={'price': 120})[0]
    def create_sauce(self):
        return Ingredient.objects.get_or_create(ingredient_name="Веганский песто", category='sauce', defaults={'price': 80})[0]
    def create_cheese(self):
        return Ingredient.objects.get_or_create(ingredient_name="Растительный сыр", category='cheese', defaults={'price': 110})[0]