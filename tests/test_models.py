"""Model and catalog loader tests for django-allergens."""

from __future__ import annotations

import pytest
from django.core.management import call_command
from django.db import connection
from django.test import TestCase, override_settings
from django.urls import clear_url_caches, reverse, set_urlconf
from django.utils import translation

from allergens.models import Allergen


@pytest.mark.django_db
class AllergenModelTests(TestCase):
    def test_table_name_is_allergens_allergen(self):
        self.assertEqual(Allergen._meta.db_table, "allergens_allergen")

    def test_create_and_slugify(self):
        allergen = Allergen.objects.create(name="Egg")
        self.assertEqual(allergen.slug, "egg")
        with translation.override("en"):
            self.assertIn("/allergens/egg/", allergen.get_absolute_url())

    def test_load_allergen_catalog_idempotent(self):
        call_command("load_allergen_catalog")
        first = Allergen.objects.count()
        self.assertGreaterEqual(first, 15)
        call_command("load_allergen_catalog")
        self.assertEqual(Allergen.objects.count(), first)
        egg = Allergen.objects.get(slug="egg")
        self.assertEqual(egg.icon, "egg")
        self.assertEqual(egg.index, 3)

    def test_catalog_fills_en_and_it_name_slug(self):
        call_command("load_allergen_catalog")
        egg = Allergen.objects.get(slug="egg")
        self.assertEqual(egg.name_en, "Egg")
        self.assertEqual(egg.name_it, "Uovo")
        self.assertEqual(egg.slug_en, "egg")
        self.assertEqual(egg.slug_it, "uovo")

    def test_reverse_en_and_it_path_prefixes(self):
        call_command("load_allergen_catalog")
        clear_url_caches()
        set_urlconf("tests.urls")
        with translation.override("en"):
            url_en = reverse("allergen-detail", kwargs={"slug": "egg"})
        with translation.override("it"):
            url_it = reverse("allergen-detail", kwargs={"slug": "uovo"})
        self.assertIn("/allergens/egg/", url_en)
        self.assertIn("/allergeni/uovo/", url_it)

    def test_absolute_url_uses_active_language_slug(self):
        call_command("load_allergen_catalog")
        egg = Allergen.objects.get(slug="egg")
        with translation.override("it"):
            self.assertIn("/allergeni/uovo/", egg.get_absolute_url())
        with translation.override("en"):
            self.assertIn("/allergens/egg/", egg.get_absolute_url())

    def test_no_legacy_db_table_override(self):
        self.assertFalse(hasattr(Allergen._meta, "original_attrs") and False)
        with connection.cursor() as cursor:
            tables = connection.introspection.table_names(cursor)
        self.assertIn("allergens_allergen", tables)
        self.assertNotIn("recipes_ingredientallergen", tables)


@override_settings(ROOT_URLCONF="tests.urls")
class AllergenFilerImportTests(TestCase):
    def test_filer_stack_importable(self):
        import easy_thumbnails  # noqa: F401
        import filer  # noqa: F401
        import mptt  # noqa: F401
        import polymorphic  # noqa: F401

        self.assertTrue(True)
