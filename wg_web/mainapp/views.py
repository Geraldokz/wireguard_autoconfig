from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin, messages
from django.shortcuts import render, redirect
from django.views.generic import View, DetailView, ListView, CreateView, UpdateView

from .exceptions import ModelDeleteException
from .forms import VPNServerForm, VPNServiceForm, VPNClientForm, VPNDeviceForm
from .services.models.crud import delete_model_object
from .services.wg_keys import generate_keys
from .services.vpn_services.service import get_all_vpn_service_devices
from .services.vpn_services.network import generate_vpn_device_ip, get_service_wg_address
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

    def get_initial(self, *args, **kwargs):
        initial = super(VPNServiceCreateView, self).get_initial()
        initial['private_key'], initial['public_key'] = generate_keys()
        return initial


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


class VPNServiceDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = VPNService
    context_object_name = 'service'
    template_name = 'mainapp/vpn_service_detail.html'

    def get_context_data(self, **kwargs):
        service_address = get_service_wg_address(self.kwargs['pk'])
        service_devices = get_all_vpn_service_devices(self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['clients'] = VPNClient.objects.filter(vpn_service=self.object)
        context['service_addr'] = service_address
        context['devices'] = service_devices
        return context


class VPNClientCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = '/login/'
    form_class = VPNClientForm
    template_name = 'mainapp/form.html'
    success_message = 'Client created successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Create VPN Client'
        context['submit_button_text'] = 'Create client'
        context['cancel_button_url'] = f'/vpn_services/{self.kwargs["pk"]}'
        return context

    def get_initial(self, *args, **kwargs):
        initial = super(VPNClientCreateView, self).get_initial()
        initial['vpn_service'] = self.kwargs['pk']
        return initial

    def get_success_url(self):
        return f'/vpn_services/{self.kwargs["pk"]}'


class VPNClientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = '/login/'
    form_class = VPNClientForm
    model = VPNClient
    template_name = 'mainapp/form.html'
    success_message = 'Client updated successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Update VPN Client'
        context['submit_button_text'] = 'Update client'
        context['cancel_button_url'] = f'/vpn_services/{self.kwargs["service_id"]}'
        return context

    def get_initial(self, *args, **kwargs):
        initial = super(VPNClientUpdateView, self).get_initial()
        initial['vpn_service'] = self.kwargs['service_id']
        return initial

    def get_success_url(self):
        return f'/vpn_services/{self.kwargs["service_id"]}'


# TO DO: change cancel button url in update form when updating from details page
class VPNClientDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    model = VPNClient
    context_object_name = 'client'
    template_name = 'mainapp/vpn_client_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['devices'] = VPNDevice.objects.filter(client=self.object)
        return context


class VPNDeviceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = '/login/'
    form_class = VPNDeviceForm
    template_name = 'mainapp/form.html'
    success_message = 'Device created successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Create VPN Device'
        context['submit_button_text'] = 'Create device'
        context['cancel_button_url'] = f'/vpn_services/{self.kwargs["service_id"]}/clients/{self.kwargs["pk"]}'
        return context

    def get_initial(self, *args, **kwargs):
        initial = super(VPNDeviceCreateView, self).get_initial()
        private_key, public_key = generate_keys()
        ip_address = generate_vpn_device_ip(self.kwargs['service_id'])
        initial['client'] = self.kwargs['pk']
        initial['private_key'] = private_key
        initial['public_key'] = public_key
        initial['private_ip'] = ip_address
        return initial

    def get_success_url(self):
        return f'/vpn_services/{self.kwargs["service_id"]}/clients/{self.kwargs["pk"]}'


class VPNDeviceUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = '/login/'
    form_class = VPNDeviceForm
    model = VPNDevice
    template_name = 'mainapp/form.html'
    success_message = 'Device updated successfully!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['header'] = 'Update VPN Device'
        context['submit_button_text'] = 'Update device'
        context['cancel_button_url'] = f'/vpn_services/{self.kwargs["service_id"]}/clients/{self.kwargs["client_id"]}'
        return context

    def get_initial(self, *args, **kwargs):
        initial = super(VPNDeviceUpdateView, self).get_initial()
        initial['client'] = self.kwargs['client_id']
        return initial

    def get_success_url(self):
        return f'/vpn_services/{self.kwargs["service_id"]}/clients/{self.kwargs["client_id"]}'


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


@login_required(login_url='/login/')
def delete_vpn_service_client(request, service_id, pk: int) -> None:
    """Delete VPN Client view"""
    if request.method == 'POST':
        try:
            delete_model_object(pk, VPNClient)
            messages.success(request, 'VPN Client deleted successfully!')
        except ModelDeleteException:
            messages.error(request, f'VPN Client with id {pk} does not exist!')
        return redirect('mainapp:vpn_service_details_page', pk=service_id)


@login_required(login_url='/login/')
def delete_vpn_device_view(request, service_id: int, client_id: int, pk: int) -> None:
    """Delete VPN Client view"""
    if request.method == 'POST':
        try:
            delete_model_object(pk, VPNDevice)
            messages.success(request, 'VPN Device deleted successfully!')
        except ModelDeleteException:
            messages.error(request, f'VPN Device with id {pk} does not exist!')
        return redirect('mainapp:vpn_client_details_page', service_id=service_id, pk=client_id)
