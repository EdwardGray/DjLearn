from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from Army.models import Category, Product
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import ContextMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ProcessFormView
from django.urls import reverse
from .forms import ProductAddForm, ProductEditForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from PIL import Image

# class ProductListView(TemplateView):
#     template_name = 'Category.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductListView, self).get_context_data(**kwargs)
#
#         try:
#             page_num = self.request.GET['page']
#         except KeyError:
#             page_num = 1
#
#         context['categories'] = Category.obj.order_by('title')
#
#         if 'category_id' not in kwargs:
#             context['category'] = Category.obj.first()
#         else:
#             context['category'] = Category.obj.get(id=kwargs['category_id'])
#
#         paginator = Paginator(Product.obj.filter(category=context['category']).order_by('title'), 2)
#
#         try:
#             context['products'] = paginator.page(page_num)
#         except InvalidPage:
#             context['products'] = paginator.page(1)
#
#         return context

# class ProductDetailView(TemplateView):
#     template_name = 'Product.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(ProductDetailView, self).get_context_data(**kwargs)
#
#         try:
#             context['page_num'] = self.request.GET['page']
#         except KeyError:
#             context['page_num'] = 1
#
#         context['categories'] = Category.obj.order_by('title')
#         try:
#             context['product'] = Product.obj.get(id=kwargs['product_id'])
#         except Product.DoesNotExist:
#             raise Http404
#         return context


class CategoryListMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.obj.order_by('title')
        return context


class ProductListView(ListView, CategoryListMixin):
    template_name = 'Category.html'
    paginate_by = 2
    category = None

    def get(self, request, *args, **kwargs):
        if 'category_id' not in self.kwargs:
            self.category = Category.obj.first()
        else:
            self.category = Category.obj.get(id=self.kwargs['category_id'])

        return super(ProductListView, self).get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        # context['categories'] = Category.obj.order_by('title')
        context['category'] = self.category

        return context

    def get_queryset(self):
        # return Product.obj.filter(category=self.category).order_by('title')
        products = Product.obj.filter(category=self.category).order_by('title')
        try:
            products = products.filter(tags__name=self.request.GET['tag'])
        except KeyError:
            pass
        return products


class ProductDetailView(DetailView, CategoryListMixin):
    template_name = 'Product.html'
    model = Product
    # context_object_name = 'product'
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        try:
            context['page_num'] = self.request.GET['page']
        except KeyError:
            context['page_num'] = 1

        # context['categories'] = Category.obj.order_by('title')
        return context


class ProductEditMixin(CategoryListMixin):
    def get_context_data(self, **kwargs):
        context = super(ProductEditMixin, self).get_context_data(**kwargs)
        try:
            context['page_num'] = self.request.GET['page']
        except KeyError:
            context['page_num'] = 1

        return context


class ProductEditView(ProcessFormView):
    def post(self, request, *args, **kwargs):
        try:
            page_num = request.GET['page']
        except KeyError:
            page_num = 1
        self.success_url = self.success_url + '?page=' + page_num

        return super().post(request, *args, **kwargs)


class ProductAdd(SuccessMessageMixin, CreateView, ProductEditMixin):
    model = Product
    form_class = ProductAddForm
    template_name = 'forms/ProductAdd.html'
    success_message = 'Продукт успешно добавлен'
    # fields = '__all__'

    def get(self, request, *args, **kwargs):
        if kwargs['category_id'] is not None:
            self.initial['category'] = Category.obj.get(id=kwargs['category_id'])
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('category',
            kwargs={'category_id': Category.obj.get(id=kwargs['category_id']).id})  # можно проще
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        content['category'] = Category.obj.get(id=self.kwargs['category_id'])
        return content


class ProductEdit(UpdateView, ProductEditMixin, ProductEditView):
    model = Product
    form_class = ProductEditForm
    template_name = 'forms/ProductEdit.html'
    pk_url_kwarg = 'product_id'
    # fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('product',
            kwargs={'product_id': kwargs['product_id']})
        return super().post(request, *args, **kwargs)


class ProductDelete(DeleteView, ProductEditMixin, ProductEditView):
    model = Product
    template_name = 'forms/ProductDelete.html'
    pk_url_kwarg = 'product_id'
    fields = '__all__'

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.has_perm('Army.delete_product'):
            pass
        else:
            return redirect('/login/?next='+request.path)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.success_url = reverse('category',
            kwargs={'category_id': Product.obj.get(id=kwargs['product_id']).category.id})
        messages.add_message(request, messages.SUCCESS,
                             'Продукт {0} успешно удален'.format(Product.obj.get(id=kwargs['product_id']).title))
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = Product.obj.get(id=self.kwargs['product_id'])
        return context


# Вход и выход

from django.contrib.auth.views import LoginView, LogoutView


class MyLoginView(LoginView, CategoryListMixin):

    template_name = 'login.html'


class MyLogoutView(LogoutView, CategoryListMixin):

    template_name = 'logout.html'

