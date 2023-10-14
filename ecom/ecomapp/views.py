from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,CartItem,Order,Cart
from django.contrib import messages
from .forms import  RegistrationForm,AuthenticationForm,ShippingAddressForm,OrderForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def home(request):
    products=Product.objects.all()
    return render(request,'ecomapp/home.html',{'products':products})

def registration(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            user.save()
            return redirect('login')
    else:
        form=RegistrationForm()        
    return render(request,'ecomapp/register.html',{'form':form})        

def user_login(request):
    if request.method=='POST':
        form=AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            login(request,form.get_user())
            messages.success(request,'you have successfully log in.')
            return redirect('home')
    else:
        form=AuthenticationForm()
    return render(request,'ecomapp/login.html',{'form':form})    

def user_logout(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')

def product_detail(request,product_id):
    product=get_object_or_404(Product,pk=product_id)
    return render(request,'ecomapp/product_detail.html',{'product':product})

@login_required
def add_to_cart(request,product_id):
    product=get_object_or_404(Product, pk=product_id)
    user = request.user
    cart,created=Cart.objects.get_or_create(user=request.user,product=product)
    cart_item,item_created=CartItem.objects.get_or_create(cart=cart,product=product)
    
    if not item_created:
        cart_item.quantity +=1
        cart_item.save()
    cart_item.update_subtotal()
    return redirect('view_cart')
@login_required
def remove_from_cart(request,cart_item_id):
    cart_item=cart_item.objects.get(id=cart_item_id)
    if cart_itme.user==request.user:
        cart_item.delete()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items=CartItem.objects.filter(user=request.user)
    print (cart_items)

    for cart_items in cart_items:
        cart_item.item_total=cart_item.product.price * cart_item.quantity
    total_price=sum(cart_item.item_total for cart_item in cart_items )
    return render(request,'ecomapp/cart.html',{'cart_items':cart_items,'total_price':total_price})
   

def checkout(request):
    user=request.user
    cart_items=CartItem.objects.filter(user=user)

    if request.method == 'POST':
        form=ShippingAddressForm(request.POST)

        if form.is_valid():
            shipping_address=form.cleaned_data['shipping_address']
            total_price=sum(items.product.price * item.quantity for item in cart_items)
            order=Order.objects.create(user=user,shipping_address=shipping_address,total=total_price)

            for cart_items in cart_items:
                order.items.add(cart_item)
            cart_items.delete()    
            return redirect('order_confirmation',order_id=order.id)
    else:
        form=ShippingAddressForm()
    return render(request,'ecomapp/checkout.html',{'form':form,'cart_items':cart_items})       

def order_confirmation(request,order_id):
    try:
        order=Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        pass

    return render(request,'ecomapp/order_confirmation.html',{'order':order})
    return HttpResponse("Your Order has been placed")
    
def create_order(request):
    if request.method=='POST':
        form=OrderForm(request.POST)
        if form.is_valid():
            product=form.cleane_data['product']
            quantity=form.cleane_data['quantity']

            order=Order(
                product=product,
                quantity=quantity,
                payment_method='COD',
                is_paid=False,
            )
            order.save()
            return redirct('order_confirmation',order_id=order.id)

    else:
        form=OrderForm()
    return render(request,'ecomapp/checkout.html',{'form':form})    


