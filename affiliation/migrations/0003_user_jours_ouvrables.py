# Generated by Django 3.1.7 on 2021-03-22 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliation', '0002_remove_user_jours_ouvrable'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='jours_ouvrables',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
