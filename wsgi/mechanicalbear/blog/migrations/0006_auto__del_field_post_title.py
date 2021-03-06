# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Post.title'
        db.delete_column(u'blog_post', 'title')


    def backwards(self, orm):
        # Adding field 'Post.title'
        db.add_column(u'blog_post', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1000, blank=True),
                      keep_default=False)


    models = {
        u'blog.audio': {
            'Meta': {'object_name': 'Audio'},
            'artist': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'duration': ('django.db.models.fields.BigIntegerField', [], {}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'blog.image': {
            'Meta': {'object_name': 'Image'},
            'height': ('django.db.models.fields.BigIntegerField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'blank': 'True'}),
            'width': ('django.db.models.fields.BigIntegerField', [], {'blank': 'True'})
        },
        u'blog.post': {
            'Meta': {'object_name': 'Post'},
            'audios': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blog.Audio']", 'symmetrical': 'False', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'blank': 'True'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.NullBooleanField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blog.Image']", 'symmetrical': 'False', 'blank': 'True'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['blog.Video']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'blog.video': {
            'Meta': {'object_name': 'Video'},
            'aid': ('django.db.models.fields.BigIntegerField', [], {}),
            'descr': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'blank': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'oid': ('django.db.models.fields.BigIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['blog']