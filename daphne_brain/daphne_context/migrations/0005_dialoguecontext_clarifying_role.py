# Generated by Django 2.1.12 on 2019-10-05 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daphne_context', '0004_dialoguecontext_clarifying_commands'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialoguecontext',
            name='clarifying_role',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
