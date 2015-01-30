import re

from django.views.generic import TemplateView
from django.db.models import Q

from . import models

class EntrySearchView(TemplateView):
    template_name = 'cedictionary/entry_search.html'

    def get_context_data(self, **kwargs):
        ctx = super(EntrySearchView, self).get_context_data(**kwargs)
        ctx['query'] = q = self.request.GET.get('q', '')
        if q:
            letters_q = re.sub(r'[^A-Za-z]', '', q)
            if letters_q:
                search = Q(pinyin_letters__iexact=letters_q)
            else:
                search = Q(chs=q) | Q(ch=q)

            ctx['cedict_entries'] = models.ChineseEntry.objects.filter(search)

        return ctx

entry_search_view = EntrySearchView.as_view()
