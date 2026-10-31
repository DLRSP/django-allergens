from modeltranslation.translator import TranslationOptions, register

from allergens.models import Allergen


@register(Allergen)
class AllergenTranslationOptions(TranslationOptions):
    fields = ("name", "slug", "description")
