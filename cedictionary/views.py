from django.views.generic import TemplateView

class EntrySearchView(TemplateView):
    template_name = 'cedictionary/entry_search.html'


entry_search_view = EntrySearchView.as_view()
