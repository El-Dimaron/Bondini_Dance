from django.http import HttpRequest, HttpResponse
from faker import Faker

from blog.models import Blog, Entity


def create(request: HttpRequest) -> HttpResponse:
    faker = Faker("UK")

    saved_data = Entity(
        blog=[Blog(name=faker.word(), text=faker.text(), author=faker.name()) for _ in range(3)],
        headline=faker.paragraph(nb_sentences=1),
    ).save()

    return HttpResponse(f"{saved_data}")


def all_blogs(request: HttpRequest) -> HttpResponse:
    blogs = Entity.objects.all()

    return HttpResponse(f"Blogs: {[blog.headline for blog in blogs]}")
