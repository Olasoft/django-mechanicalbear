# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Image'
        db.create_table(u'blog_image', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=10000, blank=True)),
            ('width', self.gf('django.db.models.fields.BigIntegerField')(blank=True)),
            ('height', self.gf('django.db.models.fields.BigIntegerField')(blank=True)),
        ))
        db.send_create_signal(u'blog', ['Image'])

        # Adding model 'Audio'
        db.create_table(u'blog_audio', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('artist', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('duration', self.gf('django.db.models.fields.BigIntegerField')()),
        ))
        db.send_create_signal(u'blog', ['Audio'])

        # Adding model 'Video'
        db.create_table(u'blog_video', (
            ('id', self.gf('django.db.models.fields.BigIntegerField')(primary_key=True)),
            ('oid', self.gf('django.db.models.fields.BigIntegerField')()),
            ('aid', self.gf('django.db.models.fields.BigIntegerField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('descr', self.gf('django.db.models.fields.TextField')(max_length=10000, blank=True)),
        ))
        db.send_create_signal(u'blog', ['Video'])

        # Adding model 'Post'
        db.create_table(u'blog_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=10000, blank=True)),
            ('deleted', self.gf('django.db.models.fields.NullBooleanField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal(u'blog', ['Post'])

        # Adding M2M table for field images on 'Post'
        m2m_table_name = db.shorten_name(u'blog_post_images')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'blog.post'], null=False)),
            ('image', models.ForeignKey(orm[u'blog.image'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'image_id'])

        # Adding M2M table for field audios on 'Post'
        m2m_table_name = db.shorten_name(u'blog_post_audios')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'blog.post'], null=False)),
            ('audio', models.ForeignKey(orm[u'blog.audio'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'audio_id'])

        # Adding M2M table for field videos on 'Post'
        m2m_table_name = db.shorten_name(u'blog_post_videos')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'blog.post'], null=False)),
            ('video', models.ForeignKey(orm[u'blog.video'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'video_id'])


    def backwards(self, orm):
        # Deleting model 'Image'
        db.delete_table(u'blog_image')

        # Deleting model 'Audio'
        db.delete_table(u'blog_audio')

        # Deleting model 'Video'
        db.delete_table(u'blog_video')

        # Deleting model 'Post'
        db.delete_table(u'blog_post')

        # Removing M2M table for field images on 'Post'
        db.delete_table(db.shorten_name(u'blog_post_images'))

        # Removing M2M table for field audios on 'Post'
        db.delete_table(db.shorten_name(u'blog_post_audios'))

        # Removing M2M table for field videos on 'Post'
        db.delete_table(db.shorten_name(u'blog_post_videos'))


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