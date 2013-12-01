# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Video.aid'
        db.delete_column(u'blog_video', 'aid')

        # Adding field 'Video.player'
        db.add_column(u'blog_video', 'player',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=1000, blank=True),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Video.aid'
        raise RuntimeError("Cannot reverse this migration. 'Video.aid' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Video.aid'
        db.add_column(u'blog_video', 'aid',
                      self.gf('django.db.models.fields.BigIntegerField')(),
                      keep_default=False)

        # Deleting field 'Video.player'
        db.delete_column(u'blog_video', 'player')


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
            'descr': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'blank': 'True'}),
            'id': ('django.db.models.fields.BigIntegerField', [], {'primary_key': 'True'}),
            'oid': ('django.db.models.fields.BigIntegerField', [], {}),
            'player': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['blog']