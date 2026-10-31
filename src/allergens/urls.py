"""URL patterns for django-allergens (translated path prefixes)."""

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import path
from django.utils.translation import gettext_lazy as _

from allergens.models import Allergen


def allergen_list(request):
    names = ", ".join(Allergen.objects.order_by("index", "name").values_list("name", flat=True))
    return HttpResponse(names or "allergens")


def allergen_detail(request, slug):
    allergen = get_object_or_404(Allergen, slug=slug)
    return HttpResponse(allergen.name)


urlpatterns = [
    path(_("allergens/"), allergen_list, name="allergens"),
    path(_("allergens/<slug:slug>/"), allergen_detail, name="allergen-detail"),
]
