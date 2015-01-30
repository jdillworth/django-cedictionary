from django.conf.urls import patterns, url, include

from . import views

urlpatterns = patterns('',

    url(r'^api/entry/$', 'cedictionary.views.chinese_entry_list', name='chineseentry'),
    url(r'^api/entry/(?P<pk>\d+)/$', 'cedictionary.views.chinese_entry_detail', name='chineseentry-detail'),

    url('^$', 'cedictionary.views.entry_search_view'),



)
