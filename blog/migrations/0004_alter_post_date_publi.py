# Generated by Django 4.1.7 on 2023-08-21 14:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_post_date_publi'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date_publi',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 21, 14, 35, 16, 465632, tzinfo=datetime.timezone.utc)),
        ),
    ]
