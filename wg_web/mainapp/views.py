from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from django.views.generic import View, DetailView, ListView

from .models import VPNServer, VPNService, VPNClient, VPNDevice


class MainPageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, *args, **kwargs):
        return render(self.request, 'mainapp/main_page.html')


class VPNServersView(LoginRequiredMixin, ListView):
    model = VPNServer
    template_name = 'mainapp/vpn_servers.html'
    context_object_name = 'servers'
