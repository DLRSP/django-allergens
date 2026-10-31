"""Idempotent allergen catalog loader (keyed by English slug)."""

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
            slug_en = row.get("slug_en") or row["slug"]
            slug_it = row.get("slug_it") or slug_en
            name_en = row.get("name_en") or row.get("name_it") or slug_en
            name_it = row.get("name_it") or name_en
            defaults = {
                "name": name_en,
                "description": row.get("description_en")
                or row.get("description_it")
                or "",
                "icon": row.get("icon") or "",
                "index": row.get("index"),
            }
            obj, was_created = Allergen.objects.update_or_create(
                slug=slug_en,
                defaults=defaults,
            )
            if hasattr(obj, "name_en"):
                obj.name_en = name_en
            if hasattr(obj, "name_it"):
                obj.name_it = name_it
            if hasattr(obj, "description_en"):
                obj.description_en = row.get("description_en") or ""
            if hasattr(obj, "description_it"):
                obj.description_it = row.get("description_it") or ""
            if hasattr(obj, "slug_en"):
                obj.slug_en = slug_en
            if hasattr(obj, "slug_it"):
                obj.slug_it = slug_it
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
