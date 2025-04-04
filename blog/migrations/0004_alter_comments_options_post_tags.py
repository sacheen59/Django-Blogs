# Generated by Django 5.1.7 on 2025-03-31 12:56

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comments'),
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'ordering': ['created'], 'verbose_name': 'Comment'},
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
