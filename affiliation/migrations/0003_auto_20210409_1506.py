# Generated by Django 3.1.7 on 2021-04-09 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliation', '0002_auto_20210323_1128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='modules',
            options={'ordering': ('id',), 'verbose_name': 'Module', 'verbose_name_plural': 'Modules'},
        ),
        migrations.AddField(
            model_name='modules',
            name='pdf1',
            field=models.FileField(blank=True, null=True, upload_to='wara/%y %m %d', verbose_name='Fichier pdf 1'),
        ),
        migrations.AddField(
            model_name='modules',
            name='pdf2',
            field=models.FileField(blank=True, null=True, upload_to='wara/%y %m %d', verbose_name='Fichier pdf 2'),
        ),
        migrations.AddField(
            model_name='modules',
            name='pdf3',
            field=models.FileField(blank=True, null=True, upload_to='wara/%y %m %d', verbose_name='Fichier pdf 3'),
        ),
    ]
