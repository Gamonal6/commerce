# Generated by Django 4.0.3 on 2022-05-16 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_rename_owner_auctions_owner_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auctions',
            old_name='owner_id',
            new_name='owner',
        ),
    ]