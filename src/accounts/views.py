from django.http import HttpRequest, HttpResponse

from accounts.tasks import generate_users


def users(request: HttpRequest) -> HttpResponse:
    try:
        count = int(request.GET.get("count", 1))
    except ValueError:
        count = 1
    generate_users.delay(count)
    return HttpResponse("Task generate_users started")
