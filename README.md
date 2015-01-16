Note: This modules is alpha and not yet fully functional. It has models
and a management command to load data, but has no views, templates or admin.

# django-cedictionary

A Django app that provides a basic Chinese-English dictionary lookup. That is,
you can enter Chinese characters or pinyin pronunciation and see matching
entries.

It can also do a full-text search against the English side of a Chinese-English
dictionary, but the quality of these results will be low (for now).

# Installation

Install the package with pip.

  pip install django-cedictionary

Add the "cedictionary" to your INSTALLED_APPS setting.

If you're using South, run "manage.py migrate cedictionary".

If you're not using South, run "manage.py syncdb".

# Loading cedict

You'll need to download the [CC-CEDICT](http://cc-cedict.org/wiki/) then
run the following management command.

  ./manage.py cedictionary cedict_1_0_ts_utf-8_mdbg.txt.gz

Note that on a fairly recent MacBook pro running Python 2.7.8, this takes
3-4 minutes and peaks at about 300MB of RAM. So patience and caution on a
small virtual server is needed.
