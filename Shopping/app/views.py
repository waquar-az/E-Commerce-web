from django.shortcuts import render,redirect,HttpResponse
# from django.views import views
from django.views.generic import View
from .models import *
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Q 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required  
from django.utils.decorators import method_decorator

# def home(request):
    #  return render(request, 'app/home.html')
    
class ProductView(View):
 def get(self,request):
     totalitem=0
     topwears=Product.objects.filter(category='TW')
     bottomwears=Product.objects.filter(category='BW')
     mobiles=Product.objects.filter(category='M')
     laptop=Product.objects.filter(category='L')
     
     if request.user.is_authenticated:
         totalitem=len(Cart.objects.filter(user=request.user))
         
     return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles,'laptop':laptop,'totalitem':totalitem})
 
# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
    def get(self,request,pk):
        totalitem=0
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart,'totalitem':totalitem})
    
@login_required
def add_to_cart(request):
    totalitem=0
    user=request.user
    product_id=request.GET.get('prod_id')
    # print(product_id)
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    # return render(request, 'app/addtocart.html')
    # if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))
         
    return redirect('/cart',{'totalitem':totalitem})

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        totalitem=0
        user=request.user
        cart=Cart.objects.filter(user=user)
        print(cart)
        # bussiness logic for money calculation
        amount=0.0
        shipping_amount=75.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        print(cart_product)
        
        totalitem=len(Cart.objects.filter(user=request.user))
        
        if cart_product:
            for p in cart_product:              
                tempamount=(p.quantity*p.product.discounted_price)
                amount+=tempamount
                total_amount=amount+shipping_amount
            return render(request,'app/addtocart.html',{'carts':cart,'total_amount':total_amount,'amount':amount,'totalitem':totalitem})
        else:
            return render(request,'app/emptycart.html',{'totalitem':totalitem})
      
def plus_cart(request):
    if request.method=='GET':
        
        prod_id=request.GET['prod_id']    
        c=Cart.objects.get(Q(product=prod_id)  & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=75.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:                          
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
            # total_amount=amount+shipping_amount
            
        data={
                'quantity':c.quantity,
                'amount':amount,
                'total_amount':amount+shipping_amount
            }
        
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']    
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=75.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:                          
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
            # total_amount=amount+shipping_amount
            
        data={
                'quantity':c.quantity,
                'amount':amount,
                'total_amount':amount+shipping_amount
            }
        return JsonResponse(data)          
    
def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']    
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        # c.quantity-=1
        c.delete()
        amount=0.0
        shipping_amount=75.0
        total_amount=0.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:                          
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
            # total_amount=amount
            
        data={
                # 'quantity':c.quantity,
                'amount':amount,
                'total_amount':amount+shipping_amount
            }
        return JsonResponse(data)  
    
def buy_now(request):
    totalitem=0
    if request.user.is_authenticated:
         totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/buynow.html',{'totalitem':totalitem})



def address(request):
    totalitem=0
    add=Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
         totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary','totalitem':totalitem})

@login_required
def orders(request):
    totalitem=0
    orderplaced=OrderPlaced.objects.filter(user=request.user)
    totalitem=len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html',{'orderplaced':orderplaced,'totalitem':totalitem})

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    totalitem=0
    if data == None:
        mobiles=Product.objects.filter(category='M')
    elif data=='Vivo' or data=='Oppo' or data=='iphone':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=='below' :
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=10000)      
    elif data=='above' :
        mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=10000) 
    if request.user.is_authenticated:
         totalitem=len(Cart.objects.filter(user=request.user))           
    return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitem':totalitem})

def laptop(request,data=None):
    totalitem=0
    if data == None:
        laptops=Product.objects.filter(category='L')
    elif data=='apple' or data=='Samsung' or data=='Asus':
        laptops=Product.objects.filter(category='L').filter(brand=data)
    elif data=='below' :
        laptops=Product.objects.filter(category='L').filter(discounted_price__lt=10000)      
    elif data=='above' :
        laptops=Product.objects.filter(category='L').filter(discounted_price__gt=10000) 
    if request.user.is_authenticated:
         totalitem=len(Cart.objects.filter(user=request.user))           
    return render(request, 'app/laptop.html',{'laptops':laptops,'totalitem':totalitem})

def topwear(request,data=None):
    totalitem=0
    if data == None:
        topwears=Product.objects.filter(category='TW')
    elif data=='xyz' or data=='roada':
        topwears=Product.objects.filter(category='TW').filter(brand=data)
    elif data=='below' :
        topwears=Product.objects.filter(category='TW').filter(discounted_price__lt=10000)      
    elif data=='above' :
        topwears=Product.objects.filter(category='TW').filter(discounted_price__gt=10000) 
    if request.user.is_authenticated:
         totalitem=len(Cart.objects.filter(user=request.user))           
    return render(request, 'app/topwear.html',{'topwears':topwears,'totalitem':totalitem})

def bottomwear(request,data=None):
    totalitem=0
    if data == None:
        bottomwears=Product.objects.filter(category='BM')
    elif data=='jeans_ind' or data=='jeansjapan':
        bottomwears=Product.objects.filter(category='BM').filter(brand=data)
    elif data=='below' :
        bottomwears=Product.objects.filter(category='BM').filter(discounted_price__lt=10000)      
    elif data=='above' :
        bottomwears=Product.objects.filter(category='BM').filter(discounted_price__gt=10000) 
    if request.user.is_authenticated:
         totalitem=len(Cart.objects.filter(user=request.user))           
    return render(request, 'app/bottomwear.html',{'bottomwears':bottomwears,'totalitem':totalitem})
# def login(request):
#  return render(request, 'app/login.html')


def logout_view(request):
 
    logout(request)
    
    return redirect('login')
# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')


class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Conguration!! Registration Successfully')
            
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form})
    
@login_required   
def checkout(request):
    totalitem=0
    user=request.user
    add=Customer.objects.filter(user=user)   
    cart_item=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=75.0
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:                          
            tempamount=(p.quantity*p.product.discounted_price)
            amount+=tempamount
        total_amount=amount+shipping_amount
    # if request.user.is_authenticated:
    totalitem=len(Cart.objects.filter(user=request.user))        
    return render(request,'app/checkout.html',{'add':add,'total_amount':total_amount,'cart_items':cart_item,'totalitem':totalitem})

@login_required
def payment_done(request):
    # totalitem=0
    user=request.user
    # from check out page take custid 
    custid =request.GET.get('custid') 
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        # cart m se delete hoga ,product se nahi
        c.delete()  
    # total_amount = sum(item.total_cost for item in cart)
    return redirect('orders')  

# @login_required
# def payment_done(request):
#     user = request.user
#     custid = request.GET.get('custid')
#     customer = Customer.objects.get(id=custid)
#     cart = Cart.objects.filter(user=user)

#     # Calculate total amount dynamically
#     total_amount = sum(item.total_cost for item in cart)

#     for c in cart:
#         OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
#         c.delete()

#     # Pass total amount to template
#     return render(request, 'payment_done.html', {'total_amount': total_amount})


@method_decorator(login_required,name='dispatch')    
class ProfileView(View):
    def get(self,request):
        totalitem=0
        form=CustomerProfileForm()
        # if request.user.is_authenticated:
        totalitem=len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})
    def post(self,request):
        totalitem=0
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            user=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congratulation !! profile update successfully')
        totalitem=len(Cart.objects.filter(user=request.user))   
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary','totalitem':totalitem})    
            
            # ------------------------------------
