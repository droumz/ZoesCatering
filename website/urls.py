from django.urls import path
from . import views
from .views import SearchView

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('gallery', views.gallery, name='gallery'),
    path('categories', views.categories, name='categories'),
    path('all_products', views.all_products, name='all_products'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.register, name='register'),
    path('category-product-list/<int:cat_id>', views.category_product_list, name='category-product-list'),
    path('product/<str:slug>/<int:id>', views.product_detail, name='product'),
    path('filter-data', views.filter_data, name='filter_data'),
    path('search', SearchView.as_view(), name='search'),
    path('contact', views.contact, name='contact'),
    path('location', views.location, name='location'),
]

