"""StartProj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from Army import views
from Army.twviews import ProductDetailView, ProductListView
from Army.twviews import ProductAdd, ProductEdit, ProductDelete
from django.conf import settings
from django.conf.urls.static import static
from Army.models import Category
from Army.twviews import MyLoginView, MyLogoutView
from django.contrib.auth.decorators import login_required, permission_required


# a = {'template_name': 'login.html'}
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^product/(?P<category_id>\d+)/add', permission_required('Army.add_product')(ProductAdd.as_view()),
            name='product_add'),
    re_path(r'^category/(?P<category_id>\d+)$', ProductListView.as_view(), name='category'),
    re_path(r'^category/$', ProductListView.as_view(), name='category'),
    re_path(r'^product/(?P<product_id>\d+)$', ProductDetailView.as_view(), name='product'),
    re_path(r'^product/(?P<product_id>\d+)/edit',
            permission_required('Army.change_product')(ProductEdit.as_view()), name='product_edit'),
    re_path(r'^product/(?P<product_id>\d+)/delete', ProductDelete.as_view(), name='product_del'),
    re_path(r'login/', MyLoginView.as_view(), name='login'),
    re_path(r'logout/', MyLogoutView.as_view(), name='logout'),
    re_path(r'comments/', include('django_comments.urls')),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
