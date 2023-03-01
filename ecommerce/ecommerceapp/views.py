from django.shortcuts import render,redirect
from ecommerceapp.models import Contact, Product, Orders, OrderUpdate
from django.contrib import messages
from math import ceil
from ecommerceapp import keys
from django.conf import settings
MERCHANT_KEY = keys.MK
import json
from django.views.decorators.csrf import csrf_exempt
from PayTm import Checksum


# Create your views here.
def index(request):
    allproducts = []
    category_products = Product.objects.values('category','id')
    catgs = {item['category'] for item in category_products}
    for cat in catgs:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n/4)-(n//4))
        allproducts.append([prod,range(1,nSlides), nSlides])

    params = {'allproducts':allproducts}
    return render(request,'index.html',params)

def contact(request):
    if request.method=="POST":
        name= request.POST.get("name")
        email= request.POST.get("email")
        phone= request.POST.get("phone")
        desc= request.POST.get("desc")
        data = Contact(name=name,email=email,phone=phone,desc=desc) 
        data.save()
        messages.info(request,"We will get back to you soon")

        return render(request,'contact.html')
    return render(request,"contact.html")


def about(request):
    return render(request,'about.html')


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login/')
    if request.method=="POST":
        items_json=request.POST.get('itemsJson')
        name=request.POST.get('name','')
        amount =request.POST.get('amt')
        email =request.POST.get('email','')
        address1 =request.POST.get('address1','')
        address2 =request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zip_code = request.POST.get('zip_code','')
        phone = request.POST.get('phone','')
        Order= Orders(items_json=items_json,name=name,amount=amount,
                      email=email,address1=address1,address2=address2,
                      city=city,zip_code=zip_code,phone=phone)
        print(amount)
        Order.save()
        update = OrderUpdate(order_id=Order.order_id,update_desc="Your order has been placed")
        update.save()
        thank = True


#payment integration

        id = Order.order_id
        oid = str(id)+"shopycart"
        param_dict = {
            'MID': keys.MID,
            'ORDER_ID': oid,
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http:127.0.0.:8080/handlerequest/',

        }
        param_dict['CHECKSUMHASH']= Checksum.generate_checksum
        (param_dict, MERCHANT_KEY)
        return render(request,'paytm.html',{'param_dict':param_dict})

    return render(request,'checkout.html')

@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i]:form[i]
        if i == "CHECKSUMHASH":
            checksum = form[i]
        
    verify = Checksum.verify_checksum(response_dict,MERCHANT_KEY,checksum)
    if verify:
        if response_dict['RESPCODE']=='01':
            print('Thank you. Your Order successfully delivered..!!')
            a = response_dict['ORDERID']
            b = response_dict['TXNAMOUNT']
            rid = a.replace("shopycart","")
            print(rid)
            filter2 = Orders.objects.filter(order_id=rid)
            print(filter2)
            print(a,b)
            for j in filter2:
                j.oid =a
                j.amountpaid = b
                j.paymentstatus = "PAID"
                j.save()
                print("Run agede function")
            
        else:
            print("Order was not successful" + response_dict['RESPMSG'])
    return render(request, 'paymentstatus.html', {'response': response_dict})


def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Login & Try Again")
        return redirect('/auth/login/')
    currentuser = request.user.username
    items=Orders.objects.filter(email=currentuser)
    rid=""
    for i in items:
        myid=i.oid
        rid = myid.replace("shopycart","")
        print(rid)
    status = "Maycha Bhok" #OrderUpdate.objects.filter(order_id=int(rid))
    print(status[::-1])
    context = {"items":items,"status":status}
    print(currentuser)

    return render(request,'profile.html',context)