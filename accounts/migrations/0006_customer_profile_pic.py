# Generated by Django 3.1.7 on 2021-03-21 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210318_1552'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='user.png', null=True, upload_to=''),
        ),
    ]