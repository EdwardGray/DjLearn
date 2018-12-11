from django.shortcuts import render
from Army.models import Category, Product
from django.http import HttpResponse, HttpResponsePermanentRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage


def category(request, category_id=None):
    try:
        page_num = request.GET['page']
    except KeyError:
        page_num = 1
    if category_id is None:
        categories = Category.obj.all()
        category = categories[0]
        category_id = category.id
        # products = Product.obj.filter(category__id=category.id)
    else:
        categories = Category.obj.all()
        category = Category.obj.get(id=category_id)
        # products = Product.obj.filter(category__id=category_id)

    paginator = Paginator(Product.obj.filter(category__id=category_id).order_by('title'), 2)

    try:
        products = paginator.page(page_num)
    except InvalidPage:
        products = paginator.page(1)

    return render(request, 'Category.html',
                  {'categories': categories, 'category': category,
                   'products': products})


def product(request, product_id=None):
    try:
        try:
            page_num = request.GET['page']
        except KeyError:
            page_num = 1

        if product_id is None:
            categories = Category.obj.all()
            product = Product.obj.filter(category=categories.first())[0]

            return render(request, 'Product.html',
                          {'categories': categories, 'product': product})
        else:
            categories = Category.obj.all()
            product = Product.obj.get(id=product_id)

            return render(request, 'Product.html',
                          {'categories': categories, 'product': product,
                           'page_num': page_num})
    except ObjectDoesNotExist:
        raise Http404