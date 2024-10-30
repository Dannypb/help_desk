# Generated by Django 5.1.2 on 2024-10-28 22:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_occupation_alter_client_contact_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agent',
            name='occupation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.occupation'),
        ),
        migrations.AlterField(
            model_name='client',
            name='contact_phone',
            field=models.CharField(blank=True, max_length=9, null=True, unique=True),
        ),
    ]