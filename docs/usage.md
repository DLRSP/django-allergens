# Usage

```python
from allergens.models import Allergen

egg = Allergen.objects.get(slug="egg")
print(egg.name_en, egg.name_it)  # Egg / Uovo
print(egg.slug_en, egg.slug_it)  # egg / uovo
```

Choice values (`icon`) are stable English codes; Italian labels live in
`locale/it`. Catalog natural-language fields use modeltranslation (`en` / `it`).

URL reverse examples (with `LocaleMiddleware` + `i18n_patterns`):

- English: `/en/allergens/egg/`
- Italian: `/it/allergeni/uovo/`
