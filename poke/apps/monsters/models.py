from django.db import models
from django.urls import reverse


class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, null=True, auto_now=True)

    class Meta:
        abstract = True
        ordering = ['pk']


class HeldItem(Timestamped):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    cost = models.PositiveIntegerField(null=True)
    fling_power = models.PositiveIntegerField(null=True)
    image = models.URLField(null=True)

    api_url = models.URLField(editable=False)

    def __str__(self):
        return f'Item {self.name}#{self.pk}'


class Move(Timestamped):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    effect = models.TextField(null=True)
    short_effect = models.CharField(max_length=500, null=True)
    accuracy = models.PositiveIntegerField(null=True)
    power = models.PositiveIntegerField(null=True)
    pp = models.PositiveIntegerField(null=True)
    priority = models.IntegerField(null=True)

    api_url = models.URLField(editable=False)

    def __str__(self):
        return f'Move {self.name}#{self.pk} '


class Pokemon(Timestamped):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    order = models.IntegerField(null=True)
    base_experience = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)
    weight = models.PositiveIntegerField(null=True)

    avatar = models.URLField(null=True)

    # Many2Many
    moves = models.ManyToManyField(Move)
    held_items = models.ManyToManyField(HeldItem, editable=False)

    # end M2M

    api_url = models.URLField(editable=False)
    json = models.JSONField(null=True, editable=False)

    def __str__(self):
        return f'{self.name} #{self.pk}'

    def get_absolute_url(self):
        return reverse('monsters-detail', kwargs={'pk': self.pk})
