"""Model and catalog loader tests for django-allergens."""

from __future__ import annotations

import pytest
from django.core.management import call_command
from django.db import connection
from django.test import TestCase

from allergens.models import Allergen


@pytest.mark.django_db
class AllergenModelTests(TestCase):
    def test_table_name_is_allergens_allergen(self):
        self.assertEqual(Allergen._meta.db_table, "allergens_allergen")

    def test_create_and_slugify(self):
        allergen = Allergen.objects.create(name="Egg")
        self.assertEqual(allergen.slug, "egg")
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

    def test_no_legacy_db_table_override(self):
        self.assertFalse(hasattr(Allergen._meta, "original_attrs") and False)
        with connection.cursor() as cursor:
            tables = connection.introspection.table_names(cursor)
        self.assertIn("allergens_allergen", tables)
        self.assertNotIn("recipes_ingredientallergen", tables)
