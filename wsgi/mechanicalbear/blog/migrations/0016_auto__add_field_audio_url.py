# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Audio.url'
        db.add_column('blog_audio', 'url',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1000, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Audio.url'
        db.delete_column('blog_audio', 'url')


    models = {
        'blog.audio': {
            'Meta': {'object_name': 'Audio'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'duration': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'radio': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'})
        },
        'blog.image': {
            'Meta': {'object_name': 'Image'},
            'height': ('django.db.models.fields.BigIntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'blank': 'True'}),
            'width': ('django.db.models.fields.BigIntegerField', [], {'blank': 'True'})
        },
        'blog.post': {
            'Meta': {'object_name': 'Post'},
            'audios': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blog.Audio']", 'symmetrical': 'False', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blog.Image']", 'symmetrical': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blog.Tag']", 'symmetrical': 'False', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blog.Video']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'blog.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True'})
        },
        'blog.video': {
            'Meta': {'object_name': 'Video'},
            'descr': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'blank': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'oid': ('django.db.models.fields.BigIntegerField', [], {}),
            'player': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['blog']