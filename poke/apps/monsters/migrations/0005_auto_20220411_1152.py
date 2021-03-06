# Generated by Django 3.2.12 on 2022-04-11 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monsters', '0004_alter_move_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='helditem',
            name='image',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='helditem',
            name='api_url',
            field=models.URLField(editable=False),
        ),
        migrations.AlterField(
            model_name='move',
            name='api_url',
            field=models.URLField(editable=False),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='api_url',
            field=models.URLField(editable=False),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='held_items',
            field=models.ManyToManyField(editable=False, to='monsters.HeldItem'),
        ),
        migrations.AlterField(
            model_name='pokemon',
            name='json',
            field=models.JSONField(editable=False, null=True),
        ),
    ]
