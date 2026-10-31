"""Ensure Filer folders/images for catalog seed assets shipped in the wheel."""

from __future__ import annotations

from importlib import resources
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db.models.signals import post_save

from filer.models import Folder
from filer.models.imagemodels import Image


def _owner():
    User = get_user_model()
    user = User.objects.filter(is_superuser=True).order_by("pk").first()
    if user is not None:
        return user
    user = User.objects.order_by("pk").first()
    if user is not None:
        return user
    return User.objects.create_user(
        username="catalog-seed",
        email="catalog-seed@localhost",
        password="catalog-seed-local-only",
    )


def ensure_folder(name: str, parent: Folder | None = None) -> Folder:
    folder, _ = Folder.objects.get_or_create(
        name=name, parent=parent, defaults={"owner": _owner()}
    )
    return folder


def ensure_image_from_package(
    package: str,
    relative: str,
    folder: Folder,
    *,
    name: str | None = None,
) -> Image | None:
    """Import ``package`` resource ``relative`` into Filer if missing.

    Idempotent by ``original_filename`` inside ``folder``.
    """
    try:
        root = resources.files(package).joinpath("data")
        data_file = root.joinpath("images").joinpath(relative)
        if not data_file.is_file():
            # allow relative already including images/
            data_file = root.joinpath(relative)
        if not data_file.is_file():
            return None
        payload = data_file.read_bytes()
        original = Path(relative).name
    except (FileNotFoundError, TypeError, AttributeError):
        return None

    existing = Image.objects.filter(
        folder=folder, original_filename=original
    ).first()
    if existing is not None:
        return existing

    image = Image(
        owner=_owner(),
        folder=folder,
        original_filename=original,
        name=name or Path(original).stem.replace("-", " ").title(),
        is_public=True,
    )
    receivers = list(post_save.receivers)
    post_save.receivers = []
    try:
        image.file.save(original, ContentFile(payload), save=True)
    finally:
        post_save.receivers = receivers
    return image
