# Generated by Django 4.0.3 on 2022-04-11 05:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maid', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maidworkdetails',
            name='customer_user',
        ),
    ]