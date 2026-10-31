from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import get_language, gettext_lazy as _
from filer.fields.image import FilerImageField

from allergens.constants import ALLERGEN_ICON


def _active_slug(obj, field="slug"):
    lang = (get_language() or "en").split("-")[0]
    value = getattr(obj, f"{field}_{lang}", None)
    return value or getattr(obj, field)


class Allergen(models.Model):
    name = models.CharField(_("Name"), max_length=200)
    slug = models.SlugField(_("Slug"), unique=True)
    description = models.CharField(_("Description"), max_length=200, blank=True)
    icon = models.CharField(
        _("Icon"),
        choices=ALLERGEN_ICON,
        max_length=40,
        default="",
        blank=True,
    )
    index = models.IntegerField(_("Allergen index"), null=True, blank=True)
    image = FilerImageField(
        verbose_name=_("Image"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="allergen_images",
    )

    class Meta:
        ordering = ["index", "name"]
        verbose_name = _("Allergen")
        verbose_name_plural = _("Allergens")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "allergen-detail", kwargs={"slug": _active_slug(self)}
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
