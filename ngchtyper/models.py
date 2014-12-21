from django.db import models

class ChineseEntry(models.Model):
    #  max 6 characters, no long phrases
    ch = models.CharField(max_length=24, db_index=True)
    chs = models.CharField(max_length=24, db_index=True)
    pinyin = models.CharField(max_length=80, db_index=True)

class ChineseEntryEnglish(models.Model):
    class Meta:
        ordering = ['order']

    chinese_entry = models.ForeignKey(ChineseEntry, related_name='definitions')
    order = models.IntegerField()
    definition = models.CharField(max_length=80)


class Document(models.Model):
    """
    Initially this will store simple JSON blobs. Some day it
    might store HTML or XML if that ever seems a good idea.
    """
    key = models.CharField(max_length=60, primary_key=True)
    type = models.CharField(max_length=12, choices=(('JSON', 'JSON'),))
    content = models.TextField()
