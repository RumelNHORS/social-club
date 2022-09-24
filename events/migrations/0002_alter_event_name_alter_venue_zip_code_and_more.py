# Generated by Django 4.1 on 2022-09-15 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=120, verbose_name='Event Name'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='Zip_code',
            field=models.CharField(blank=True, max_length=10, verbose_name='Zip Code'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='web',
            field=models.URLField(blank=True, verbose_name='Website Address'),
        ),
    ]