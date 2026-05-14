from abc import ABC, abstractmethod

class Pizza(ABC):
    @abstractmethod
    def get_cost(self): pass
    @abstractmethod
    def get_description(self): pass


class BasePizza(Pizza):
    def __init__(self, base, sauce, cheese):
        self.base = base
        self.sauce = sauce
        self.cheese = cheese

    def get_cost(self):
        return self.base.price + self.sauce.price + self.cheese.price

    def get_description(self):
        return f"{self.base.ingredient_name} + {self.sauce.ingredient_name} + {self.cheese.ingredient_name}"


class PizzaDecorator(Pizza):
    def __init__(self, pizza):
        self._pizza = pizza

    def get_cost(self):
        return self._pizza.get_cost()

    def get_description(self):
        return self._pizza.get_description()


class ToppingDecorator(PizzaDecorator):
    def __init__(self, pizza, topping):
        super().__init__(pizza)
        self.topping = topping

    def get_cost(self):
        return self._pizza.get_cost() + self.topping.price

    def get_description(self):
        return self._pizza.get_description() + f", {self.topping.ingredient_name}"