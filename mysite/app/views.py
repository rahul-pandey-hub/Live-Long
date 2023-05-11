from django.shortcuts import render,redirect
from django.views import View
from .models import *
from .models import registration_patient
from django.views.generic.list import ListView
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from datetime import date,datetime
import random
import json
from .models import appointment as app
# from django.contrib.auth.decorators import log_user_required
from django.utils.decorators import method_decorator
import pymongo
from django.core.files.storage import FileSystemStorage
import secrets
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .process import html_to_pdf
from django.template.loader import render_to_string
from django.views.generic import View


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


client = pymongo.MongoClient('mongodb://localhost:27017/')
    #Define DB Name
dbname = client['mysite4']


# function to generate the next sequence number
def get_next_sequence_number(sequence_name):
    counters = client.mysite.counters
    counter = counters.find_and_modify(query={'_id': sequence_name}, update={'$inc': {'seq': 1}}, new=True)
    return counter['seq']

# insert a new user document
# new_user = {'_id': get_next_sequence_number('userid'), 'name': 'John Doe'}
def logout(request):
     del request.session['email']
     return redirect('/')

def log_user(request):
    pasw=request.POST.get('password')
    email=request.POST.get('email')
    collection = dbname['log']
    a1=collection.find_one({"email":email})
    if a1==None:
        messages.error(request,"The email address you entered isn't connected to an account")        
        return redirect('login')
    else:
         passw=a1['pasword']
         if passw==pasw:
            if a1["type"]=="doctor":
                  request.session['email'] = email
                  return redirect('/doctor')
            else:
                 request.session['email'] = email
                 return redirect('/patient')
         else:
            messages.error(request,'You enter the wrong password')        
            return redirect('login')
def appoint(request):
    a2=request.session['email'] 
    #collection=dbname['mascot2']
    # a1=collection.find_one({"email":a2})
    emailpatient =a2
    emaildoc = request.POST.get("doc_email")
    request.session['doc_email'] = emaildoc
    collection = dbname['registration_doctor']
    a1=collection.find_one({"email":emaildoc})
    phone_patient=request.POST.get("phone")
    phone_doc=a1["phone"]
    appointment_time=request.POST.get("time")
    doc_name=a1["first_name"]
    patient_name=request.POST.get("name")

    time=request.POST.get("select")
    time=int(time)
    if time == 1:
         time = 60

    p=a1['price']
    
       
    if time==30:
         p=p*2
    elif time==45:
         p=p*3
    elif time == 1 :
         p=p*4
    abc=secrets.token_hex(2)
    appointment_Date=request.POST.get('date')
    date_format="%Y-%m-%d"
    
    appointment_Date = datetime.strptime(str(appointment_Date), date_format)
    print(appointment_Date)
    if appointment_Date:
         a=datetime.now()
         if a>appointment_Date:
              messages.error(request,"Please enter the valid Date")        
              return redirect('/doctor_info')
    appointment_Date=str(appointment_Date)
    print(appointment_Date)
    appointment_Date=appointment_Date.replace("00:00:00","")
    
    print(appointment_Date)
    
    collection2=dbname['appointment']
    b=0
    t=collection2.find({"emaildoc":emaildoc,"appointment_Date":appointment_Date,"appointment_time":appointment_time})
    for x in t:
          b+=x['time']
    b=b+time    
    if b > 60:
        messages.error(request,"The Data and Time you enter is already Booked by other")        
        return redirect('/doctor_info')
               


    
    appoint={
               "id":abc,
               "emailpatient":emailpatient,
               "emaildoc": emaildoc,
               "phone_patient":phone_patient,
               "phone_doc":phone_doc,
               "appointment_time":appointment_time,
               "doc_name":doc_name,
               "patient_name":patient_name,
               "time":time,
               "price":p,
               "image":a1['image'],
               "appointment_Date":appointment_Date,
                }
    # collection2.insert_one(appoint)
    # messages.success(request,"Your Appointment has been Booked!")
    return render(request,'appointmentcheckout.html',appoint)

def appointmentconfi(request):
     id=request.POST.get("id")
     emailpatient=request.POST.get("emailpatient")
     emaildoc =request.POST.get("emaildoc")
     phone_patient =request.POST.get("phone_patient")
     phone_doc=request.POST.get("phone_doc")
     appointment_time=request.POST.get("appointment_time")
     doc_name=request.POST.get("doc_name")
     patient_name=request.POST.get("patient_name")
     time=int(request.POST.get("time"))
     price=int(request.POST.get("price"))
     appointment_Date=request.POST.get("appointment_Date")
     collection2=dbname['appointment']
     data = {
                "id":id,
                "emailpatient":emailpatient,
                "emaildoc": emaildoc,
                "phone_patient":phone_patient,
                "phone_doc":phone_doc,
                "appointment_time":appointment_time,
                "doc_name":doc_name,
                "patient_name":patient_name,
                "time":time,
                "price":price,
                "appointment_Date":appointment_Date,
                "doctor_remove":0,
                "patient_remove":0
            }
     collection2.insert_one(data)
     
     

     return JsonResponse({'status':"Your appoitment has been placed successfully!"})
def doctor_info(request):
    if 'email' in request.session:
          email=request.POST.get('email',None)
          if email is None:
              email=request.session['doc_email']
          collection=dbname['registration_doctor']
          a2=request.session['email'] 
          a1=collection.find_one({"email":email})
          return render(request,"doctor_info.html",{"a1":a1,"a2":a2})
    else:
         return redirect('/')
def appointment(request):
    return render(request,'vid.html')
def patient(request):
    a1=request.session['email'] 
    collection = dbname['registration_patient']
    a=collection.find_one({"email":a1})
    collection2 = dbname['appointment']
    b=collection2.find({"emailpatient":a1,})
    b1=[]
    collection = dbname['registration_doctor']
    
    abcd=list(collection.find({}))
    productCategoryDetails = ProductCategory.objects.all()
    a2=[]
    for i in productCategoryDetails:
        a2.append(i)
    
    if b == None:
          return render(request,'patient.html',{"a":a,"b":b1,"data":a2,"doctors":abcd})
    else:
        for i in b:
                b1.append(i)
        return render(request,'patient.html',{"a":a,"b":b1,"data":a2,"doctors":abcd})
def reg(request):
    if 'email' in request.session:
        a2=request.session['email'] 
        if a2 is not None:
             collection = dbname['log']
             a1=collection.find_one({"email":a2})
             print(a1)
             if a1["type"]=="doctor":
                           
                           return redirect('/doctor')
             else:
                          
                          return redirect('/patient')
                  
                    
    return render(request,'reg.html')
def doc(request):
    return render(request,'app.html')
def map(request):
    return render(request,'map.html')
def video(request):
    return render(request,'video.html')
def sub(request):
    a=request.GET.get("room","default")
    
    collection=dbname['appointment']
    a=collection.find_one({'id':a})
    d={"room":a}
    if a is None:
          messages.error(request,'You Enter the Wrong Code')        
          return redirect('/appointment')
    else:
         return render(request,'sub.html',d)
         


def doctors(request):
    q = request.GET.get('q')
    collection = dbname['registration_doctor']
    a1=[]
    a=collection.find({})
    if q:
        object_list =registration_doctor.objects.filter((Q(first_name__icontains=q) | Q(last_name__icontains=q)))
        return render(request,'doctors.html',{"a":object_list})
    
    for i in a:
        a1.append(i)
    return render(request,'doctors.html',{"a":a1})
def login(request):
    if 'email' in request.session:
        a2=request.session['email'] 
        if a2 is not None:
             collection = dbname['log']
             a1=collection.find_one({"email":a2})
                  
             if a1["type"]=="doctor":
                           
                           return redirect('/doctor')
             else:
                          
                          return redirect('/patient')
                  
                    
    return render(request,'login.html')
def doctor(request):
    a1=request.session['email']
    collection = dbname['registration_doctor']
    collection2 = dbname['appointment']
    a=collection.find_one({"email":a1})
    b=list(collection2.find({"emaildoc":a1}))
    b1=[]
    a5=len(b)
    
    abc=0
    for i in b:
         abc=abc+i['doctor_remove']
    if a5 == abc:
         b=None 
    if b == None:
          return render(request,'doctor.html',{"a":a,"b":b1})
    else:
        for i in b:
                b1.append(i)
        return render(request,'doctor.html',{"a":a,"b":b1})  
def reg1(request):
    fname= request.POST.get('fname')
    lname= request.POST.get('lname')
    pasw=request.POST.get('pass')
    email=request.POST.get('email')
    e=email
    phone=request.POST.get('phone')
    p=phone
    firstArea = Area.objects.first()
    select=request.POST.get('select')
    gen=request.POST.get('gender')
    ans=request.POST.get("ans")
    age=request.POST.get('age')
    #Define Collection
    collection = dbname['registration_patient']
    collection2=dbname['log']
    a=collection2.find_one({"email":email})
    if a==None:    
         mascot_1=registration_patient.objects.create(first_name=fname,last_name=lname,gender=gen,pasword=pasw,email=e,phone=p,age=age,question=select,answer=ans,pincode=firstArea)
       
         mascot_1.save()
         
         a1=collection.find_one({"email":email})
         log_usr={
             "email":email,
             "pasword":pasw,
             "type":"patient"
              }
         collection2.insert_one(log_usr)
    else:
        messages.error(request,'Email is alredy taken by another user ')        
        return redirect('/')
    return render(request,'login.html')
def reg2(request):
    fname= request.POST.get('fname')
    lname= request.POST.get('lname')
    pasw=request.POST.get('passw')
    email=request.POST.get('email')
    phone=request.POST.get('phone')
    select=request.POST.get('select')
    gender=request.POST.get('gender')
    payid=request.POST.get('id',None)
    address=request.POST.get('address')
    que=request.POST.get('que')
    ans=request.POST.get('ans')
    #Define Collection
    collection = dbname['mascot2']
    collection2=dbname['log']
    a=collection2.find_one({"email":email})
    if a==None:    
         mascot_1=registration_doctor(
             first_name=fname,
             last_name= lname,
             gender=gender,
             pasword=pasw,
             email=email,
             phone=phone,
             select=select,
             time=None,
             payid=payid,
             address=address,
             question=que,
             answer=ans

         )
         mascot_1.save()
        
         log_usr={
             "email":email,
             "pasword":pasw,
             "type":"doctor"
              }
         collection2.insert_one(log_usr)
    else:
        messages.error(request,' The Email You entered into the doctor section is alredy taken by another user ')        
        return redirect('/')
    return render(request,'login.html')

def Update_Profile(request):
          if request.session['email'] == None:
              return redirect('/log')
          else:
              equest_file = request.FILES['upload'] if 'upload' in request.FILES else None
              file_url =None
              if equest_file:
                  upload = request.FILES['upload']
                  fss = FileSystemStorage()
                  file = fss.save(upload.name, upload)
                  file_url = fss.url(file)
              a1=request.session['email'] 
              fname= request.POST.get('fname')
              lname= request.POST.get('lname')
              phone=request.POST.get('phone')
              state=request.POST.get('state',None)
              problem=request.POST.get('problem',None)
              add=request.POST.get('address',None)
              mycol= dbname['registration_patient']
              myquery ={"email":a1}
              if file_url is not None:
                   newvalues = { "$set": { "image": file_url}}
                   mycol.update_one(myquery, newvalues)
              
              newvalues = { "$set": { 
                                    "first_name":fname,
                                    "last_name":lname,
                                    "phone":phone,
                                    "state":state,
                                    "problem":problem,
                                    "address":add} }
              mycol.update_one(myquery, newvalues)
              return redirect('/patient')
          
def Update_docinfo(request):
         a2=request.session['email']
         equest_file = request.FILES['upload'] if 'upload' in request.FILES else None
         file_url =None
         if equest_file:
             upload = request.FILES['upload']
             fss = FileSystemStorage()
             file = fss.save(upload.name, upload)
             file_url = fss.url(file)
         fname= request.POST.get('fname')
         lname= request.POST.get('lname')
         phone=request.POST.get('phone')
         select=request.POST.get('select')
         add=request.POST.get('address')
         price=int(request.POST.get('price',None))
         degree=request.POST.get('degree',None)
         mycol= dbname['registration_doctor']
         myquery ={"email":a2}
         if file_url is not None:
               newvalues = { "$set": { "image": file_url}}
               mycol.update_one(myquery, newvalues)
         
         newvalues = { "$set": { 
                                "first_name":fname,
                                "last_name":lname,
                                "phone":phone,
                                "price":price,
                                "select":select,
                                "dgree":degree,
                                "address":add} }
         mycol.update_one(myquery, newvalues)
         return redirect('/doctor')
    
def doc_profile(request):
    
     a2=request.session['email']
    
     collection2 = dbname['registration_doctor']
     a2=collection2.find_one({"email":a2})
     return render(request,'doc_details.html',a2)
        
    
def User_profile(request):
    
    
    if 'email' in request.session:
         a1= request.session['email']
         
         collection = dbname['registration_patient']
         a=collection.find_one({"email":a1})
         if a is None:
                   return redirect('/login')
         else:
                    
                    return render(request,'profile.html',a)
    else:
         return redirect('/login')

#new
class ProductSubCategoryListView(ListView):
    model = ProductSubCategory
    template_name = 'medicene.html'

    def get_queryset(self,*args, **kwargs):
        q = self.request.GET.get('q')
        getCategory = ProductCategory.objects.get(id=int(self.kwargs['prodCatId']))
        collection2 = dbname['ProductSubCategory']
        #a2=collection2.find({"pcategory":getCategory.id})
        if self.kwargs.get('prodCatId'):
           # ProductSubCategory.objects.filter(pcategory=getCategory.id)
            object_list = ProductSubCategory.objects.filter(pcategory=getCategory.id)
            # a1=collection2.find({"pcategory":getCategory.id})
            # for i in a1:
            #      object_list.append(i)
            print(object_list)
            
            if q:
                object_list = self.model.objects.filter((Q(title__icontains=q) | Q(description__icontains=q)),pcategory=getCategory.id)
            else:
                #object_list = ProductSubCategory.objects.filter(pcategory=getCategory.id)
                object_list = ProductSubCategory.objects.filter(pcategory=getCategory.id)
                # a1=collection2.find({"pcategory":getCategory.id})
                # for i in a1:
                #      object_list.append(i)
                print(object_list)
        return object_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productCategory"] = ProductCategory.objects.get(id=self.kwargs['prodCatId'])
        return context

class ProductListView(ListView):
    model = Product
    template_name = 'med.html'

    def get_queryset(self,*args, **kwargs):
        q = self.request.GET.get('q')
        #collection2 = dbname['Product']
        getCategory = ProductSubCategory.objects.get(id=int(self.kwargs['prodSubId']))
        print(getCategory)
        if self.kwargs.get('prodSubId'):
            #object_list = Product.objects.filter(psubcategory=getCategory.id)
            object_list = object_list = Product.objects.filter(psubcategory=getCategory.id)
            if q:
                object_list = self.model.objects.filter((Q(title__icontains=q) | Q(description__icontains=q)),psubcategory=getCategory.id)
            else:
                 object_list =object_list = Product.objects.filter(psubcategory=getCategory.id)
        return object_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["productCat"] = ProductCategory.objects.get(id=self.kwargs['prodCatId'])
        context["prodSubCat"] = ProductSubCategory.objects.get(id=self.kwargs['prodSubId'])

        return context
def productDetailsViewAllData(request,prodCatId,prodSubId,prodId):
#  collection2 = dbname['Product']
#  print(prodId)
#  productDetailsData=collection2.find_one({"id":prodId})
#  print(productDetailsData)
 productDetailsData = Product.objects.get(id=int(prodId))
 r1 = Review.objects.filter(item_iditem=int(prodId))
 u1 = registration_patient.objects.get(email=request.session['email'])
 try:
       r2 = Review.objects.get(item_iditem=int(prodId),user_iduser=u1.id)
 except:
      r2=None
 userId = u1.id
 try:
   orders = Order.objects.get(user_iduser=userId,order_status='Delivered')
   abcd=orders.order_status
   print(orders)
 except:
    abcd=None
 
 if abcd != 'Delivered':
      abcd=None
      
 data = {
  'productDetailsData':productDetailsData,
  'currentUserDetails':u1,
  'usersReview':r1,
  'currentUserReview':r2,
  'orders':abcd
 }
 return render(request,'mediceneDetail.html',data)

def reviewsubmit(request,item_id):
    url = request.META.get('HTTP_REFERER')
    if 'email' in request.session:
        u1 = registration_patient.objects.get(email=request.session['email'])
        userId = u1.id
        try:
            if(Review.objects.get(user_iduser=userId,item_iditem=item_id)):
                r1 = Review.objects.get(user_iduser=userId,item_iditem=item_id)
                ratingValue = request.POST.get('rating')
                if(not ratingValue):
                    r1.rating_value = 0
                else:
                    r1.rating_value = request.POST.get('rating')
                r1.subject = request.POST.get('subject')
                r1.review_description = request.POST.get('review')
                r1.reviewDate = date.today()
                r1.save()
                messages.success(request,'Review updated successfully!')
                return redirect(url)
        except:
            if request.method == "POST":
                userReview = Review()
                ratingValue = request.POST.get('rating')
                if(not ratingValue):
                    userReview.rating_value = 0
                else:
                    userReview.rating_value = request.POST.get('rating')
                userReview.subject = request.POST.get('subject')
                userReview.review_description = request.POST.get('review')

                userReview.user_iduser = registration_patient.objects.get(id=u1.id)
                userReview.item_iditem = Product.objects.get(id=item_id)
                userReview.reviewDate = date.today()
                userReview.save()
                messages.success(request,'Review added successfully!')
            return redirect(url)
    else:
        messages.error(request,'Login to continue!')
        return redirect(url)


#cart

def cartUser(request): 
    u1 = registration_patient.objects.get(email=request.session['email'])
    userId = u1.id
    cart1 = Cart.objects.filter(user=userId)
    data = {
        'userCart':cart1
    }
    if 'email' not in request.session:
        messages.error(request,'Login to continue!')
        return redirect('/patient')
    return render(request,'cart.html',data)

def addToCart(request):
  if request.method == "POST":
        if 'email' in request.session:
            u1 = registration_patient.objects.get(email=request.session['email'])
            prod_id = int(request.POST.get('prod_id'))
            ProductCheck = Product.objects.get(id=prod_id)
            if(ProductCheck):
                if(ProductCheck.offer_idoffer):
                    if(Cart.objects.filter(user=u1.id,product=prod_id)):
                        return JsonResponse({'data':"Product already in cart!"})
                    else:
                        prod_qty = int(request.POST.get('prod_qty'))
                        Cart.objects.create(user=registration_patient.objects.get(id=u1.id),product=Product.objects.get(id=prod_id),quantity=prod_qty,offer_record=0)
                        return JsonResponse({'status':"Product Added Successfully!"})
                elif(not ProductCheck.offer_idoffer):
                    if(Cart.objects.filter(user=u1.id,product=prod_id)):
                        return JsonResponse({'data':"Product already in cart!"})
                    else:
                        prod_qty = int(request.POST.get('prod_qty'))
                        Cart.objects.create(user=registration_patient.objects.get(id=u1.id),product=Product.objects.get(id=prod_id),quantity=prod_qty)
                        return JsonResponse({'status':"Product Added Successfully!"})
            else:
              return JsonResponse({'data':"No Such Product Found!"})
        else:
            return JsonResponse({'data':"Login to continue!"})
  return redirect('patient')

def deleteCartProduct(request):
    if request.method == "POST":
        product_id = int(request.POST.get('product_id'))
        u1 =registration_patient.objects.get(email=request.session['email'])
        userId = u1.id
        if(Cart.objects.filter(user=userId, product=product_id)):
            cartitem = Cart.objects.get(product=product_id,user=userId)
            cartitem.delete()
        return JsonResponse({'status':"Product removed from cart!"})
    return redirect('cart')

def updateUserCart(request):
    if request.method == "POST":
        
        product_id = int(request.POST.get('product_id'))
        u1 =registration_patient.objects.get(email=request.session['email'])
        userId = u1.id
        if(Cart.objects.filter(user=userId, product=product_id)):
            product_qty = int(request.POST.get('product_qty'))
            cart = Cart.objects.get(product=product_id,user=userId)
            cart.quantity = product_qty
            cart.save()
            return JsonResponse({'status':"Cart updated successfully", 'error': 'errorrerer'})
    return redirect('home')


#CHECKOUT
def checkoutProduct(request):
    u1 = registration_patient.objects.get(email=request.session['email'])
    c1 = City.objects.all()
    a1 = Area.objects.all()
    a3 = Area.objects.get(id=u1.pincode.id)
    a2 = Area.objects.filter(city_idcity=u1.pincode.id)
    delcharges = 0
    userId = u1.id
    cartproducts = Cart.objects.filter(user=userId)
    cartOfferProduct = Cart.objects.filter(user=userId,offer_record=0)
    grand_total = 0
    total_offer_price = 0
    total_price = 0
    if(cartOfferProduct):
        for i in cartOfferProduct:
            total_offer_price = total_offer_price + i.product.offer_price * i.quantity
    else:
        total_offer_price = 0
    
    for item in cartproducts:
        total_price = total_price + (item.product.selling_price * item.quantity)

    grand_total = (total_price) - total_offer_price  
    context = {'cartproducts':cartproducts,'total_price':total_price, 'city':c1, 'area':a2,'current_user':u1,'delArea':delcharges,'offerPrice':total_offer_price,'grandTotal':grand_total}
    
    return render(request,'productcheckout.html',context)

#order
def change_city(request):
    if request.method == "POST":
        areaname = request.POST.get('cityname')
        a2=City.objects.get(city_name=areaname)
        print(a2)
        a1 = Area.objects.filter(city_idcity=a2.idcity).values()
        print(a1[1])
        a3=[]
        b=len(a1)
        for i in range(0,b):
             
             a=a1[i]
             
             a3.append(a)
        
        abc={'a':a3}
        return HttpResponse(json.dumps(abc), content_type='application/json')
    return redirect('/checkout/')
     
def changecharges(request):
    if request.method == "POST":
        areaname = request.POST.get('areaname')
        a1 = Area.objects.get(area_name=areaname)
        return JsonResponse({'status':a1.area_delivery_charges})
    return redirect('/checkout/')

def placeorder(request):
    if request.method == "POST":
        u1 = registration_patient.objects.get(email=request.session['email'])
        userId = u1.id
        neworder = Order()
        neworder.user_iduser = registration_patient.objects.get(id=userId)
        neworder.orderfname = request.POST.get('fname')
        neworder.orderlname = request.POST.get('lname')
        neworder.orderemail = request.POST.get('email')
        neworder.ordermobile = request.POST.get('mobile')
        neworder.order_delivery_address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        a1 = Area.objects.get(area_name=request.POST['area1'])
        neworder.area_pincode = Area.objects.get(id=a1.id)
        neworder.order_payment_method = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_id')

        userpincode = request.POST.get('pincode')

        cart = Cart.objects.filter(user=userId)
        cartOfferProduct = Cart.objects.filter(user=userId,offer_record=0)
        total_offer_price = 0
        if(cartOfferProduct):
            for i in cartOfferProduct:
                total_offer_price = total_offer_price + i.product.offer_price * i.quantity
        else:
            total_offer_price = 0

        cart_total_price = 0
        for item in cart:
            cart_total_price = cart_total_price + (item.product.selling_price * item.quantity)

        cart_total_price = (cart_total_price - total_offer_price)
        neworder.total_amount = cart_total_price + a1.area_delivery_charges

        trackno = 'Livelong'+str(random.randint(1111111,9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'LiveLong'+str(random.randint(1111111,9999999))
        neworder.tracking_no = trackno

        currentDateTime2 = datetime.now()
        neworder.created_at = datetime(currentDateTime2.year,currentDateTime2.month,currentDateTime2.day,currentDateTime2.hour,currentDateTime2.minute,currentDateTime2.second)
        neworder.save()

        neworderitem = Cart.objects.filter(user=userId)
        for item in neworderitem:
            OrderedProduct.objects.create(
                order_idorder = neworder,
                product_idProduct = item.product,
                price = item.product.selling_price,
                quantity = item.quantity
            )

        Cart.objects.filter(user=userId).delete()
        u1.user_address = neworder.order_delivery_address
        u1.pincode = neworder.area_pincode
        u1.save()

        
        payMode = request.POST.get('payment_mode')
        if(payMode == "Paid by Razorpay" or payMode == "paid by paypal"):
            return JsonResponse({'status':"Your order has been placed successfully!"})
        else:
            messages.success(request,"Your order has been placed successfully!")
    
    return redirect('/patient')
def my_appointment(request):
    u1 = registration_patient.objects.get(email=request.session['email'])
    email1=u1.email
    print(email1)
    products = app.objects.filter(emailpatient=email1)
    
    context = {'userOrderData':products}
    
    return render(request,'user-appointment.html',context)
def doc_appointment(request):
    u1 = registration_doctor.objects.get(email=request.session['email'])
    email1=u1.email
    print(email1)
    products = app.objects.filter(emaildoc=email1)
    
    context = {'userOrderData':products}
    
    return render(request,'doc-appointment.html',context)
     

def orderpage(request):
    u1 = registration_patient.objects.get(email=request.session['email'])
    userId = u1.id
    orders = Order.objects.filter(user_iduser=userId)
    context = {'userOrderData':orders}
    return render(request,'user_order.html',context)

def orderdetailspage(request,t_no):
    u1 = registration_patient.objects.get(email=request.session['email'])
    userId = u1.id
    order = Order.objects.filter(tracking_no=t_no).filter(user_iduser=userId).first()
    orderitems = OrderedProduct.objects.filter(order_idorder=order)
    context = {'userOrderData':order,'userOrderDetails':orderitems}
    return render(request,'userOrderDetails.html',context)
def appointmentdetailspage(request,t_no):
    u1 = registration_patient.objects.get(email=request.session['email'])
    
    order = app.objects.get(id=t_no)
    userId = order.emaildoc
    image=registration_doctor.objects.get(email=userId)
    context = {'userOrderData':order,'image':image.image}
    return render(request,'userAppointmentDetail.html',context)

def forget(request):
     return render(request,'forget.html')
class orderInvoicePdf(View):
    def get(self, request, *args, **kwargs):
        totalOfferPrice = 0
        totalPrice = 0
        u2 = registration_patient.objects.get(email=request.session['email'])
        u1 = u2.id
        o1 = Order.objects.get(tracking_no=self.kwargs['t_no'])

        od1 = OrderedProduct.objects.filter(order_idorder=o1.idorder)
        if od1:
            for i in od1:
                totalOfferPrice = totalOfferPrice + i.product_idProduct.offer_price
        else:
            totalOfferPrice=0

        for i in od1:
            totalPrice = totalPrice + i.product_idProduct.selling_price

        data = {
            'order':o1,
            'orderDetails':od1,
            'totalOfferPrice':totalOfferPrice,
            'totalPrice':totalPrice
        }
        open('templates/temp.html',"w").write(render_to_string("invoice.html",{"data":data}))

        pdf = html_to_pdf('temp.html')

        return HttpResponse(pdf,content_type='application/pdf')
def cancelappointment(request):
     id=request.POST.get('id')
     print(id)
     mycol=dbname["appointment"]
     myquery={"id":id}
     newvalues = { "$set": { "patient_remove": 1}}
     mycol.update_one(myquery, newvalues)
     return JsonResponse({'status':"Appointment Remove successfully!"})
def canceldocappointment(request):
     id=request.POST.get('id')
     print(id)
     mycol=dbname["appointment"]
     myquery={"id":id}
     newvalues = { "$set": { "doctor_remove": 1}}
     mycol.update_one(myquery, newvalues)
     return JsonResponse({'status':"Appointment Remove successfully!"})

def orderCancel(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        
        userOrder = Order.objects.get(tracking_no=order_id)
        
        if(userOrder.order_payment_method == "COD"):
            userOrder.is_cancel_order = 1
            userOrder.cancel_order_date = datetime.now()
            # orderedItemDelete = OrderedProduct.objects.get(order_idorder=userOrder.idorder)
            # print(orderedItemDelete)
            # orderedItemDelete.delete()
            mycol =dbname["ordered_product"]

            myquery = { "order_idorder":userOrder.idorder }

            mycol.delete_one(myquery)
            userOrder.save()
            return JsonResponse({'status':"Order Cancel successfully!"})
    return redirect('/patient')
def report(request):
     return render(request,'report.html')
def change_password(request):
     email=request.POST.get('email',None)
     ques=request.POST.get('question')
     ans=request.POST.get('ans')
     Npass=request.POST.get('npass',None)
     cpass=request.POST.get('cpass',None)
     if Npass is not None:
          a=log.objects.get(email=email)
          
          if a is not None:
               b=None
               if a.type=='doctor':
                    b=registration_doctor.objects.get(email=email)
                    mycol= dbname['registration_doctor']
                    myquery ={"email":a.email}
               else:
                    b=registration_patient.objects.get(email=email)
                    mycol= dbname['registration_patient']
                    myquery ={"email":a.email}
               if b.question == ques:
                    if b.answer == ans:
                       newvalues = { "$set": { "pasword":Npass }}
                       mycol.update_one(myquery, newvalues)
                       
                       return redirect('login')
                     
              
              
                   
                         
          else:
                    
                    messages.error(request,'You enter wrong email')     
                    
                   
            
    
         
     

def show_product(request):
  p=Product.objects.all()
  data={'products':p,   
      }
  return render(request,'productReport.html',data)

def pdf_report_create(request):
    products = Product.objects.all()
    context = {'products': products}


    template = get_template('productReport copy.html')
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')



def show_product_category(request):
  pc=ProductCategory.objects.all()
  data={'products':pc,   
      }
  return render(request,'categoryReport.html',data)

def pdf_report_create_category(request):
    products =ProductCategory.objects.all()
    context = {'products': products}


    template = get_template('categoryReport copy.html')
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')

  


  
def show_product_subcategory(request):
  p=ProductSubCategory.objects.all()
  data={'products':p,   
      }
  return render(request,'subCategoryReport.html',data)

def pdf_report_create_subcategory(request):
    products = ProductSubCategory.objects.all()
    context = {'products': products}


    template = get_template('subCategoryReport copy.html')
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')

def show_order(request):
   global sdate
   global edate
   sdate = request.POST.get('start_date',None)
   edate = request.POST.get('end_date',None)
   if sdate is not None and edate is not None:
        products = Order.objects.filter(order_date__range=(sdate,edate),is_cancel_order=0)
   else:
        products = Order.objects.filter(is_cancel_order=0)
   global data
   data={'products':products}
   return render(request,'orderReport.html',data)

def pdf_report_create_order(request):
    # products = OrderedProduct.objects.all()
    # context = {'products': products}


    # template = get_template('orderReport.html')
    # html = template.render(context)
    # result = BytesIO()

    # pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    # if not pdf.err:
    #     return HttpResponse(result.getvalue(), content_type='application/pdf')
    # else:
    #     return HttpResponse('Error')
    if sdate is not None and edate is not None:
            o = Order.objects.filter(order_date__range=(sdate,edate),is_cancel_order=0)
    else:
            o = Order.objects.filter(is_cancel_order=0)
    data = {'products': o}


    template = get_template('orderReport copy.html')
    html = template.render(data)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')



def show_cart(request):
  p=Cart.objects.all()
  data={'products':p,   
      }
  return render(request,'cartReport.html',data)
def show_appointmet(request):
      products = app.objects.filter()
      
      data={'products':products}
      return render(request,'appointment_report.html',data)
def pdf_appointmentReport_create(request):
    products = app.objects.all()
    context = {'products': products}


    template = get_template('appointment_report copy.html')
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')
     
     

def pdf_report_create_cart(request):
    products = Cart.objects.all()
    context = {'products': products}


    template = get_template('cartReport copy.html')
    html = template.render(context)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')
    
def show_doctors_appointmet(request):
      global email1
      email1 = request.POST.get('email',None)
      print(email1)
      if email1 is None:
           
            products = registration_doctor.objects.filter()
            
            data={'products':products}
            return render(request,'doctors_appointment_report.html',data)
      else:
            
            products = app.objects.filter(emaildoc=email1)
            
            data={'app':products}
            return render(request,'doctors_appointment_report.html',data)

def pdf_doctors_appointment_report(request):
    
    products = app.objects.filter(emaildoc=email1)
            
    data={'app':products}

    template = get_template('doctors_appointment_report copy.html')
    html = template.render(data)
    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('ISO-8859-1')), result)

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse('Error')
    
