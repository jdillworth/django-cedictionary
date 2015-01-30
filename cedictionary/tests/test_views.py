# -*- coding: utf-8 -*-
from unittest import TestCase
from StringIO import StringIO
import gzip, os, tempfile, urllib

from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.test import Client

from .. import models

SAMPLE1 = """京味 京味 [jing1 wei4] /Beijing flavor/Beijing style/
敬畏 敬畏 [jing4 wei4] /to revere/
精微 精微 [jing1 wei1] /subtle/profound/
經緯 经纬 [jing1 wei3] /warp and woof/longitude and latitude/main points/"""


class TestEntrySearchViewCEDict(TestCase):
    def setUp(self):
        txt_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        txt_file.write(SAMPLE1)
        txt_file.close()

        try:
            call_command('cedictionary', txt_file.name)
        finally:
            os.remove(txt_file.name)

    def test_pinyin_searches_without_tones(self):

        c = Client()
        response = c.get(reverse('cedictionary.views.entry_search_view') +
                '?q=' + urllib.quote('jingwei'))

        self.assertEqual(4, len(response.context['cedict_entries']))

        # try it with spaces, should work the same
        response = c.get(reverse('cedictionary.views.entry_search_view') +
                '?q=' + urllib.quote('jing wei'))

        self.assertEqual(4, len(response.context['cedict_entries']))

    def test_chinese_traditional_finds_exact_entry(self):
        c = Client()
        response = c.get(reverse('cedictionary.views.entry_search_view') +
                '?q=' + urllib.quote('經緯'))

        self.assertEqual(1, len(response.context['cedict_entries']))
        self.assertEqual('jing1 wei3', response.context['cedict_entries'][0].pinyin)

    def test_chinese_simplified_finds_exact_entry(self):
        c = Client()
        response = c.get(reverse('cedictionary.views.entry_search_view') +
                '?q=' + urllib.quote('经纬'))

        self.assertEqual(1, len(response.context['cedict_entries']))
        self.assertEqual('jing1 wei3', response.context['cedict_entries'][0].pinyin)
