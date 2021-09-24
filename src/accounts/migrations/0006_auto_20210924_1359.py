# Generated by Django 3.2.7 on 2021-09-24 13:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210924_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('5073566d-1864-449e-a544-f1fe716ce697'), editable=False, primary_key=True, serialize=False),
        ),
    ]
