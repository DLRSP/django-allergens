# django-allergens

[![CI](https://github.com/DLRSP/django-allergens/actions/workflows/ci.yaml/badge.svg)](https://github.com/DLRSP/django-allergens/actions/workflows/ci.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

EU Annex II food allergen vocabulary (+ nickel) for Django, with Filer images,
modeltranslation-ready name/slug/description fields, and an idempotent catalog
loader.

## Requirements

- Python 3.10+
- Django 4.2+
- django-filer
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
    "allergens",
]
```

```shell
python manage.py migrate
python manage.py load_allergen_catalog
```

## Quick usage

```python
from allergens.models import Allergen

egg = Allergen.objects.get(slug="egg")
```

Choice values (`icon`) are English stable codes; Italian labels ship in
`locale/it`. Catalog natural-language fields use modeltranslation (`en` / `it`).

## License

MIT
