# Generated by Django 2.0.3 on 2018-03-19 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0002_auto_20180318_1516'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.AddField(
            model_name='post',
            name='Tags',
            field=models.ManyToManyField(to='myblog.Tag'),
        ),
    ]