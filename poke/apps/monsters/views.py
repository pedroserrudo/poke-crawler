import random

from django.views.generic import ListView, DetailView


from poke.apps.monsters.models import Pokemon
from poke.apps.crawler.api import crawler


class MonstersListView(ListView):
    template_name = "monsters/list.html"
    model = Pokemon
    paginate_by = 50

    def get_queryset(self):
        qs = self.model.objects.all()
        if search := self.request.GET.get('search'):
            qs = qs.filter(name__icontains=search)
        return qs


class MonstersDetailView(DetailView):
    model = Pokemon
    template_name = "monsters/details.html"
    queryset = Pokemon.objects.all().prefetch_related('moves', 'held_items')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.weight is None or self.object.height is None:
            # needs update
            crawler.update_all_details(self.object.pk)
            self.object = self.get_object()

        # logic for catch me
        is_catch = False
        catches = request.session.get('catches', [])

        if request.GET.get('catch'):
            if random.randint(1, 100) >= 69:
                is_catch = 'catch'
                catches.append(self.object.pk)
            else:
                is_catch = 'miss'

        request.session['catches'] = catches
        context = self.get_context_data(object=self.object)
        context['move'] = self.object.moves.all().order_by('?').first() if is_catch == 'miss' else None
        context['catch'] = is_catch
        context['many'] = catches.count(self.object.pk)

        return self.render_to_response(context)





