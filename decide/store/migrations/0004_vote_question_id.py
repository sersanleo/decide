# Generated by Django 2.0 on 2020-12-26 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20180921_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='question_id',
            field=models.CharField(default='1', max_length=140),
        ),
    ]