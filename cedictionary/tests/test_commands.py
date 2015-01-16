# -*- coding: utf-8 -*-

from django.core.management import call_command

from unittest import TestCase
from StringIO import StringIO
import gzip, os, tempfile

from .. import models

sample_cedict = """齡 龄 [ling2] /age/length of experience, membership etc/
齢 齢 [ling2] /Japanese variant of 齡|龄/
咬 咬 [yao3] /to bite/to nip/
齩 咬 [yao3] /variant of 咬[yao3]/
麵包房 面包房 [mian4 bao1 fang2] /bakery/CL:家[jia1]/
家 家 [jia1] /home/family/(polite) my (sister, uncle etc)/classifier for families or businesses/refers to the philosophical schools of pre-Han China/noun suffix for a specialist in some activity, such as a musician or revolutionary, corresponding to English -ist, -er, -ary or -ian/CL:個|个[ge4]/
鮎 鲇 [nian2] /sheatfish (Parasilurus asotus)/oriental catfish/see also 鯰|鲶[nian2]/
鯰 鲶 [nian2] /sheatfish (Parasilurus asotus)/oriental catfish/see also 鮎|鲇[nian2]/"""



class TestLoadCEDict(TestCase):
    def setUp(self):
        self.txt_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt')
        self.txt_file.write(sample_cedict)
        self.txt_file.close()

        self.gz_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt.gz')
        gz = gzip.GzipFile(fileobj=self.gz_file, mode='w')
        gz.write(sample_cedict)
        gz.close()
        self.gz_file.close()

    def tearDown(self):
        os.remove(self.txt_file.name)
        os.remove(self.gz_file.name)
        models.ChineseEntry.objects.all().delete()

    def test_entries_created(self):
        """
        Make sure we can load entries from a .txt file
        """
        call_command('cedictionary', self.txt_file.name)
        self.assertEqual(models.ChineseEntry.objects.count(), 8)

    def test_gz_entries_created(self):
        """
        Make sure we can load entries from a .txt.gz file
        """
        call_command('cedictionary', self.gz_file.name)
        self.assertEqual(models.ChineseEntry.objects.count(), 8)

    def test_variant_gets_defs(self):
        """
        An entry such as the first yao3, which only contains a variant note,
        should get definitions copied from its reference
        """
        call_command('cedictionary', self.txt_file.name)
        for entry in models.ChineseEntry.objects.filter(pinyin='yao3'):
            self.assertEqual(entry.definitions.count(), 2)

    def test_measure_word_reference(self):
        """
        Bakery should have 1 measure word reference
        """
        call_command('cedictionary', self.txt_file.name)
        bakery = models.ChineseEntry.objects.get(pinyin='mian4 bao1 fang2')
        self.assertEqual(bakery.measure_words.count(), 1)

    def test_multi_load_safe(self):
        call_command('cedictionary', self.txt_file.name)
        call_command('cedictionary', self.txt_file.name)
        self.assertEqual(models.ChineseEntry.objects.count(), 8)
