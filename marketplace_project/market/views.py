from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product
from .forms import ProductForm


# ✅ Home / Product List
def product_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'market/product_list.html', {'products': products})


# ✅ Product Details
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'market/product_detail.html', {'product': product})


# ✅ Add Product (only for logged-in users)
@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'Your product has been added successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'market/add_product.html', {'form': form})


# ✅ Edit Product
@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('my_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'market/add_product.html', {'form': form, 'is_edit': True})


# ✅ Delete Product
@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('my_products')
    return render(request, 'market/product_confirm_delete.html', {'product': product})


# ✅ My Products (for each seller)
@login_required
def my_products(request):
    products = Product.objects.filter(seller=request.user)
    return render(request, 'market/my_products.html', {'products': products})


# ✅ Signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('product_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# ✅ Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# ✅ Logout
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ✅ Simple Cart View (placeholder)
@login_required
def cart_view(request):
    return render(request, 'market/cart.html')
