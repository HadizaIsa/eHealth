# Generated by Django 4.2.4 on 2023-08-27 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='decision',
            field=models.CharField(blank=True, choices=[('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected')], max_length=10, null=True),
        ),
    ]