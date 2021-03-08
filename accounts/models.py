from django.db import models

# Create your models here.


class Customer(models.Model):
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__ (self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=200, null=True)

	def __str__ (self):
		return self.name


class Product(models.Model):
	CATAGORY = (
			('Indoor', 'Indoor'),
			('Outdoor', 'Outdoor'),
		)
	name = models.CharField(max_length=200, null=True)
	price = models.FloatField(null=True)
	description = models.CharField(max_length=200, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	category = models.CharField(max_length=200, null=True, choices=CATAGORY)
	tags = models.ManyToManyField(Tag)

	def __str__ (self):
		return self.name


class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out of delivery', 'Out of delivery'),
			('Dilevered', 'Dilevered'),
		)
	customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)
	
	def __str__(self):
		return self.product.name