from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory # for creating multiple orders
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import *
from .filters import OrderFilter # ordering filters
from .forms import OrderForm, CustomerForm, ProductForm, CreateUserForm

from .decorators import unauthenticated_user, allowed_users, admin_only
# Create your views here.


@unauthenticated_user
def registerPage(request):
    # if request.user.is_authenticated:
    #     return redirect('dashboard')
    # else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')

                group = Group.objects.get(name= 'customer')
                user.groups.add(group)

                messages.success(request, 'Account was created for ' + username)
                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    # if request.user.is_authenticated:
    #     return redirect('dashboard')
    # else:
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Username or Password is incorrect!')
            # return render(request, 'accounts/login.html', context)

        context = {}
        return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all().order_by('-id')
    customers = Customer.objects.all().order_by('-id')

    total_orders = orders.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()

    total_customers = customers.count()

    context = {
                'orders': orders,
                'customers': customers,
                'total_orders': total_orders,
                'delivered': delivered,
                'pending': pending,
            }
    return render(request, 'accounts/dashboard.html', context)


def userPage(request):
    context = {}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all().order_by('-id')
    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
                'customer': customer,
                'orders': orders,
                'total_orders': total_orders,
                'myFilter': myFilter,
            }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request):
    form = OrderForm()

    if request.method == 'POST':
        # print('Printing post: ', request.POST)
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrderById(request, pk):
    # use 'extra' for as many fields as required
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)

    customer = Customer.objects.get(id=pk)

    ## in case of using new fields and also placed orders
    # formset = OrderFormSet(instance = customer)

    ## in case of using only new fields
    formset = OrderFormSet(queryset=Order.objects.none(), instance = customer)

    ## form = OrderForm(initial={'customer': customer})

    if request.method == 'POST':
        # print('Printing post: ', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/customer/'+ str(pk))

    context = {'formset': formset}
    return render(request, 'accounts/order_form_by_id.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        # print('Printing post: ', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        # print('Printing post: ', request.POST)
        order.delete()
        return redirect('/')

    context = { 'id': pk,
                'item': order.product,
                'customer': order.customer,
                'date_created': order.date_created,
                'status': order.status,
            }
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
    form = CustomerForm()

    if request.method == 'POST':
        # print('Printing post: ', request.POST)
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/customer_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        # print('Printing post: ', request.POST)
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/customer/'+str(pk))

    context = {'form': form}
    return render(request, 'accounts/customer_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createProduct(request):
    form = ProductForm()

    if request.method == 'POST':
        # print('Printing post: ', request.POST)
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/products/')

    context = {'form': form}
    return render(request, 'accounts/product_form.html', context)
