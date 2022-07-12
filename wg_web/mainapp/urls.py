from django.urls import path

from .views import MainPageView, VPNServersView, VPNServersCreateView, delete_vpn_server_view

app_name = 'mainapp'

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('vpn_servers', VPNServersView.as_view(), name='vpn_servers_page'),
    path('vpn_servers/create', VPNServersCreateView.as_view(), name='create_vpn_server'),
    path('vpn_servers/delete/<pk>', delete_vpn_server_view, name='delete_vpn_server')
]
