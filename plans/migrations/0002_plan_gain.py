# Generated by Django 5.1.4 on 2024-12-26 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='gain',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
