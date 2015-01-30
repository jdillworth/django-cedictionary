# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ChineseEntry.pinyin_letters'
        db.add_column(u'cedictionary_chineseentry', 'pinyin_letters',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=160, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ChineseEntry.pinyin_letters'
        db.delete_column(u'cedictionary_chineseentry', 'pinyin_letters')


    models = {
        u'cedictionary.chineseentry': {
            'Meta': {'object_name': 'ChineseEntry'},
            'ch': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            'chs': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure_words': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'measure_word_for'", 'symmetrical': 'False', 'to': u"orm['cedictionary.ChineseEntry']"}),
            'pinyin': ('django.db.models.fields.CharField', [], {'max_length': '160', 'db_index': 'True'}),
            'pinyin_letters': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '160', 'db_index': 'True'}),
            'variants': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['cedictionary.ChineseEntry']", 'through': u"orm['cedictionary.Variant']", 'symmetrical': 'False'})
        },
        u'cedictionary.chineseentryenglish': {
            'Meta': {'ordering': "['order']", 'object_name': 'ChineseEntryEnglish'},
            'chinese_entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'definitions'", 'to': u"orm['cedictionary.ChineseEntry']"}),
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '600'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        },
        u'cedictionary.variant': {
            'Meta': {'unique_together': "(('entry', 'variant'),)", 'object_name': 'Variant'},
            'entry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cedictionary.ChineseEntry']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'variant': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'variant_of'", 'to': u"orm['cedictionary.ChineseEntry']"})
        }
    }

    complete_apps = ['cedictionary']