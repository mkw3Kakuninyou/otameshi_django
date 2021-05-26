# Generated by Django 3.1.7 on 2021-05-15 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_post_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='BBS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bbscontent', models.TextField(max_length=50, verbose_name='掲示板')),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(max_length=10000, verbose_name='内容'),
        ),
    ]
