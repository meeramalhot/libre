# Generated by Django 5.1.5 on 2025-04-13 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pages',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
