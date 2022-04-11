from django.contrib import admin
from django.utils.html import mark_safe

from poke.apps.monsters.models import Pokemon, Move, HeldItem


@admin.register(HeldItem)
class HeldItemAdmin(admin.ModelAdmin):
    list_display = ('_img', 'pk', 'name', 'cost', 'fling_power')
    search_fields = ('name', )
    list_display_links = ('_img', 'pk', 'name')

    def _img(self, obj):
        return mark_safe(f'<img src="{obj.image}" width="75" />')


@admin.register(Move)
class MoveAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'pp', 'power', 'priority', 'accuracy')
    search_fields = ('name',)
    list_display_links = ('pk', 'name')


@admin.register(Pokemon)
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('_avatar', 'pk', 'name', 'order', 'height', 'weight')
    search_fields = ('name', )
    readonly_fields = ('avatar', )
    ordering = ('pk',)
    list_display_links = ('_avatar', 'pk', 'name')

    def _avatar(self, obj):
        img = obj.avatar or 'https://pokeapi.co/pokeapi_192_square.png'
        return mark_safe(f'<img src="{img}" width="75" />')


