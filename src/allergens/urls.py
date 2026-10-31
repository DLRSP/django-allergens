"""URL patterns for django-allergens."""

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import path

from allergens.models import Allergen


def allergen_detail(request, slug):
    allergen = get_object_or_404(Allergen, slug=slug)
    return HttpResponse(allergen.name)


urlpatterns = [
    path("allergens/<slug:slug>/", allergen_detail, name="allergen-detail"),
]
