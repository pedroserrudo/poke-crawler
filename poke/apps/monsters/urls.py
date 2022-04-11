from django.urls import path

from poke.apps.monsters.views import MonstersListView, MonstersDetailView


urlpatterns = [

    path('', MonstersListView.as_view(), name='monsters-list'),
    path('<int:pk>/', MonstersDetailView.as_view(), name='monsters-detail')

]
