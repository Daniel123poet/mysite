# Generated by Django 2.0.3 on 2020-05-17 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0005_auto_20200302_1535'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['comment_time']},
        ),
    ]
