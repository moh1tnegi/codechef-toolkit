from django.conf.urls import url
from . import views

app_name = 'codechef'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^city-details/$', views.city_details, name='all_cities'),
    url(r'^state-details/$', views.state_details, name='all_states'),
    url(r'^institute-details/$', views.inst_details, name='all_inst'),
]
