# Generated by Django 3.1.4 on 2021-01-11 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affiliation', '0005_auto_20201228_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='don_bam',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='don_mand',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='don_maya',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='don_zou',
            field=models.BooleanField(default=False, null=True),
        ),
    ]