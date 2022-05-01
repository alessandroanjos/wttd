from django.db import models
from django.shortcuts import resolve_url as resolve
# Create your models here.


class Speaker(models.Model):
    name = models.CharField('Nome', max_length=255)
    slug = models.SlugField('slug')
    photo = models.URLField('foto')
    website = models.URLField('website', blank=True)
    description = models.TextField('descrição', blank=True)

    class Meta:
        verbose_name = 'Palestrante'
        verbose_name_plural = 'Palestrantes'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return resolve('speaker_detail', slug=self.slug)
