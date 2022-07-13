from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.shortcuts import render, redirect

from django.views.generic import View, DetailView, ListView, CreateView, UpdateView, FormView

from .exceptions import ModelDeleteException
from .forms import VPNServerForm, VPNServiceForm
from .services.models.crud import delete_model_object
from .models import VPNServer, VPNService, VPNClient, VPNDevice


class MainPageView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, *args, **kwargs):
        return render(self.request, 'mainapp/main_page.html')


class VPNServerListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = VPNServer
    template_name = 'mainapp/vpn_servers.html'
    context_object_name = 'servers'


class VPNServerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = '/login/'
    model = VPNServer
    form_class = VPNServerForm
    template_name = 'mainapp/form.html'
    success_url = '/vpn_servers'
    success_message = 'Server created successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Create server'
        context['submit_button_text'] = 'Create server'
        context['cancel_button_url'] = self.success_url
        return context


class VPNServerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = '/login/'
    model = VPNServer
    form_class = VPNServerForm
    template_name = 'mainapp/form.html'
    success_url = '/vpn_servers'
    success_message = 'Server updated successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Update server'
        context['submit_button_text'] = 'Update server'
        context['cancel_button_url'] = self.success_url
        return context


class VPNServiceListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = VPNService
    template_name = 'mainapp/vpn_services.html'
    context_object_name = 'services'


class VPNServiceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = '/login/'
    form_class = VPNServiceForm
    template_name = 'mainapp/form.html'
    success_url = '/vpn_services'
    success_message = 'VPN Service created successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Create VPN Service'
        context['submit_button_text'] = 'Create service'
        context['cancel_button_url'] = self.success_url
        return context


class VPNServiceUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = '/login/'
    model = VPNService
    form_class = VPNServiceForm
    template_name = 'mainapp/form.html'
    success_url = '/vpn_services'
    success_message = 'VPN Service updated successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Update VPN Service'
        context['submit_button_text'] = 'Update service'
        context['cancel_button_url'] = self.success_url
        return context


@login_required(login_url='/login/')
def delete_vpn_server_view(request, pk: int) -> None:
    """Delete server view"""
    if request.method == 'POST':
        try:
            delete_model_object(pk, VPNServer)
            messages.success(request, 'Server deleted successfully!')
        except ModelDeleteException:
            messages.error(request, f'Server with id {pk} does not exist!')
        return redirect('mainapp:vpn_servers_page')


@login_required(login_url='/login/')
def delete_vpn_service_view(request, pk: int) -> None:
    """Delete service view"""
    if request.method == 'POST':
        try:
            delete_model_object(pk, VPNService)
            messages.success(request, 'VPN Service deleted successfully!')
        except ModelDeleteException:
            messages.error(request, f'VPN Service with id {pk} does not exist!')
        return redirect('mainapp:vpn_services_page')
