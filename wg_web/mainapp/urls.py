from django.urls import path

from .views import (
    MainPageView,
    VPNServerListView,
    VPNServerCreateView,
    VPNServerUpdateView,
    VPNServiceListView,
    delete_vpn_server_view
)

app_name = 'mainapp'

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('vpn_servers', VPNServerListView.as_view(), name='vpn_servers_page'),
    path('vpn_servers/create', VPNServerCreateView.as_view(), name='create_vpn_server'),
    path('vpn_servers/update/<pk>', VPNServerUpdateView.as_view(), name='update_vpn_server'),
    path('vpn_servers/delete/<pk>', delete_vpn_server_view, name='delete_vpn_server'),
    path('vpn_services', VPNServiceListView.as_view(), name='vpn_services_page'),
]
