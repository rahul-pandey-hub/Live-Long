from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.contrib import messages
import pymongo
from django.core.files.storage import FileSystemStorage

class log_info:
    a={}
client = pymongo.MongoClient('mongodb://localhost:27017/')
    #Define DB Name
dbname = client['admin']
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

def log_user(request):
    pasw=request.POST.get('password')
    email=request.POST.get('email')
    collection = dbname['log1']
    a1=collection.find_one({"email":email})
    if a1==None:
        messages.error(request,"The email address you entered isn't connected to an account")        
        return redirect('login')
    else:
         passw=a1['pasword']
         if passw==pasw:
            if a1["type"]=="doctor":
                  log_info.a=a1
                  return redirect('/doctor')
            else:
                 log_info.a=a1
                 return redirect('/patient')
         else:
            messages.error(request,'You Enter the wrong password')        
            return redirect('login')
    
def index(request): 
    return render(request,'index.html')
def hello(request):
    return render(request,'home.html')
def appointment(request):
    return render(request,'vid.html')
def patient(request):
    a1=log_info.a
    collection = dbname['mascot']
    collection2 = dbname['appointment']
    a=collection.find_one({"email":a1['email']})
    b=collection2.find_one({"email":a1['email']})
    return render(request,'patient.html',{'a':a,'b':b})
def reg(request):
    return render(request,'reg.html')
def doc(request):
    return render(request,'app.html')
def map(request):
    return render(request,'map.html')
def video(request):
    return render(request,'video.html')
def sub(request):
    a=request.GET.get("room","default")
    d={"room":a}
    return render(request,'sub.html',d)
def abc(request):
    return render(request,'abc.html')
def doctors(request):
    collection = dbname['mascot']
    a1=[]
    a=collection.find({})
    for i in a:
        a1.append(i)
    return render(request,'doctors.html',{"a":a1})
def login(request):
    return render(request,'login.html')
def doctor(request):
    a1=log_info.a
    collection = dbname['mascot2']
    print(a1)
    a=collection.find_one({"email":a1['email']})
    return render(request,'doctor.html',a)
def reg1(request):
    fname= request.POST.get('fname')
    lname= request.POST.get('lname')
    pasw=request.POST.get('pass','ni mila')
    email=request.POST.get('email','ni mila')
    phone=request.POST.get('phone','ni mila')
    select=request.POST.get('select')
    gender=request.POST.get('gender')
    #Define Collection
    collection = dbname['mascot']
    collection2=dbname['log1']
    a=collection2.find_one({"email":email})
    if a==None:    
         mascot_1={
             "first_name": fname,
             "last_name" : lname,
             "gender":gender,
             "pasword":pasw,
             "email":email,
             "phone":phone,
             "select":select,
             "time":None
         }
         collection.insert_one(mascot_1)
         
         a1=collection.find_one({"email":email})
         log_usr={
             "_id":a1['_id'],
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
    pasw=request.POST.get('passw','ni mila')
    email=request.POST.get('email','ni mila')
    phone=request.POST.get('phone','ni mila')
    select=request.POST.get('select')
    gender=request.POST.get('gender')
    #Define Collection
    collection = dbname['mascot2']
    collection2=dbname['log1']
    a=collection2.find_one({"email":email})
    if a==None:    
         mascot_1={
             "first_name": fname,
             "last_name" : lname,
             "gender":gender,
             "pasword":pasw,
             "email":email,
             "phone":phone,
             "select":select,
             "time":None
         }
         collection.insert_one(mascot_1)
         log_usr={
             "email":email,
             "pasword":pasw,
             "type":"doctor"
              }
         collection2.insert_one(log_usr)
    else:
        messages.error(request,'email is alredy taken by another user ')        
        return redirect('/')
    return render(request,'login.html')
def sub1(request):
    equest_file = request.FILES['upload'] if 'upload' in request.FILES else None
    if equest_file:
        upload = request.FILES['upload']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        print(file_url)
        return render(request, 'a.html', {'file_url': file_url})
    else:
        file_url = '/media/doc_YHAOITd.png'
        print(file_url)
        return render(request, 'a.html', {'file_url': file_url})