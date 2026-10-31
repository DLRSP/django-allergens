from django.contrib import admin

from allergens.models import Allergen


@admin.register(Allergen)
class AllergenAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon", "index")
    list_editable = ("index",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug", "description")
    ordering = ("index", "name")
