from django.urls import path

from .views import (
    MainPageView,
    VPNServerListView,
    VPNServerCreateView,
    VPNServerUpdateView,
    VPNServiceListView,
    VPNServiceCreateView,
    VPNServiceUpdateView,
    VPNServiceDetailView,
    VPNClientCreateView,
    VPNClientUpdateView,
    delete_vpn_server_view,
    delete_vpn_service_view,
    delete_vpn_service_client
)

app_name = 'mainapp'

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('vpn_servers', VPNServerListView.as_view(), name='vpn_servers_page'),
    path('vpn_servers/create', VPNServerCreateView.as_view(), name='create_vpn_server'),
    path('vpn_servers/update/<pk>', VPNServerUpdateView.as_view(), name='update_vpn_server'),
    path('vpn_servers/delete/<pk>', delete_vpn_server_view, name='delete_vpn_server'),
    path('vpn_services', VPNServiceListView.as_view(), name='vpn_services_page'),
    path('vpn_services/create', VPNServiceCreateView.as_view(), name='create_vpn_service'),
    path('vpn_services/update/<pk>', VPNServiceUpdateView.as_view(), name='update_vpn_service'),
    path('vpn_services/<pk>', VPNServiceDetailView.as_view(), name='vpn_service_details_page'),
    path('vpn_services/delete/<pk>', delete_vpn_service_view, name='delete_vpn_service'),
    path('vpn_services/<pk>/clients/create_client', VPNClientCreateView.as_view(), name='create_vpn_client'),
    path('vpn_services/<service_id>/clients/update/<pk>', VPNClientUpdateView.as_view(),
         name='update_vpn_client'),
    path('vpn_services/<service_id>/clients/delete/<pk>', delete_vpn_service_client, name='delete_vpn_client'),
]
