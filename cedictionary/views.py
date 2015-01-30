import re

from django.views.generic import TemplateView
from django.db.models import Q

from rest_framework import viewsets, generics
from rest_framework.response import Response

from . import models, serializers

def entries_matching(q):
    q = q.strip()
    # only keep * at the end for now
    letters_q = (re.sub(r'[^A-Za-z]', '', q[:-1]) +
            re.sub(r'[^A-Za-z\*]', '', q[-1]))
            
    if letters_q:
        if letters_q[-1] == '*':
            search = Q(pinyin_letters__istartswith=letters_q[:-1])
        else:
            search = Q(pinyin_letters__iexact=letters_q)
    else:
        search = Q(chs=q) | Q(ch=q)

    return models.ChineseEntry.objects.filter(search)

class EntrySearchView(TemplateView):
    template_name = 'cedictionary/entry_search.html'

    def get_context_data(self, **kwargs):
        ctx = super(EntrySearchView, self).get_context_data(**kwargs)
        ctx['query'] = q = self.request.GET.get('q', '')
        if q:
            ctx['cedict_entries'] = entries_matching(q)

        return ctx

entry_search_view = EntrySearchView.as_view()

class ChineseEntryList(generics.ListAPIView):
    """
    API endpoint that allows chinese entries to be listed and searched.
    """
    model = models.ChineseEntry
    serializer_class = serializers.ChineseEntrySerializer
    paginate_by = 20

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        if q:
            return entries_matching(q)
        else:
            return models.ChineseEntry.objects.all()


chinese_entry_list = ChineseEntryList.as_view()


class ChineseEntryDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a specific chinese entry to be retrieved
    """

    queryset = models.ChineseEntry.objects.all()
    serializer_class = serializers.ChineseEntrySerializer


chinese_entry_detail = ChineseEntryDetail.as_view()
