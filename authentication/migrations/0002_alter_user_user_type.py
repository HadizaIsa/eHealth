# Generated by Django 4.2.4 on 2023-08-25 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('HEALTH_WORKER', 'health_worker'), ('PATIENT', 'patient')], default='PATIENT', max_length=15),
        ),
    ]
