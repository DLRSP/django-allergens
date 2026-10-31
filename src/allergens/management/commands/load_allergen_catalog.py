"""Idempotent allergen catalog loader (keyed by slug)."""

from __future__ import annotations

import json
from importlib import resources

from django.core.management.base import BaseCommand
from django.db import transaction

from allergens.models import Allergen


def _load_rows() -> list[dict]:
    package = resources.files("allergens").joinpath("data")
    raw = package.joinpath("allergens.json").read_text(encoding="utf-8")
    return json.loads(raw)


class Command(BaseCommand):
    help = "Load the EU allergen (+ nickel) catalog idempotently by slug."

    @transaction.atomic
    def handle(self, *args, **options):
        created = updated = 0
        for row in _load_rows():
            defaults = {
                "name": row.get("name_en") or row.get("name_it") or row["slug"],
                "description": row.get("description_en")
                or row.get("description_it")
                or "",
                "icon": row.get("icon") or "",
                "index": row.get("index"),
            }
            obj, was_created = Allergen.objects.update_or_create(
                slug=row["slug"],
                defaults=defaults,
            )
            # Prefer Italian translations when modeltranslation columns exist.
            if hasattr(obj, "name_it") and row.get("name_it"):
                obj.name_it = row["name_it"]
            if hasattr(obj, "description_it") and row.get("description_it") is not None:
                obj.description_it = row["description_it"]
            if hasattr(obj, "name_en") and row.get("name_en"):
                obj.name_en = row["name_en"]
            if hasattr(obj, "description_en") and row.get("description_en") is not None:
                obj.description_en = row["description_en"]
            if hasattr(obj, "slug_it"):
                obj.slug_it = row["slug"]
            if hasattr(obj, "slug_en"):
                obj.slug_en = row["slug"]
            obj.save()
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Allergen catalog: {created} created, {updated} updated "
                f"({created + updated} total)."
            )
        )
