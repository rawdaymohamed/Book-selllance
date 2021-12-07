from django.http import response
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from main import forms
from main import models
from django.views.generic import View
from django.contrib.auth import logout
import logging
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django import forms as django_forms
from django.db import models as django_models
import django_filters
from django_filters.views import FilterView



logger = logging.getLogger(__name__)


class DateInput(django_forms.DateInput):
    input_type = 'date'

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = models.Order
        fields = {
            'user__email': ['icontains'],
            'status': ['exact'],
            'date_updated': ['gt', 'lt'],
            'date_added': ['gt', 'lt'],
        }
        filter_overrides = {
            django_models.DateTimeField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f:{
                    'widget': DateInput
                }
            }
        }

        
class OrderView(UserPassesTestMixin, FilterView):
    filterset_class = OrderFilter
    login_url = reverse_lazy('login')
    def test_func(self):
        return self.request.user.is_staff is True

'''
    Contact us 
    Class Based View
'''


class ContactUsView(FormView):
    template_name = 'contact_form.html'
    form_class = forms.ContactForm
    success_url = '/'

    # called when the form is valid
    def form_valid(self, form):
        form.send_mail()
        return super().form_valid(form)


# Function based View
"""
    def contact_us(request):
        if request.methos == 'POST':
            form = = forms.ContactForm(request.POST)
            if form.is_valid():
                form.send_mail()
                return HttpResponseRedirect('/')
            else:
                form = forms.ContactForm()
        return render(request, 'contact_form.html', {'form': form})
"""

# product list
# url --> products/<slug:tag>/


class ProductListView(ListView):
    template_name = 'main/product_list.html'
    paginate_by = 4

    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None
        if tag != 'all':
            self.tag = get_object_or_404(
                models.ProductTag, slug=tag
            )
        if self.tag:
            products = models.Product.objects.active().filter(
                tags=self.tag
            )
        else:
            # ActiveManager
            products = models.Product.objects.active()
        return products.order_by('name')

''' 
url -> signup/
'''
class SignupView(FormView):
    template_name = 'main/signup.html'
    form_class = forms.UserCreationForm
    
    # todo search
    def get_success_url(self):
        redirect_to = self.request.GET.get('next', '/')
        return redirect_to

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        logger.info('New signup for email=%s through SignupView', email)
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        form.send_mail()
        messages.info(self.request, 'You signed up successfully.')
        return response

# url --> address/
class AddressListView(LoginRequiredMixin, ListView):
    model = models.Address

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

# url --> address/create
class AddressCreateView(LoginRequiredMixin, CreateView):
    model = models.Address
    fields = ['name', 'address1', 'address2', 'zip_code', 'city', 'country']
    success_url = reverse_lazy('address_list')

    # called when the form is valid
    # save the address after assigning authorized author
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

# url --> address/<int:pk>/
class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Address
    fields = ['name', 'address1', 'address2', 'zip_code', 'city', 'country']
    success_url = reverse_lazy('address_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


# url --> address/<int:pk>/delete
class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Address
    template_name = 'main/address_delete.html'
    success_url = reverse_lazy('address_list')

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


# url --> add_to_basket/
# todo ???????
def add_to_basket(request):
    product = get_object_or_404(
        models.Product, pk=request.GET.get('product_id')
    )
    basket = request.basket
    if not request.basket:
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        basket = models.Basket.objects.create(user=user)
        request.session['basket_id'] = basket.id
    basketline, created = models.BasketLine.objects.get_or_create(
        basket=basket, product=product
    )
    if not created:
        basketline.quantity += 1
        basketline.save()
    return HttpResponseRedirect(reverse('product', args=(product.slug,)))



# function-based view
# it would be difficult with CBV

# url --> basket/
def manage_basket(request):
    if not request.basket:
        return render(request, 'basket.html', {'formset': None})

    if request.method == 'POST':
        formset = forms.BasketLineFormSet(
            request.POST, instance=request.basket
        )
        if formset.is_valid():
            formset.save()
    else:
        formset = forms.BasketLineFormSet(instance=request.basket)
    if request.basket.is_empty():
        return render(request, 'basket.html', {'formset': None})
    return render(request, 'basket.html', {'formset': formset})

# url --> order/address_select/
class AddressSelectionView(LoginRequiredMixin, FormView):
    template_name = 'address_select.html'
    form_class = forms.AddressSelectionForm
    success_url = reverse_lazy('checkout_done')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # print(self.request.session['basket_id'])
        del self.request.session['basket_id']
        basket = self.request.basket
        basket.create_order(
            form.cleaned_data['billing_address'],
            form.cleaned_data['shipping_address']
        )
        return super().form_valid(form)

