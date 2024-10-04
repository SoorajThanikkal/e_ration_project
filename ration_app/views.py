from django.shortcuts import redirect, render
from . models import reg,sreg,pro,shop,feed,super_user
from .models import *

# Create your views here.

import smtplib
import razorpay #import this
from django.conf import settings
from django.http import HttpResponse, JsonResponse #import this
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt #import this
from django.http import HttpResponseBadRequest #import this
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def index(request):
    return render(request,'index.html')
 
def shop_home(request):
    return render(request,'shop_home.html')
 
def user_home(request):
    return render(request,'user_home.html')

def admin_home(request):
    return render(request,'admin_home.html')

# user registration view

def user_register(request):
   if request.method =='POST':
      uploaded_file = request.FILES['file']
      fname = request.POST.get('rfname')
      address1 = request.POST.get('raddress')
      phone = request.POST.get('rcontact')
      num = request.POST.get('rnum')
      card = request.POST.get('rcard')
      passw = request.POST.get('rpass')
      reg(fullname=fname,address=address1,contact=phone,cardno=num,card=card,password=passw,image=uploaded_file).save()
      return render(request,'user_login.html')
   else:
      return render(request,'user_register.html')
   
   
# user login view

def user_login(request):
   if request.method=='POST':
      num = request.POST.get('rnum')
      passw = request.POST.get('rpass')
      cr = reg.objects.filter(cardno=num,password=passw)
      if cr:
         details = reg.objects.get(cardno= num, password = passw)
         cardno = details.cardno
         request.session['us']=cardno

         return render(request,'user_home.html')
      else:
         message="Invalid Username Or Password"
         return render(request,'user_login.html',{'me':message})
   else: 
      return render(request,'user_login.html')
   
   
# user profile view

def user_profile(request):
   c = request.session['us']
   cr = reg.objects.get(cardno=c)
   pfname = cr.fullname
   paddress = cr.address
   pcontact = cr.contact
   pcardno = cr.cardno
   pcard = cr.card
   pimage = cr.image
   return render(request,'user_profile.html',{'name':pfname,'address':paddress,'contact':pcontact,'cardno':pcardno,'card':pcard,'image':pimage})


# shop owner registration view

def shop_register(request):
   if request.method =='POST':
      fname = request.POST.get('rfname')
      address1 = request.POST.get('raddress')
      phone = request.POST.get('rcontact')
      num = request.POST.get('rnum')
      passw = request.POST.get('rpass')
      sreg(fullname=fname,address=address1,contact=phone,license=num,password=passw).save()
      return render(request,'shop_login.html')
   else:
      return render(request,'shop_register.html')
   
   
# shop owner login view

def shop_login(request):
   if request.method=='POST':
      num = request.POST.get('rnum')
      passw = request.POST.get('rpass')
      cr = sreg.objects.filter(license=num,password=passw)
      if cr:
         details = sreg.objects.get(license = num, password = passw)
         cardno = details.license
         request.session['os']=cardno

         return render(request,'shop_home.html')
      else:
         message="Invalid Username Or Password"
         return render(request,'shop_login.html',{'me':message})
   else: 
      return render(request,'shop_login.html')
   
   
# shop owner profile view


def shop_profile(request):
    c = request.session.get('os')
    cr = sreg.objects.get(license=c)
   #  pr = shop.objects.get(license=c)
    pfname = cr.fullname
    paddress = cr.address
    pcontact = cr.contact
    pcardno = cr.license
   #  plicense = pr.license
   #  pimage = pr.image
   #  ploc = pr.locality
   #  ptime = pr.time

    # Retrieve products associated with the shop owner
    products = pro.objects.filter(license=pcardno)

    return render(request, 'shop_profile.html', {
        'name': pfname,
        'address': paddress,
        'contact': pcontact,
        'cardno': pcardno,
      #   'license': plicense,
      #   'image': pimage,
      #   'locality': ploc,
      #   'time': ptime,
        'products': products 
    })


# add shops view


def add_shop(request):
    cardno=request.session['os']
    lino = cardno
    if request.method == 'POST':
        
        uploaded_file = request.FILES['file']
        loc = request.POST.get('rlocality')
        time = request.POST.get('rtime')

        # Check if the shop owner already has a shop
        
        if shop.objects.filter(license=lino).exists():
            message = "You can only register one shop."
            return render(request, 'shop_home.html', {'message': message})
        else:
            # Shop owner does not have a shop, register the shop
            shop(license=lino, image=uploaded_file, locality=loc, time=time).save()
            message = "Shop Registered Successfully !"
            return render(request, 'shop_home.html', {'me': message})
    else:
        return render(request, 'add_shop.html',{'lino':lino})


# add products view
   
def add_pro(request):
   cardno=request.session['os']
   lino = cardno
   if request.method =='POST':
      
      uploaded_file = request.FILES['file']
      name = request.POST.get('pname')
      apl = request.POST.get('papl')
      bpl = request.POST.get('pbpl')
      ay = request.POST.get('pay')
      stock = request.POST.get('pstock')
      price = request.POST.get('price')
      
      pro(license=lino,image=uploaded_file,name=name,apl=apl,bpl=bpl,ay=ay,stock=stock,price=price).save()
      message="Products Added Successfully"
      return render(request,'shop_home.html',{'me':message})
   else:
      return render(request,'add_pro.html',{'lino':lino})
   

# shops list view

def shops_view(request):
    data=shop.objects.all()
    return render(request,'shops_view.html',{'data':data})


# products list view

def pro_view(request, id):
    data = shop.objects.get(id=id)
    products = pro.objects.filter(license=data.license)  
    return render(request, 'pro_view.html', {'data': products})


# feedback form view

def feedback(request):
   if request.method =='POST':
      num = request.POST.get('rnum')
      fname = request.POST.get('rfname')
      msg = request.POST.get('rmsg')
      mail = request.POST.get('rmail')
      feed(cardno=num,fullname=fname,message=msg,email=mail).save()
      return render(request,'shop_home.html')
   else:
      return render(request,'feedback.html')


# update profile view

def edit_profile(request):
   c=request.session['us']
   cr = reg.objects.get(cardno=c)
   id = cr.id
   a = cr.fullname
   b = cr.address
   c = cr.contact
   d = cr.cardno
   e = cr.card
  
   return render(request,'edit_profile.html',{'id':id,'a':a,'b':b,'c':c,'d':d,'e':e})


def update_profile(request):
   if request.method=='POST':
      id = request.POST.get('rid')
      b = request.POST.get('rfname')
      c = request.POST.get('raddress')
      d = request.POST.get('rcontact')
      
      dt=reg.objects.get(id=id)
      
    
      dt.fullname = b
      dt.address = c
      dt.contact = d
      dt.save()
      return render(request,'user_home.html')


# add to cart view

   
from django.shortcuts import render, redirect, get_object_or_404
  # Ensure you import your models

# def addtocart(request, id):
#     user = request.session.get('us')  # Ensure this session key is set properly
#     if not user:
#         return redirect('user_login')  # Redirect to login if session user is not found

#     us = get_object_or_404(reg, cardno=user)  # Ensure the user exists

#     # Check if the product exists
#     product = get_object_or_404(pro, id=id)  # Ensure the product exists

#     # Use get_or_create to avoid the error
#     cart_item, created = add2cart.objects.get_or_create(
#         user=us,
#         product=product,
#         defaults={
#             'quantity': 1,  # Start with a quantity of 1
#         }
#     )
    
#     if not created:
#         # Increase quantity if item already exists in the cart
#         cart_item.quantity += 1
#         cart_item.save()
    
#     return redirect('cart_view')
from django.shortcuts import get_object_or_404, redirect, render

def addtocart(request, id):
    user = request.session.get('us')  # Ensure this session key is set properly
    if not user:
        return redirect('user_login')  # Redirect to login if session user is not found

    us = get_object_or_404(reg, cardno=user)  # Ensure the user exists

    # Check if the product exists
    product = get_object_or_404(pro, id=id)  # Ensure the product exists

    # Check available stock before adding to the cart
    desired_quantity = 1  # Default to adding one item; modify as needed (e.g., from request.POST)

    # Ensure the stock is available
    if product.stock <= 0:
        return render(request, 'error.html', {'message': 'Out of stock!'})

    # Decrement stock for all users
    product.stock -= desired_quantity
    product.save()

    # Add item to cart
    cart_item, created = add2cart.objects.get_or_create(
        user=us,
        product=product,
        defaults={
            'quantity': 0,  # Start with zero in the cart
        }
    )

    if created:
        # If this is a new cart item, set quantity and save
        cart_item.quantity = desired_quantity
        cart_item.save()
    else:
        # If item already exists in the cart, check the total quantity
        cart_item.quantity += desired_quantity
        cart_item.save()

    return redirect('cart_view')




def cart_view(request):
    # Assuming 'us' contains the user's session identifier
    user_cardno = request.session.get('us')

    # Get the user object using the 'cardno'
    user = get_object_or_404(reg, cardno=user_cardno)
    
    # Fetch all cart items for the logged-in user
    cart_items = add2cart.objects.filter(user=user)
  
    # Calculate total price of all items in the cart
    total_price = sum(float(item.product.price) * item.quantity for item in cart_items)
    
    # Render the cart view template with the cart items and total price
    return render(request, 'my_cart.html', {'cart_items': cart_items, 'total_price': total_price})

def error(request):
   return render(request,'error.html')
def orderpayment(request):
    email=request.session['email']
    cr=add2cart.objects.filter(c_email=email)
    return render(request,'orderpayment.html',{'a':cr})

def delete_record(request,id):
    data=add2cart.objects.get(id=id)
    data.delete()
    return redirect('cart_view')


# orders view

def view_orders(request):
#    c = request.session['os']
   cr = Payment.objects.all()

   return render(request,'view_orders.html',{'data':cr})




# payment history view

def pay_history(request):
   c = request.session['us']
   cr = reg.objects.get(cardno=c)
   user = Payment.objects.filter(user=cr)
   return render(request,'pay_history.html',{'data':user})

# admin registration view

def admin_reg(request):
   if request.method =='POST':
      uname = request.POST.get('rname')
      passw = request.POST.get('rpass')
      super_user(username=uname,password=passw).save()
      return render(request,'admin_login.html')
   else:
      return render(request,'admin_reg.html')
   
   
# admin login view

def admin_login(request):
   if request.method=='POST':
      uname = request.POST.get('rname')
      passw = request.POST.get('rpass')
      cr = super_user.objects.filter(username=uname,password=passw)
      if cr:
         details = super_user.objects.get(username= uname, password = passw)
         username = details.username
         request.session['cs']=username

         return render(request,'admin_home.html')
      else:
         message="Invalid Username Or Password"
         return render(request,'admin_login.html',{'me':message})
   else: 
      return render(request,'admin_login.html')
   
   
# users list view

def users_list(request):
    data=reg.objects.all()
    return render(request,'users_list.html',{'data':data})


def delete_record1(request,id):
    data=reg.objects.get(id=id)
    data.delete()
    return render(request,'admin_home.html')
   
   
# owners list view

def owners_list(request):
    data=sreg.objects.all()
    return render(request,'owners_list.html',{'data':data})


def delete_record2(request,id):
    data=sreg.objects.get(id=id)
    data.delete()
    return render(request,'admin_home.html')


# payment list view

def pay_list(request):
    data=Payment.objects.all()
    return render(request,'pay_list.html',{'data':data})


def delete_record3(request,id):
    data=Payment.objects.get(id=id)
    data.delete()
    return render(request,'admin_home.html')
      

# feedback list view

def feed_list(request):
    data=feed.objects.all()
    return render(request,'feed_list.html',{'data':data})


def delete_record4(request,id):
    data=feed.objects.get(id=id)
    data.delete()
    return render(request,'admin_home.html')


# payment view

# def payment(request):
#     cardno=request.session['us']
#     cr=add2cart.objects.filter(cardno=cardno)
#     totalprice = 0
    
#     for i in cr:
#      pay(fullname=i.fullname, cardno=i.cardno, card=i.card, proname=i.proname, price=i.price, license=i.license).save()
#      totalprice += int(i.price)
#      i.delete()
    
#     totalprice = int(totalprice*100)
#     amount=int(totalprice)
#     #amount=200
#     print('amount is',str(amount))
#     currency = 'INR'
#     #amount = 20000  # Rs. 200

#     # Create a Razorpay Order
#     razorpay_order = razorpay_client.order.create(dict(amount=amount,
#                                                        currency=currency,
#                                                        payment_capture='0'))
 
#     # order id of newly created order.
#     razorpay_order_id = razorpay_order['id']
#     callback_url = 'paymenthandler/'
 
#     # we need to pass these details to frontend.
#     context = {}
#     context['razorpay_order_id'] = razorpay_order_id
#     context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
#     context['razorpay_amount'] = amount
#     context['currency'] = currency
#     context['callback_url'] = callback_url
 
#     return render(request, 'payment.html', context=context)
 
# @csrf_exempt
# def paymenthandler(request):
 
#     # only accept POST request.
#     if request.method == "POST":
#         try:
           
#             # get the required parameters from post request.
#             payment_id = request.POST.get('razorpay_payment_id', '')
#             razorpay_order_id = request.POST.get('razorpay_order_id', '')
#             signature = request.POST.get('razorpay_signature', '')
#             params_dict = {
#                 'razorpay_order_id': razorpay_order_id,
#                 'razorpay_payment_id': payment_id,
#                 'razorpay_signature': signature
#             }
 
#             # verify the payment signature.
#             result = razorpay_client.utility.verify_payment_signature(
#                 params_dict)
#             if result is not None:
#                 amount = 20000  # Rs. 200
#                 try:
 
#                     # capture the payemt
#                     razorpay_client.payment.capture(payment_id, amount)
 
#                     # render success page on successful caputre of payment
#                     return render(request, 'pay_success.html')
#                 except:
 
#                     # if there is an error while capturing payment.
#                     return render(request, 'pay_failed.html')
#             else:
 
#                 # if signature verification fails.
#                 return render(request, 'pay_failed.html')
#         except:
 
#             # if we don't find the required parameters in POST data
#             return HttpResponseBadRequest()
#     else:
#        # if other than POST request is made.
#         return HttpResponseBadRequest()
    

# update product view

def edit_product(request,id):
   cr=pro.objects.get(id=id)
   id = cr.id
   license = cr.license
   a = cr.name
   b = cr.apl
   c = cr.bpl
   d = cr.ay
   e = cr.stock
   f = cr.price
  
   return render(request,'edit_product.html',{'id':id,'license':license,'a':a,'b':b,'c':c,'d':d,'e':e,'f':f})


def update_product(request):
   if request.method=='POST':
      id = request.POST.get('id')
      a = request.POST.get('name')
      b = request.POST.get('apl')
      c = request.POST.get('bpl')
      d = request.POST.get('ay')
      e = request.POST.get('stock')
      f = request.POST.get('price')

      
      dt=pro.objects.get(id=id)
      
    
      dt.name = a
      dt.apl = b
      dt.bpl = c
      dt.ay = d
      dt.stock = e
      dt.price = f

      dt.save()
      return render(request,'shop_home.html')






# views.py
from django.shortcuts import render, redirect
from django.conf import settings
import razorpay
from .models import Payment

def buy_product(request):
    if request.method == 'POST':
        total_amount = request.POST.get('total_amount')  # Get total amount from the form
        c = request.session['us']
        user = reg.objects.get(cardno=c)
          # Assuming user ID is stored in session
        products = "[{\"product_id\": 1, \"quantity\": 2}, {\"product_id\": 2, \"quantity\": 1}]"  # Example product data

        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        payment_order = client.order.create({
            'amount': int(float(total_amount) * 100),  # Amount in paise
            'currency': 'INR',
            'payment_capture': '1'
        })

        # Create the payment record
        payment = Payment.objects.create(
            user=user,
            total_amount=total_amount,
            razorpay_order_id=payment_order['id'],
            status='created',
            products=products  # Store product details as string
        )

        context = {
            'payment': payment_order,
            'razorpay_key_id': settings.RAZOR_KEY_ID,
            'price': total_amount
        }

        return render(request, 'buy.html', context)
    
    return redirect('cart_view')  # Redirect to cart if method is not POST

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        data = request.POST
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        payment = get_object_or_404(Payment, razorpay_order_id=razorpay_order_id)
        payment.razorpay_payment_id = razorpay_payment_id
        payment.razorpay_signature = razorpay_signature
        payment.status = 'successful'
        payment.save()
        return render(request, 'pay_success.html', {'payment': payment})
    return redirect('productlist')

