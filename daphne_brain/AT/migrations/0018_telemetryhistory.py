# Generated manually for TelemetryHistory model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('daphne_context', '0001_initial'),
        ('AT', '0017_atcontext_seen_tutorial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelemetryHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('telemetry_data', models.JSONField()),
                ('source', models.CharField(default='Hera', max_length=50)),
                ('session_id', models.CharField(blank=True, max_length=100, null=True)),
                ('metadata', models.JSONField(blank=True, default=dict)),
                ('user_information', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='daphne_context.userinformation')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddIndex(
            model_name='telemetryhistory',
            index=models.Index(fields=['timestamp'], name='AT_telemetr_timesta_3ae4ba_idx'),
        ),
        migrations.AddIndex(
            model_name='telemetryhistory',
            index=models.Index(fields=['source', 'timestamp'], name='AT_telemetr_source_31fc75_idx'),
        ),
        migrations.AddIndex(
            model_name='telemetryhistory',
            index=models.Index(fields=['session_id', 'timestamp'], name='AT_telemetr_session_499ae1_idx'),
        ),
    ]
