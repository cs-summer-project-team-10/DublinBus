# Generated by Django 2.2.2 on 2019-07-08 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusStop',
            fields=[
                ('stop_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='Stop ID')),
                ('stop_name', models.CharField(max_length=200, verbose_name='Bus Station Name')),
                ('lat', models.FloatField(null=True, verbose_name='Latitude')),
                ('lng', models.FloatField(null=True, verbose_name='Longitude')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('route_id', models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='Route ID')),
                ('end_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='End_Stop_ID', to='map.BusStop', verbose_name='End Stop ID')),
                ('start_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Start_Stop_ID', to='map.BusStop', verbose_name='Start Stop ID')),
            ],
        ),
        migrations.CreateModel(
            name='RouteStops',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_id', models.CharField(max_length=50, verbose_name='Line ID')),
                ('stop_order', models.IntegerField(verbose_name='Stop Order')),
                ('route_id', models.ForeignKey(db_column='route_id', on_delete=django.db.models.deletion.CASCADE, to='map.Route', verbose_name='Route ID')),
                ('stop_id', models.ForeignKey(db_column='stop_id', on_delete=django.db.models.deletion.CASCADE, to='map.BusStop', verbose_name='Stop ID')),
            ],
            options={
                'unique_together': {('route_id', 'stop_id')},
            },
        ),
    ]
