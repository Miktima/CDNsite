# Generated by Django 4.1.5 on 2023-02-02 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cash_settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('url_auth', models.CharField(max_length=200)),
                ('url_status', models.CharField(max_length=200)),
                ('url_request', models.CharField(max_length=200)),
            ],
        ),
    ]
