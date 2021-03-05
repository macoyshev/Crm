from django.contrib import admin

# Register your models here.


from .models import *

#сначала нужно создать модели - таблицы, где каждая сторока представляет поле , в котором храниться объект
#Админка - это встроенная утилита Django, которая позволяет обращаться к моделям и на их основе создать объекты 
#Но перед этим модели нужно зарегистрировать это сделано стой целью , чтобы модели не предназначенные для редактирования не попали в админку 

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Tag)