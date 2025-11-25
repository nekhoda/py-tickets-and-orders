from django.db.models import QuerySet

from db.models import Order, User, Ticket
from datetime import datetime
from django.db import transaction


def create_order(tickets: list, username: str, date: datetime = None) -> Order:
    with transaction.atomic():
        new_order = Order.objects.create(
            user=User.objects.get(
                username=username
            )
        )
        if date:
            new_order.created_at = date

        Ticket.objects.bulk_create(
            [
                Ticket(
                    order=new_order,
                    seat=ticket["seat"],
                    row=ticket["row"],
                    movie_session_id=ticket["movie_session"]
                ) for ticket in tickets
            ]
        )
        return new_order

def get_orders(username: str = None) -> QuerySet:
    if username:
        return User.objects.get(username=username).orders.all()
    return Order.objects.all()