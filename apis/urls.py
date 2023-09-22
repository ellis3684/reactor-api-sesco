from django.urls import path
from .views import ListAllReactors, ListReactorsByState, ListOutagesByDate, DetailReactorByDocket, \
    DetailLastOutageByDocket, DetailLastOutageByName, DetailStatusByDocketOnDate, DetailStatusByNameOnDate


urlpatterns = [
    # Reactor endpoints
    path('reactors/all/', ListAllReactors.as_view(), name='reactor_list'),
    path('reactors/state/<str:state>/', ListReactorsByState.as_view(), name='reactor_list_by_state'),
    path('reactors/docket/<str:docket_num>/', DetailReactorByDocket.as_view(), name='reactor_detail_by_docket'),

    # Status entry endpoints
    path('status/out/<str:date>/', ListOutagesByDate.as_view(), name='outage_list_by_date'),
    path('status/last_out/docket/<str:docket_num>/', DetailLastOutageByDocket.as_view(),
         name='last_outage_detail_by_docket'),
    path('status/last_out/name/<str:short_name>/', DetailLastOutageByName.as_view(),
         name='last_outage_detail_by_name'),
    path('status/<str:docket_num>/<str:date>/', DetailStatusByDocketOnDate.as_view(),
         name='status_detail_by_docket_on_date'),
    path('status/<str:short_name>/<str:date>/', DetailStatusByNameOnDate.as_view(),
         name='status_detail_by_name_on_date'),
]
