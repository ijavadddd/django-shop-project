from django.urls import path
from .views import (DashboardView,
                    ProfileView,
                    PasswordChangeView,
                    SuccessPasswordChangeView,
                    AddressesView,
                    AddAddressView,
                    EditAddressView,
                    DeleteAddressView,
                    OrdersView,
                    OrderView,
                    ReturnedOrdersView,
                    ReturnedOrderView,
                    AddReturnedOrderView,
                    EditReturnedOrderView)


app_name = 'dashboard'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', PasswordChangeView.as_view(), name='password_change'),
    path('success-change-password/', SuccessPasswordChangeView.as_view(), name='success_change_password'),
    path('addresses/', AddressesView.as_view(), name='addresses'),
    path('add-new-address/', AddAddressView.as_view(), name='add_address'),
    path('edit-address/<int:pk>/', EditAddressView.as_view(), name='edit_address'),
    path('delete-address/<int:pk>/', DeleteAddressView.as_view(), name='delete_address'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('order/<int:id>/', OrderView.as_view(), name='order'),
    path('returned-orders/', ReturnedOrdersView.as_view(), name='returned_orders'),
    path('returned-order/<int:order_code>/', ReturnedOrderView.as_view(), name='returned_order'),
    path('add-returned-order/<int:order_id>/', AddReturnedOrderView.as_view(), name='add_returned_order'),
    path('edit-returned-order/<int:order_id>/', EditReturnedOrderView.as_view(), name='edit_returned_order'),
]
