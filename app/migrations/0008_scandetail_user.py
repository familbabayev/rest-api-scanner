# Generated by Django 4.1.7 on 2023-05-13 17:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0007_scan_vulnerabilities"),
    ]

    operations = [
        migrations.AddField(
            model_name="scandetail",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
