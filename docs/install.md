# Install

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

Wire package URLs inside `i18n_patterns` so path prefixes translate:

```python
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

urlpatterns += i18n_patterns(
    path("", include("allergens.urls")),
)
```
