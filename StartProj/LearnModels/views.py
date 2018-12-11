from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect, Http404
from LearnModels.models import Category, Product
from django.core.exceptions import ObjectDoesNotExist


def t_print(request, id):
    p_in_stock = Product.obj.filter(in_stock=True)
    p_dict = {}
    for prod in p_in_stock:
        p_dict[prod.title] = {'title': prod.title,
                              'in stock': '+' if prod.in_stock else '-'}
    # response =
    return HttpResponse(id)


def product(request, product_id=None):
    if product_id is None:
        return HttpResponse('<h1>Продукт не выбран</h1>')
    else:
        try:
            product = Product.obj.get(id=product_id)
        except ObjectDoesNotExist:
            raise Http404
        return render(request, 'Product.html', {'product': product})


def categories(request, category_id=None):
    if category_id is None:
        category = Category.obj.all()
        return render(request, 'Categories.html',
                      {'categories': category})
    else:
        category = Category.obj.get(id=category_id)
        products = Product.obj.filter(category__id=category_id)
        return render(request, 'ProductsInCategory.html',
                      {'category': category, 'products': products})
