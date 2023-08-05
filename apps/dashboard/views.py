from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import PasswordChangeView as BasePasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ProfileForm, PasswordChangeForm, AddAddressForm, AddReturnedOrderForm
from apps.accounts.models import User, Address
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from apps.order.models import Order, ReturnOrder
from django.core.paginator import Paginator
import datetime
import pytz


class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard/dashboard.html'

    def get(self, request):
        last_month = datetime.datetime.now() - datetime.timedelta(weeks=6)
        recently_orders = Order.objects.filter(user=request.user, created_at__gt=last_month)
        return render(request, self.template_name, {'recently_orders': recently_orders})


class ProfileView(View):
    template_name = 'dashboard/profile.html'
    form_class = ProfileForm

    def get(self, request):
        user_profile = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'phone_number': request.user.phone_number,
            'email': request.user.email,
        }
        return render(request, self.template_name, {'form': self.form_class(initial=user_profile)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            print(cleaned_data['first_name'])
            try:
                user = User.objects.get(phone_number=request.user.phone_number)
                user.first_name = cleaned_data['first_name']
                user.last_name = cleaned_data['last_name']
                user.email = cleaned_data['email']
                user.save()

                messages.success(request, 'اطلاعات شما با موفقیت تغییر یافت', 'success')
                return redirect('dashboard:dashboard')
            except ObjectDoesNotExist:
                messages.error(request, 'مشکلی در ویرایش اطلاعات پیش آمد', 'danger')
                return render(request, self.template_name, {'form': form})

        messages.warning(request, 'لطفا تمامی فیلدها رو پر کنید', 'warning')
        return render(request, self.template_name, {'form': form})


class PasswordChangeView(BasePasswordChangeView):
    template_name = 'dashboard/password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('dashboard:success_change_password')


class SuccessPasswordChangeView(View):
    def get(self, request, *args, **kwargs):
        messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد', 'success')
        return redirect('dashboard:password_change')


class AddressesView(View):
    template_name = 'dashboard/addresses.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class AddAddressView(View):
    template_name = 'dashboard/add_address.html'
    form_class = AddAddressForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.addresses.count() >= 5:
            messages.warning(request, 'شما سقف تعداد آدرس ها را دارید، برای افزودن آدرس جدید یک آدرس را حدف کنید')
            return redirect('dashboard:addresses')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            messages.success(request, 'آدرس جدید ثبت شد', 'success')
            return redirect('dashboard:addresses')
        messages.error(request, 'مشکلی در ثبت آدرس رخ داد', 'danger')
        return render(request, self.template_name, {'form': form})


class EditAddressView(View):
    template_name = 'dashboard/add_address.html'
    form_class = AddAddressForm

    def setup(self, request, *args, **kwargs):
        self.selected_address = get_object_or_404(Address, id=kwargs['pk'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,
                      {'form': self.form_class(initial=self.selected_address)})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.selected_address)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            messages.success(request, 'آدرس موردنظر با موفقیت ویرایش شد', 'success')
            return redirect('dashboard:addresses')
        messages.warning(request, 'مشکلی در ویرایش آدرس به وجود آمد', 'warning')
        return render(request, self.template_name, {'form': form})


class DeleteAddressView(View):

    def get(self, request, *args, **kwargs):
        address = get_object_or_404(Address, id=kwargs['pk'])
        address.delete()
        messages.success(request, 'آدرس مورد نظر به درستی حذف شد', 'success')
        return redirect('dashboard:addresses')


class OrdersView(View):
    template_name = 'dashboard/orders.html'

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        paginator = Paginator(orders, 7)
        page_number = request.GET.get('page')
        order_objects = paginator.get_page(page_number)
        return render(request, self.template_name, {'orders': order_objects})


class OrderView(View):
    template_name = 'dashboard/order.html'

    def setup(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order, user=request.user)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'order': self.order})


class ReturnedOrdersView(View):
    template_name = 'dashboard/returned_orders.html'

    def get(self, request, *args, **kwargs):
        orders = ReturnOrder.objects.filter(order__user=request.user)
        paginator = Paginator(orders, 7)
        page_number = request.GET.get('page')
        order_objects = paginator.get_page(page_number)
        return render(request, self.template_name, {'orders': order_objects})


class ReturnedOrderView(View):
    template_name = 'dashboard/returned_order.html'

    def setup(self, request, *args, **kwargs):
        self.order = get_object_or_404(ReturnOrder, user=request.user)
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'order': self.order})


class AddReturnedOrderView(View):
    template_name = 'dashboard/add_returned_order.html'
    form_class = AddReturnedOrderForm

    def setup(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order, pk=kwargs['order_id'])
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        utc = pytz.UTC
        two_week_test = self.order.created_at + datetime.timedelta(weeks=2)
        if not two_week_test > (utc.localize(datetime.datetime.now())):
            messages.warning(request,
                             'بیش از دو هفته از ثبت سفارش شما گذشته و قادر به درخواست مرجوعی نیستید،'
                             ' در صورت داشتن سوال با پشتیبانی تماس بگیرید',
                             'warning')
            return redirect('dashboard:orders')

        if ReturnOrder.objects.filter(order=self.order).exists():
            messages.info(request, 'برای این سفارش مرجوعی ثبت شده، میتوانید سفارش مرجوعی خود را ویرایش کنید', 'info')
            return redirect('dashboard:edit_returned_order', order_id=self.order.id)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class(order_id=kwargs['order_id'])})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, order_id=kwargs['order_id'])
        if form.is_valid():
            new_returned_order = form.save(commit=False)
            new_returned_order.order = self.order
            new_returned_order.save()
            products_ids = [product.id for product in form.cleaned_data['products']]
            new_returned_order.products.set(products_ids)
            new_returned_order.save()
            return redirect('dashboard:returned_orders')


class EditReturnedOrderView(View):
    template_name = 'dashboard/add_returned_order.html'
    form_class = AddReturnedOrderForm

    def setup(self, request, *args, **kwargs):
        self.order = get_object_or_404(Order, pk=kwargs['order_id'])
        self.returned_order = get_object_or_404(ReturnOrder, order=kwargs['order_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form_data = {
            'description': self.returned_order.description
        }
        return render(request, self.template_name, {'form': self.form_class(initial=form_data,
                                                                            order_id=kwargs['order_id'])})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, order_id=kwargs['order_id'], instance=self.returned_order)
        if form.is_valid():
            new_returned_order = form.save(commit=False)
            new_returned_order.order = self.order
            new_returned_order.save()
            products_ids = [product.id for product in form.cleaned_data['products']]
            new_returned_order.products.set(products_ids)
            new_returned_order.save()
            messages.success(request, 'با موفقیت ویرایش شد', 'success')
            return redirect('dashboard:returned_orders')
