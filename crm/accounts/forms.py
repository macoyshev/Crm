from django.forms import ModelForm
from .models import Order


"""
	класс с помощье которого можно создавать новые сторики(заказы) в базе данных(Order)
	model мы указываем какую модель взять в качестве шаблона и с какими параметрами создать новую строку в базе данныйх (fields)
"""
class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'