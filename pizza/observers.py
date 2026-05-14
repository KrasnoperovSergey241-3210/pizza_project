from abc import ABC, abstractmethod
from .models import Order, OrderNotification

class Observer(ABC):
    @abstractmethod
    def update(self, order: Order):
        pass


class KitchenObserver(Observer):
    def update(self, order: Order):
        OrderNotification.objects.create(
            order=order,
            observer_type="Кухня",
            message=f"Заказ #{order.order_id} изменил статус на: {order.status}"
        )


class CustomerObserver(Observer):
    def update(self, order: Order):
        OrderNotification.objects.create(
            order=order,
            observer_type="Клиент",
            message=f"Ваш заказ #{order.order_id} теперь в статусе: {order.status}"
        )


class AdminObserver(Observer):
    def update(self, order: Order):
        OrderNotification.objects.create(
            order=order,
            observer_type="Администратор",
            message=f"Заказ #{order.order_id} обновлён до статуса: {order.status}"
        )


class OrderSubject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, order: Order):
        for observer in self._observers:
            observer.update(order)