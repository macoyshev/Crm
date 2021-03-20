from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *

from .forms import *

from .decorators import unauthenticated_user, allowed_users, admin_only

from django.forms.models import inlineformset_factory
from .filters import OrderFilter

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm

'''django проходит по каждому приложению , и если видет папку templates, то кидает их в помещает их templates всего приложения
и render вызывает первый совпавший шаблон , поэтому внутри папки templates принято создавать папку приложения, чтобы вызывать 
конкрентный шаблон (main файлы будут почти в каджом приложении , и если их не разделить , то будет вызываться 1 совпавший шаблон)'''


# function called by link - 'port/'
@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()
	total_orders = orders.count()
	delivered = orders.filter(status="Dilevered").count()
	pending = orders.filter(status="Pending").count()
	context = {
			'orders': orders,
			'customers': customers,
			'total_orders': total_orders,
			'delivered': delivered,
			'pending': pending,
		}
	return render(request, 'accounts/dashboard.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles='customer')
def userPage(request):
	orders = request.user.customer.order_set.all()
	total_orders = orders.count()
	delivered = orders.filter(status="Dilevered").count()
	pending = orders.filter(status="Pending").count()
	context = {
			'orders': orders,
			'total_orders': total_orders,
			'delivered': delivered,
			'pending': pending,
		}
	return render(request, 'accounts/userPage.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def products(request):
	products = Product.objects.all()
	context = {
			'products': products,
		}
	return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)
	orders = customer.order_set.all()
	total_orders = orders.count()
	myFilter = OrderFilter(request.GET, queryset=Order.objects.all())
	orders = myFilter.qs
	context = {
		'customer': customer,
		'orders': orders,
		'total_orders': total_orders,
		'myFilter': myFilter,
	}
	return render(request, 'accounts/customer.html', context)


""" 
	Функция для создания заказа
	Создается экземляр класса OrderForm -> form.py для дальнейшего ознакомления
	Затем форма с пустыми полями отправляется в шаблон 
	(1 первым агрумент OrderForm POST в котором хранятся поля со значениями для сохр)
	Если мы получили запрос(POST)(это экземляр Querry...чего-то там)
	то проверяем на валидность 
	и сохраняем save. Django за нас создаст новую строку в Таблице order с полученными параметрами
	и перессылаем в HOme 
"""
@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def create_order(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields = ('product', 'status'))
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	if request.method == 'POST':
		formset = OrderForm(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	context = {
		'formset': formset
	}
	return render(request, 'accounts/create_order.html', context)


"""
	все тоже самое, что и в create_order за одним исключение мы не создаем новый объект, а
	корректируем старый для этого стоит отпративить объект которым мы хотим обновить в параметре instance 
	
"""
@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def update_order(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {
		'form': form
	}
	return render(request, 'accounts/create_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def delete_order(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {
		'item': order,
	}
	return render(request, 'accounts/delete_order.html', context)


@unauthenticated_user
def register(request):
	form = CreateRegisterForm()
	if request.method == 'POST':
		form = CreateRegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			group = Group.objects.get(name='customer')
			user.groups.add(group)
			messages.success(request, 'Account was created' + username)
			return redirect('login')
	context = {
		'form': form,
	}
	return render(request, 'accounts/register.html', context)


"""
	Login создает сессию, где хранит id обьекта для дальнейшего использования
	Authenticate проверяют базу данных на наличие пользователя и возращает обьект в случае успеха
"""
@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request.POST, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request,'Uncorrect login or password')
	return render(request, 'accounts/login.html')

""""""
def logOutUser(request):
	logout(request)
	return redirect('login')