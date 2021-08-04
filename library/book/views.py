from django.shortcuts import render, redirect
from book import models
# Create your views here.


def add_publisher(request):
    if request.method == "POST":
        #获取表单提交的内荣
        publisher_name = request.POST.get("name")
        publisher_address = request.POST.get("address")
        # 保存到数据库
        models.Publisher.objects.create(name=publisher_name,address=publisher_address)
        # 专跳列表页
        return redirect("/book/publisher_list/")

    return render(request, "add_publisher.html")


def publisher_list(request):
    # 查询数据库中的所有信息
    publisher_list=models.Publisher.objects.all()
    return render(request, "publisher_list.html", {'publisher_obj_list': publisher_list})

def edit_publisher(request):
    # 如果是post请求
    if request.method == 'POST':
        # 获取id
        id = request.POST.get('id')
        name  = request.POST.get('name')
        address = request.POST.get('address')
        # 去数据库中查找相应的数据
        publisher_obj = models.Publisher.objects.get(id=id)

        # 修改
        publisher_obj.name = name
        publisher_obj.address = address
        publisher_obj.save()
        # 重定向到出版社列表
        return redirect('/book/publisher_list/')
    else:
        #id
        id = request.GET.get('id')
        # 去数据库中找相应的数据
        publisher_obj = models.Publisher.objects.get(id=id)
        publisher_obj_list = models.Publisher.objects.all()
    # 返回页面中
        return render(request, 'edit-publisher.html',{'publisher_obj': publisher_obj, 'publisher_obj_list': publisher_obj_list})


def delete_publisher(request):
    # 获取id
    id = request.GET.get('id')
    #
    models.Publisher.objects.filter(id=id).delete()
    return redirect('/book/publisher_list/')


def book_list(request):
    # 获取图书
    book_obj_list = models.Book.objects.all()
    # 将数据放入页面上
    return render(request, 'book_list.html', {"book_obj_list": book_obj_list})


def add_book(request):
    # 获取所有出版社
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        inventory = request.POST.get('inventory')
        sale_num = request.POST.get('sale_num')
        publisher_id = request.POST.get('publisher_id')
        # 保存到数据库
        models.Book.objects.create(name=name, price=price, inventory=inventory, sale_name=sale_num, publisher_id=publisher_id)
        #重定向到图书列表页面
        return redirect('/book/book_list/')
    else:
        publisher_obj_list = models.Publisher.objects.all()
        return render(request, "add_book.html", {"publisher_obj_list": publisher_obj_list})

# 修改
def edit_book(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        # 取数据库中查找相应的数据
        book_obj = models.Book.objects.filter(id=id).first()
        # 查找所有的出版社
        publisher_list = models.Publisher.objects.all()
        # 返回页面
        return render(request, 'edit_book.html',{'book_obj': book_obj, 'publisher_list': publisher_list})
    else:
        id = request.POST.get('id')
        name = request.POST.get('name')
        price = request.POST.get('price')
        inventory = request.POST.get('inventory')
        sale_num = request.POST.get('sale_num')
        publisher_id = request.POST.get('publisher_id')
        # 查询数据金西行更新
        models.Book.objects.filter(id=id).update(name=name, price=price, inventory=inventory, sale_name=sale_num, publisher_id=publisher_id)

        #重定向
        return redirect('/book/book_list/')


def delete_book(request):
    # 获取id
    id = request.GET.get('id')
    # 删除图书
    models.Book.objects.filter(id=id).delete()
    return redirect('/book/book_list/')


def author_list(request):
    ret_list = []
    author_obj_list = models.Author.objects.all()
    for author_obj in author_obj_list:
        book_obj_list = author_obj.book.all()
        ret_dic = {}
        ret_dic['author_obj'] = author_obj
        ret_dic['book_list'] = book_obj_list
        ret_list.append(ret_dic)
    return render(request, 'author_list.html', {'ret_list': ret_list})


def add_author(request):
    if request.method == 'GET':
    # 获取所有图书
        book_obj_list = models.Book.objects.all()
        return render(request, 'add_author.html', {'book_obj_list': book_obj_list})
    else:
        name = request.POST.get('name')
        book_ids = request.POST.getlist('books')
        author_obj = models.Author.objects.create(name=name)
        author_obj.book.set(book_ids) # 设置关系

        return redirect('/book/author_list/')


def edit_author(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        author_obj = models.Author.objects.get(id=id)
        book_obj_list = models.Book.objects.all()
        # 返回页面
        return render(request, 'edit_author.html', {'author_obj':author_obj, 'book_obj_list': book_obj_list})
    else:
        id = request.POST.get('id')
        name = request.POST.get('name')
        book_ids = request.POST.getlist('books')
        author_obj = models.Author.objects.filter(id=id).first()
        author_obj.name = name
        author_obj.book.set(book_ids)
        author_obj.save()
        return redirect('/book/author_list/')


def delete_author(request):
    # 获取 id
    id = request.GET.get("id")
    # 删除作者
    models.Author.objects.filter(id=id).delete()
    # 重定向
    return redirect('/book/author_list/')