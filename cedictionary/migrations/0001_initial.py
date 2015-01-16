# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ChineseEntry'
        db.create_table(u'cedictionary_chineseentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ch', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('chs', self.gf('django.db.models.fields.CharField')(max_length=64, db_index=True)),
            ('pinyin', self.gf('django.db.models.fields.CharField')(max_length=120, db_index=True)),
        ))
        db.send_create_signal(u'cedictionary', ['ChineseEntry'])

        # Adding M2M table for field measure_words on 'ChineseEntry'
        m2m_table_name = db.shorten_name(u'cedictionary_chineseentry_measure_words')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_chineseentry', models.ForeignKey(orm[u'cedictionary.chineseentry'], null=False)),
            ('to_chineseentry', models.ForeignKey(orm[u'cedictionary.chineseentry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_chineseentry_id', 'to_chineseentry_id'])

        # Adding model 'Variant'
        db.create_table(u'cedictionary_variant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cedictionary.ChineseEntry'])),
            ('variant', self.gf('django.db.models.fields.related.ForeignKey')(related_name='variant_of', to=orm['cedictionary.ChineseEntry'])),
            ('note', self.gf('django.db.models.fields.CharField')(max_length=80, blank=True)),
        ))
        db.send_create_signal(u'cedictionary', ['Variant'])

        # Adding unique constraint on 'Variant', fields ['entry', 'variant']
        db.create_unique(u'cedictionary_variant', ['entry_id', 'variant_id'])

        # Adding model 'ChineseEntryEnglish'
        db.create_table(u'cedictionary_chineseentryenglish', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('chinese_entry', self.gf('django.db.models.fields.related.ForeignKey')(related_name='definitions', to=orm['cedictionary.ChineseEntry'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'cedictionary', ['ChineseEntryEnglish'])


    def backwards(self, orm):
        # Removing unique constraint on 'Variant', fields ['entry', 'variant']
        db.delete_unique(u'cedictionary_variant', ['entry_id', 'variant_id'])

        # Deleting model 'ChineseEntry'
        db.delete_table(u'cedictionary_chineseentry')

        # Removing M2M table for field measure_words on 'ChineseEntry'
        db.delete_table(db.shorten_name(u'cedictionary_chineseentry_measure_words'))

        # Deleting model 'Variant'
        db.delete_table(u'cedictionary_variant')

        # Deleting model 'ChineseEntryEnglish'
        db.delete_table(u'cedictionary_chineseentryenglish')


    models = {
        u'cedictionary.chineseentry': {
            'Meta': {'object_name': 'ChineseEntry'},
            'ch': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'chs': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measure_words': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'measure_word_for'", 'symmetrical': 'False', 'to': u"orm['cedictionary.ChineseEntry']"}),
            'pinyin': ('django.db.models.fields.CharField', [], {'max_length': '120', 'db_index': 'True'}),
            'variants': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['cedictionary.ChineseEntry']", 'through': u"orm['cedictionary.Variant']", 'symmetrical': 'False'})
        },
        u'cedictionary.chineseentryenglish': {
            'Meta': {'ordering': "['order']", 'object_name': 'ChineseEntryEnglish'},
            'chinese_entry': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'definitions'", 'to': u"orm['cedictionary.ChineseEntry']"}),
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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