# Generated by Django 2.2.2 on 2019-06-18 14:36

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20190618_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='thumbnail',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='post_images/'),
        ),
    ]
