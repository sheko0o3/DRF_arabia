# Generated by Django 5.0.3 on 2024-03-11 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]