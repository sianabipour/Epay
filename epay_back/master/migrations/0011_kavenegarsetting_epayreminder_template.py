# Generated by Django 3.2.10 on 2022-05-23 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0010_auto_20220523_0356'),
    ]

    operations = [
        migrations.AddField(
            model_name='kavenegarsetting',
            name='EpayReminder_template',
            field=models.CharField(max_length=50, null=True),
        ),
    ]