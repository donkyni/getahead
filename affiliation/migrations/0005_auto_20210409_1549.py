# Generated by Django 3.1.7 on 2021-04-09 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliation', '0004_auto_20210409_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='modules',
            name='texte11',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier pdf'),
        ),
        migrations.AddField(
            model_name='modules',
            name='texte12',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier pdf'),
        ),
        migrations.AddField(
            model_name='modules',
            name='texte13',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier pdf'),
        ),
        migrations.AddField(
            model_name='modules',
            name='texte14',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier pdf'),
        ),
        migrations.AddField(
            model_name='modules',
            name='texte15',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Intitulé du fichier pdf'),
        ),
    ]
