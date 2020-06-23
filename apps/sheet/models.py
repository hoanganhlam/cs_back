from django.db import models
from base import interface
from django.contrib.postgres.fields import JSONField, ArrayField
from django.contrib.auth.models import User
from apps.general.models import HashTag
from utils.slug import unique_slugify
from apps.media.models import Media
from django.utils import timezone


# Create your models here.


class CheatSheet(interface.BaseModel):
    title = models.CharField(max_length=120)
    slug = models.CharField(max_length=120, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    settings = JSONField(null=True, blank=True)
    sheets = ArrayField(JSONField(null=True, blank=True), null=True, blank=True)
    user = models.ForeignKey(User, related_name="cheat_sheets", on_delete=models.CASCADE)
    taxonomies = models.ManyToManyField(HashTag, related_name="cheat_sheets", blank=True)
    is_public = models.BooleanField(default=False)
    media = models.ForeignKey(Media, related_name="cheat_sheets", null=True, blank=True, on_delete=models.SET_NULL)
    date_published = models.DateTimeField(default=timezone.now)

    def save(self, **kwargs):
        # generate unique slug
        if hasattr(self, 'slug') and self.slug is None or self.slug == '':
            unique_slugify(self, self.title)
        super(CheatSheet, self).save(**kwargs)
