# Generated by Django 2.2.2 on 2019-06-19 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0006_auto_20190619_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marker',
            name='stat_number',
            field=models.IntegerField(unique=True, verbose_name='Station ID'),
        ),
    ]