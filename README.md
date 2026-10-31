# django-allergens

[![CI](https://github.com/DLRSP/django-allergens/actions/workflows/ci.yaml/badge.svg)](https://github.com/DLRSP/django-allergens/actions/workflows/ci.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docs](https://img.shields.io/badge/docs-github.io-blue)](https://dlrsp.github.io/django-allergens/)

EU Annex II food **allergen vocabulary** (+ nickel) for Django sites, with
translatable names/slugs, catalog images, and an idempotent seed loader.

## Why use it

- Standard allergen codes and labels without maintaining your own list
- English default with Italian UI, URL prefixes (`allergeni/`), and catalog fields
- Filer-backed images ready for admin and public pages
- Drop-in dependency for ingredient and recipe catalogs

## Requirements

- Python 3.10+
- Django 4.2+
- django-filer (+ mptt, easy-thumbnails, polymorphic)
- django-modeltranslation

## Install

```shell
pip install django-allergens
```

```python
INSTALLED_APPS = [
    "modeltranslation",  # before django.contrib.admin
    # ...
    "easy_thumbnails",
    "filer",
    "mptt",
    "polymorphic",
    "allergens",
]
```

```shell
python manage.py migrate
python manage.py load_allergen_catalog
```

Include `allergens.urls` inside `i18n_patterns` for translated path prefixes.

## Quick usage

```python
from allergens.models import Allergen

egg = Allergen.objects.get(slug="egg")
```

## License

MIT
