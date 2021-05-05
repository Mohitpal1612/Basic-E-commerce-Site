from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from django.views import View
# Create your views here.

class Index(View):
    def post(self,request):
        product=request.POST.get('product')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity-1
                    
                else:
                    cart[product]=quantity+1
            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1
        request.session['cart']=cart
        print('cart',request.session['cart'])
        return redirect('homepage')
       
    def get(self, request):
        cart=request.session.get('cart')
        if not cart:
            request.session['cart']={}
            
            products=None 
        categories=Category.get_all_categories()
        categoryID=request.GET.get('category')
        if(categoryID):
            products=Product.get_product_by_id(categoryID)
        else:
            products=Product.get_all_product()
        data={}
        data['products']=products
        data['categories']=categories
        print(request.session.get('customer_id'))
        return render(request,"index.html",data)

def signup(request):
    if request.method=='GET':
        return render(request, 'signup.html')
    # request.method=="POST":
    else:
        first_name=request.POST.get("firstname")
        last_name=request.POST.get("lastname")
        phone=request.POST.get("phone")      
        email=request.POST.get("email")
        password=request.POST.get("password")
        #now we will create object of customer
        
        c=Customer(first_name=first_name, last_name=last_name, 
                    phone=phone, email=email, password=password)

        em=c.isexists()
        if em:
            msg="Email already Registered"
            return render(request, 'signup.html',{"msg":msg})
        else:
            c.password=make_password(c.password)
            c.register() 
        return redirect('homepage')

class Login(View):
    def get(self,request):
        return render(request, "login.html")
    def post(self,request):
        email=request.POST.get('email')
        password=request.POST.get('password')
        c=Customer.get_customer_by_email(email)
        if c:
            flag=check_password(password,c.password)
            if flag:
                request.session['customer']=c.id
                return redirect('homepage')
            else:
                msg="invalid Credentials"
                return render(request,'login.html',{"msg":msg})

def logout(request):
    request.session.clear()
    return redirect('login')

class Cart(View):
    def get(self,request):
        ids=list(request.session.get('cart').keys())
        products=Product.get_products_by_id(ids)
        return render(request, "cart.html",{'products':products})
    
# def login(request):
#         if request.method=="GET":
#             return render(request, "login.html")
#         else:
#             email=request.POST.get('email')
#             password=request.POST.get('password')
#             c=Customer.get_customer_by_email(email)
#             if c:
#                 flag=check_password(password,c.password)
#                 if flag:
#                     return redirect('homepage')
#             else:
#                 msg="invalid Credentials"
#                 return render(request,'login.html',{"msg":msg})
