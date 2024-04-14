from django.shortcuts import render, redirect
from .forms import RegisterForm, ContactForm
from django.contrib import messages
from .models import *
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.db import connection
from django.views import View
from django.template import RequestContext


from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'website/index.html', {})


def about(request):
    return render(request, 'website/about.html', {})


def gallery(request):
    return render(request, 'website/gallery.html', {})


def categories(request):
    data = Category.objects.all().order_by('-id')
    return render(request, 'website/categories.html', {'data': data})


def all_products(request):
    data = Product.objects.filter(status=True).order_by('id')
    cats = Product.objects.distinct().values('category__title')
    sizes = ProductAttribute.objects.distinct().values('size__title')
    return render(request, 'website/all_products.html',
                  {
                      'data': data,
                      'cats': cats,
                      'sizes': sizes,
                  }
                  )


def category_product_list(request,cat_id):
    category=Category.objects.get(id=cat_id)
    data=Product.objects.filter(category=category, status=True).order_by('id')
    cats = Product.objects.distinct().values('category__title')
    sizes = ProductAttribute.objects.distinct().values('size__title')
    return render(request, 'website/category_product_list.html',
                  {
                      'data': data,
                      'cats': cats,
                      'sizes': sizes,
                  }
                  )


@login_required(login_url='login')
def product_detail(request, slug, id):
    product=Product.objects.get(id=id)
    sizes = ProductAttribute.objects.filter(product=product).values('size__id', 'size__title', 'price',).distinct()

    return render(request, 'website/product_detail.html',
                  {'data': product, 'sizes': sizes,})


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was successfully created for ' + user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'website/register.html', {'form': form})


@csrf_exempt
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            #include flash message in case of invalid login credentials
            messages.error(request, 'Invalid username or password.')
            return render(request, 'website/login.html')
    else:
        return render(request, 'website/login.html', {})


def logoutUser(request):
    logout(request)
    return redirect('login')


def filter_data(request):
    categories = request.GET.getlist('category[]')
    sizes = request.GET.getlist('size[]')
    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(category__id__in=categories).distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(productattribute__size__id__in=sizes).distinct()
    t = render_to_string('website/all_products.html', {'data': allProducts})
    return JsonResponse({'data': t})


class SearchView(View):
    template_name = 'website/search.html'

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')

        sql = """
        SELECT id, title, slug, image
        FROM website_product
        WHERE title LIKE '%""" + query + """%' AND status = 1
        """

        with connection.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        products = [{'id': row[0], 'title': row[1], 'slug': row[2], 'image': row[3]} for row in rows]

        context = {
            'products': products,
            'query': query,
        }

        return render(request, self.template_name, context)



@csrf_exempt
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            timestamp = datetime.now()

            ContactMessage.objects.create(name=name, email=email, message=message, timestamp=timestamp)
            return redirect('contact')
    else:

        initial_data = {}
        if request.user.is_authenticated:
            initial_data['username'] = request.user.get_full_name() or request.user.username
        form = ContactForm(initial=initial_data)

    return render(request, 'website/contact.html', {'form': form})


# Predefined list of locations
locations = ['New York', 'Los Angeles', 'Chicago', 'San Francisco']


def location(request):
    if request.method == 'POST':
        # Get the user input from the form
        user_location = request.POST.get('location', '')

        # Check if the user input matches any location in the predefined list
        if user_location in locations:
            exists = True
        else:
            exists = False

        # Pass the result to the template
        return render(request, 'website/location.html', {'user_location': user_location, 'exists': exists})
    else:
        # Render the initial form
        return render(request, 'website/location.html')