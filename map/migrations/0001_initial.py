# Generated by Django 2.2.2 on 2019-07-02 16:24

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
                ('stat_number', models.IntegerField(primary_key=True, serialize=False, verbose_name='Station ID')),
                ('name', models.CharField(max_length=200, verbose_name='Bus Station Name')),
                ('lat', models.FloatField(null=True, verbose_name='Latitude')),
                ('lng', models.FloatField(null=True, verbose_name='Longitude')),
            ],
        ),
        migrations.CreateModel(
            name='Routes',
            fields=[
                ('routeID', models.IntegerField(primary_key=True, serialize=False, verbose_name='Route ID')),
                ('routeName', models.CharField(max_length=50, unique=True, verbose_name='Route Name')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('DataSource', models.CharField(max_length=50, verbose_name='Unique Bus Operator Code')),
                ('DayOfService', models.CharField(max_length=100, verbose_name='Day of service,One day of service could last more than 24 hours')),
                ('TripID', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Unique trip code')),
                ('RouteID', models.CharField(max_length=50, verbose_name='Unique route code')),
                ('Direction', models.CharField(max_length=10, verbose_name='Route direction:IB or OB')),
                ('PlannedTime_Dep', models.IntegerField(verbose_name='Planned departure time of the trip, in seconds')),
                ('PlannedTime_Arr', models.IntegerField(verbose_name='Planned arrival time of the trip, in seconds')),
                ('Basin', models.CharField(max_length=50, verbose_name='Basin code')),
                ('TenderLot', models.CharField(max_length=50, verbose_name='Tender lot')),
                ('ActualTime_Dep', models.CharField(max_length=50, verbose_name='Actual departure time of the trip, in seconds')),
                ('ActualTime_Arr', models.CharField(max_length=50, verbose_name='Actual arrival time of the trip, in seconds')),
                ('Suppressed', models.IntegerField(verbose_name='The whole trip has been suppressed (0 =achieved, 1 = suppressed)')),
                ('JustificationID', models.IntegerField(verbose_name='Fault code')),
                ('LastUpdate', models.CharField(max_length=100, verbose_name='Time of the last record update')),
                ('Note', models.CharField(max_length=255, verbose_name='Free note')),
                ('LineID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.Routes', to_field='routeName')),
            ],
        ),
        migrations.CreateModel(
            name='RouteStops',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop_order', models.IntegerField(verbose_name='Route Name')),
                ('routeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.Routes')),
                ('stopID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='map.BusStop')),
            ],
        ),
    ]
