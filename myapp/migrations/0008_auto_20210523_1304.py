# Generated by Django 3.1.7 on 2021-05-23 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_layout_page_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='layout',
            name='page_title',
        ),
        migrations.AddField(
            model_name='seo',
            name='page_title',
            field=models.CharField(default=1, max_length=25, verbose_name='ページタイトル'),
            preserve_default=False,
        ),
    ]
