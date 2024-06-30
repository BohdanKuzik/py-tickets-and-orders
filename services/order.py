from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, MovieSession, Ticket, User


def create_order(tickets: list, username: User, date: str = None) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save(update_fields=["created_at"])

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                pk=ticket_data["movie_session"]
            )
            ticket = Ticket(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session=movie_session,
                order=order
            )
            ticket.full_clean()
            ticket.save()

        return order


def get_orders(username: User = None) -> None:
    if username:
        user = get_user_model().objects.get(username=username)
        orders = Order.objects.filter(user=user)
    else:
        orders = Order.objects.all()

    return orders
