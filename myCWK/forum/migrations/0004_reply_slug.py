# Generated by Django 5.1.5 on 2025-02-22 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_reply_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='slug',
            field=models.SlugField(blank=True, max_length=400, unique=True),
        ),
    ]
