import datetime
import random
import time

from celery import shared_task

from shop.models import Category, Item, Tag


@shared_task
def generate_items(count=1):
    Item.generate_items(count)


@shared_task
def generate_tags(count=1):
    Tag.generate_tags(count)


@shared_task
def generate_categories(count=1):
    Category.generate_categories(count)


# Test tasks


@shared_task
def mine_bitcoin():
    time.sleep(random.randint(1, 10))


@shared_task
def mine_birthday_bitcoin():
    """We shouldn't be working on our birthdays"""
    ...


@shared_task
def mine_bitcoin_on_lazy_tuesday():
    """We will just simulate some work"""
    time.sleep(random.randint(1, 1))


@shared_task
def mine_bitcoin_for_satan():
    current_year = datetime.datetime.now().year
    if current_year % 4 == 0:
        print("Hello, Satan!")
        time.sleep(random.randint(1, 13))
