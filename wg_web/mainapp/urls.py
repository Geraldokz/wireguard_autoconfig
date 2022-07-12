from django.urls import path

from .views import MainPageView, VPNServersView

app_name = 'mainapp'

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('vpn_servers', VPNServersView.as_view(), name='vpn_servers_page'),
]
