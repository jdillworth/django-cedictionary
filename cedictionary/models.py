import re

from django.db import models


class ChineseEntry(models.Model):
    #  max 6 characters, no long phrases
    ch = models.CharField(max_length=100, db_index=True)
    chs = models.CharField(max_length=100, db_index=True)
    pinyin = models.CharField(max_length=160, db_index=True)
    pinyin_letters = models.CharField(max_length=160, editable=False,
            db_index=True, default='')
    variants = models.ManyToManyField(
            'self', symmetrical=False, through='Variant')
    measure_words = models.ManyToManyField(
            'self', symmetrical=False, related_name='measure_word_for')

    def init_pinyin_letters(self):
        self.pinyin_letters = re.sub(r'[^A-Za-z]', '', self.pinyin)

    def save(self, *args, **kwargs):
        self.init_pinyin_letters()
        super(ChineseEntry, self).save(*args, **kwargs)

class Variant(models.Model):
    class Meta:
        unique_together = (('entry', 'variant'),)
    entry = models.ForeignKey(ChineseEntry)
    variant = models.ForeignKey(ChineseEntry, related_name='variant_of')
    note = models.CharField(max_length=80, blank=True)

class ChineseEntryEnglish(models.Model):
    class Meta:
        ordering = ['order']

    chinese_entry = models.ForeignKey(ChineseEntry, related_name='definitions')
    order = models.IntegerField()
    definition = models.CharField(max_length=600)
