# Generated by Django 3.1.1 on 2020-11-19 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliation', '0004_auto_20201116_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payement',
            name='etat',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
    ]
