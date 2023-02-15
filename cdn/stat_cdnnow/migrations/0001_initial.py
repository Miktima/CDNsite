# Generated by Django 4.1.5 on 2023-01-26 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Portals_stat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portal', models.CharField(max_length=200)),
                ('id_portal', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Stat_settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('cliend_id', models.CharField(max_length=200)),
                ('url_stat', models.CharField(max_length=200)),
                ('url_auth', models.CharField(max_length=200)),
            ],
        ),
    ]