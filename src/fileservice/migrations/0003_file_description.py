# Generated by Django 3.2.7 on 2021-11-03 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileservice', '0002_create'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
