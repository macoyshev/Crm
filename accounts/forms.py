from django.forms import ModelForm
from .models import Order
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django import forms

"""
	класс с помощье которого можно создавать новые сторики(заказы) в базе данных(Order)
	model мы указываем какую модель взять в качестве шаблона и с какими параметрами создать новую строку в базе данныйх (fields)
"""
class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'


class CreateRegisterForm(UserCreationForm):
	class Meta:
		model = User 
		fields = ['username', 'email', 'password1', 'password2']
