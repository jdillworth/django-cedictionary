# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ChineseEntry'
        db.create_table(u'ngchtyper_chineseentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ch', self.gf('django.db.models.fields.CharField')(max_length=24, db_index=True)),
            ('chs', self.gf('django.db.models.fields.CharField')(max_length=24, db_index=True)),
            ('pinyin', self.gf('django.db.models.fields.CharField')(max_length=80, db_index=True)),
        ))
        db.send_create_signal(u'ngchtyper', ['ChineseEntry'])

        # Adding model 'ChineseEntryEnglish'
        db.create_table(u'ngchtyper_chineseentryenglish', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chinese_entry', self.gf('django.db.models.fields.related.ForeignKey')(related_name='definitions', to=orm['ngchtyper.ChineseEntry'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal(u'ngchtyper', ['ChineseEntryEnglish'])

        # Adding model 'Document'
        db.create_table(u'ngchtyper_document', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=60, primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'ngchtyper', ['Document'])


    def backwards(self, orm):
        # Deleting model 'ChineseEntry'
        db.delete_table(u'ngchtyper_chineseentry')

        # Deleting model 'ChineseEntryEnglish'
        db.delete_table(u'ngchtyper_chineseentryenglish')

        # Deleting model 'Document'
        db.delete_table(u'ngchtyper_document')


    models = {
        u'ngchtyper.chineseentry': {
            'Meta': {'object_name': 'ChineseEntry'},
            'ch': ('django.db.models.fields.CharField', [], {'max_length': '24', 'db_index': 'True'}),
            'chs': ('django.db.models.fields.CharField', [], {'max_length': '24', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pinyin': ('django.db.models.fields.CharField', [], {'max_length': '80', 'db_index': 'True'})
        },
        u'ngchtyper.chineseentryenglish': {
            'Meta': {'ordering': "['order']", 'object_name': 'ChineseEntryEnglish'},
            'chinese_entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'definitions'", 'to': u"orm['ngchtyper.ChineseEntry']"}),
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        u'ngchtyper.document': {
            'Meta': {'object_name': 'Document'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '60', 'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['ngchtyper']