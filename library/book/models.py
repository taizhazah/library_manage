from django.db import models

# Create your models here.


class Publisher(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False)
    address = models.CharField(max_length=64, null=False)


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    #价格 总共5位 小数2位 设置default 因为已经存在的字段没有数据
    price = models.DecimalField(max_digits=5, decimal_places=2, default=10.01)
    inventory = models.IntegerField(verbose_name='库存数')
    sale_name = models.IntegerField(verbose_name="卖出数")
    publisher = models.ForeignKey(to='Publisher', on_delete=models.CASCADE)


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    book = models.ManyToManyField(to='Book')