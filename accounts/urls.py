from django.urls import path
from . import views
from django.conf import settings 
from django.conf.urls.static import static


urlpatterns = [
	path('', views.home, name="home"),
	path('products/', views.products, name="products"),
	path('customer/<str:pk_test>/', views.customer, name="customer"),
	path('userPage', views.userPage, name="userPage"),
	path('profileSettings', views.profileSettings, name='profileSettings'),

	path('create_order/<str:pk>/', views.create_order, name="create_order"),
	path('update_order/<str:pk>/', views.update_order, name="update_order"),
	path('delete_order/<str:pk>/', views.delete_order, name="delete_order"),

	path('login', views.loginPage, name='login'),
	path('register', views.register, name='register'),
	path('logout', views.logOutUser, name='logout'),

	path('contact', views.contactPage, name='contactPage')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)