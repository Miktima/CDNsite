# Generated by Django 4.1.5 on 2023-02-01 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('traffic_metric', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Granularity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nsec', models.IntegerField(verbose_name='number of seconds')),
                ('code', models.CharField(max_length=50)),
            ],
        ),
    ]
