# Generated by Django 2.2.7 on 2019-11-11 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('daphne_context', '0007_auto_20191111_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExperimentContext',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_running', models.BooleanField()),
                ('experiment_id', models.IntegerField()),
                ('current_state', models.TextField()),
                ('user_information', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='daphne_context.UserInformation')),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('end_state', models.TextField()),
                ('experimentcontext', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiment.ExperimentContext')),
            ],
        ),
        migrations.CreateModel(
            name='ExperimentAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.TextField()),
                ('date', models.DateTimeField()),
                ('experimentstage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='experiment.ExperimentStage')),
            ],
        ),
        migrations.CreateModel(
            name='AllowedCommand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('command_type', models.CharField(choices=[('engineer', 'Engineer Commands'), ('analyst', 'iFEED Commands'), ('explorer', 'Explorer Commands'), ('historian', 'Historian Commands'), ('critic', 'Critic Commands'), ('engineer_instruments', 'Instruments Cheatsheet'), ('engineer_instrument_parameters', 'Instrument Parameters Cheatsheet'), ('engineer_measurements', 'Measurements Cheatsheet'), ('engineer_stakeholders', 'Stakeholders Cheatsheet'), ('engineer_objectives', 'Objectives Cheatsheet'), ('engineer_subobjectives', 'Subobjectives Cheatsheet'), ('historian_measurements', 'Historical Measurements Cheatsheet'), ('historian_missions', 'Historical Missions Cheatsheet'), ('historian_technologies', 'Historical Technologies Cheatsheet'), ('historian_space_agencies', 'Space Agencies Cheatsheet')], max_length=40)),
                ('command_descriptor', models.IntegerField()),
                ('user_information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='daphne_context.UserInformation')),
            ],
        ),
    ]
