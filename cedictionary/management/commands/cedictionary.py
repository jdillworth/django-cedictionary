from __future__ import print_function, division

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import cedict

from optparse import make_option
import os, gzip, re, hashlib

from ... import models

class Command(BaseCommand):
    args = 'cedict-file'
    help = 'cc-cedict loader for cedictionary'

    @transaction.atomic
    def handle(self, *args, **options):
        if len(args) != 1:
            print('Usage:\n\n\tmanage.py cedictionary cedict-file|cedict-gz-file\n')
            return

        fname = args[0]
        if not os.path.isfile(fname):
            print(fname, 'is not a file')
            return

        if fname[-3:].lower() == '.gz':
            f = gzip.open(fname)
        else:
            f = open(fname)

        try:
            all_entries = set((e.ch, e.chs, e.pinyin)
                    for e in models.ChineseEntry.objects.all())
            batch = []

            # First pass, create the basic dictionary entries (no definitions)
            for ch, chs, pinyin, defs, variants, mw in cedict.iter_cedict(f):

                # skip dupes
                if (ch, chs, pinyin) in all_entries:
                    continue

                all_entries.add((ch, chs, pinyin))
                batch.append(models.ChineseEntry(ch=ch, chs=chs, pinyin=pinyin))

                if len(batch) == 2000:
                    models.ChineseEntry.objects.bulk_create(batch)
                    batch = []

            if len(batch) > 0:
                models.ChineseEntry.objects.bulk_create(batch)


            # second pass, load english definitions (unless they're dupes)
            f.seek(0)
            batch = []
            all_entries = dict(((e.ch, e.chs, e.pinyin), e.pk)
                    for e in models.ChineseEntry.objects.all())
            defs_by_entry = {}
            for english in models.ChineseEntryEnglish.objects.all():
                defs_by_entry.setdefault(
                        english.chinese_entry_id, set()
                    ).add(english.definition)

            for ch, chs, pinyin, defs, variants, mw in cedict.iter_cedict(f):
                entry = models.ChineseEntry.objects.get(
                        pk=all_entries[(ch, chs, pinyin)])

                defs_already = defs_by_entry.setdefault(entry.pk, set())
                for d in defs:
                    if d not in defs_already:
                        defs_already.add(d)
                        batch.append(models.ChineseEntryEnglish(
                            chinese_entry=entry,
                            order=len(defs_already),
                            definition=d
                        ))

                if len(batch) >= 2000:
                    models.ChineseEntryEnglish.objects.bulk_create(batch)
                    batch = []

            if len(batch) > 0:
                models.ChineseEntryEnglish.objects.bulk_create(batch)


            # Third pass, connect variants and measure words
            f.seek(0)
            batch = []
            for ch, chs, pinyin, defs, variants, mw in cedict.iter_cedict(f):

                # we only care about variants and measure words on this pass
                if not (variants or mw):
                    continue

                entry = models.ChineseEntry.objects.get(
                        ch=ch, chs=chs, pinyin=pinyin)

                defs_count = entry.definitions.count()

                # setup variant records
                for variant in variants:
                    # ch, chs, py, vartype

                    try:
                        q = {'ch':variant['ch']}

                        if variant.get('py'):
                            q['pinyin'] = variant['py']
                        if variant.get('chs'):
                            q['chs'] = variant['chs']

                        var_entry = models.ChineseEntry.objects.get(**q)
                    except models.ChineseEntry.DoesNotExist:
                        continue
                    except models.ChineseEntry.MultipleObjectsReturned:
                        continue

                    # if it's a variant with no defs, copy defs from the entry it's
                    # a variant of
                    if defs_count == 0 and var_entry.definitions.count() > 0:
                        for df in var_entry.definitions.all():
                            entry.definitions.create(
                                    definition=df.definition, order=defs_count+1)
                            defs_count += 1

                    if entry.variants.filter(pk=var_entry.pk).count() == 0:
                        v = models.Variant.objects.create(
                                entry=entry, variant=var_entry,
                                note=variant.get('vartype') or '')


                # setup measure word entries and link to them
                for ch, chs, pinyin in mw:
                    try:
                        q = {'ch':ch, 'chs':chs}
                        if pinyin:
                            q['pinyin'] = pinyin
                        mw_entry = models.ChineseEntry.objects.get(**q)
                    except models.ChineseEntry.DoesNotExist:
                        continue
                    except models.ChineseEntry.MultipleObjectsReturned:
                        continue

                    if entry.measure_words.filter(pk=mw_entry.pk).count() == 0:
                        # TODO: do I really need the above logic check?
                        entry.measure_words.add(mw_entry)
        finally:
            f.close()
