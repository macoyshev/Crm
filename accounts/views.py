from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, RegisterForm
from django.forms.models import inlineformset_factory
from .filters import OrderFilter


'''django проходит по каждому приложению , и если видет папку templates, то кидает их в помещает их templates всего приложения
и render вызывает первый совпавший шаблон , поэтому внутри папки templates принято создавать папку приложения, чтобы вызывать 
конкрентный шаблон (main файлы будут почти в каджом приложении , и если их не разделить , то будет вызываться 1 совпавший шаблон)'''


# function called by link - 'port/'

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

def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html',{
			'products': products,
		})


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


def delete_order(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {
		'item': order,
	}
	return render(request, 'accounts/delete_order.html', context)


def register(request):
	form = RegisterForm()
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
	context = {
		'form': form,
	}
	return render(request, 'accounts/register.html', context)


def login(request):
	return render(request, 'accounts/login.html')