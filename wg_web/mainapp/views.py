from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.shortcuts import render, redirect

from django.views.generic import View, DetailView, ListView, CreateView

from .exceptions import ServerDeleteException
from .forms import VPNServerForm
from .services.servers import delete_vpn_server
from .models import VPNServer, VPNService, VPNClient, VPNDevice


class MainPageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, *args, **kwargs):
        return render(self.request, 'mainapp/main_page.html')


class VPNServersView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = VPNServer
    template_name = 'mainapp/vpn_servers.html'
    context_object_name = 'servers'


class VPNServersCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = '/login/'
    model = VPNServer
    form_class = VPNServerForm
    template_name = 'mainapp/form.html'
    success_url = '/vpn_servers'
    success_message = 'Server created successfully!'


@login_required(login_url='/login/')
def delete_vpn_server_view(request, pk: int) -> None:
    """Delete server view"""
    if request.method == 'POST':
        try:
            delete_vpn_server(pk)
            messages.success(request, 'Server deleted successfully!')
        except ServerDeleteException:
            messages.error(request, f'Server with id {pk} does not exist!')
        return redirect('mainapp:vpn_servers_page')
