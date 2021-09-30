from django.shortcuts import render
from django.http import HttpResponse
from second_gen import random_adventurers


def index(request):
    adventurers = random_adventurers.random_adventurers(
        alignment=True,
        classes=True,
        epic=True,
        equipment=True,
        expanded=True,
        experience=True,
        slow=True,
    )
    return HttpResponse(f"<pre>{adventurers}</pre>")
