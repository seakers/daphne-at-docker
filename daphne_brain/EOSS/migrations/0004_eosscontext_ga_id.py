# Generated by Django 2.2.7 on 2019-11-17 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EOSS', '0003_auto_20191005_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='eosscontext',
            name='ga_id',
            field=models.TextField(null=True),
        ),
    ]
