# Generated by Django 4.1.7 on 2023-05-17 08:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0017_remove_scan_url_scandetail_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="scan",
            name="auth_detail",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="scan",
            name="auth_type",
            field=models.CharField(default="None", max_length=150),
            preserve_default=False,
        ),
    ]
