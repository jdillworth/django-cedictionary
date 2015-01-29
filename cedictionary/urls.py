from django.conf.urls import patterns, url


urlpatterns = patterns('',

    url('^$', 'cedictionary.views.entry_search_view'),

)
