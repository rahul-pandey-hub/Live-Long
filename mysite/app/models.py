

from django.db import models
from djongo.models import ObjectIdField
from django.utils.html import mark_safe
import datetime
from django.core.validators import MaxLengthValidator,MinLengthValidator


STATE_CHOICE=(
    ('Andaman & Nicobar Island','Andaman & Nicobar Island'),
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chhattisgarh','Chhattisgarh'),
    ('Dadra & Nagar Haveli','Dadra & Nagar Haveli'),
    ('Daman and Diu','Daman and Diu'),
    ('Delhi','Delhi'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu & Kashmir','Jammu & Kashmir'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Lakshadweep','Lakshadweep'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Puducherry','Puducherry'),
    ('Panjab','Panjab'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttarakhand','Uttarakhand'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('West Bengal','West Bengal'),
)

class City(models.Model):
    idcity = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=45)

    class Meta:
        managed = True
        db_table = 'city'
    
    def __str__(self):
        return self.city_name


class Area(models.Model):
    id=models.AutoField(primary_key=True)
    area_name = models.CharField(max_length=100,unique=True)
    area_delivery_charges = models.IntegerField()
    city_idcity = models.ForeignKey(City,on_delete=models.SET_NULL,null=True, db_column='city_idcity')

    class Meta:
        managed = True
        db_table = 'area'
    
    def __str__(self):
        return self.area_name

class log(models.Model):
    email = models.CharField(primary_key=True,max_length=60,blank=False)
    pasword= models.CharField(max_length=60)
    type=models.CharField(max_length=60)
    

    class Meta:
        managed: True
        db_table = "log"

   
    def __str__(self):
        return self.email
class appointment(models.Model):
    id = models.CharField(primary_key=True,max_length=60,blank=False)
    emailpatient = models.CharField(max_length=60)
    emaildoc = models.CharField(max_length=60)
    phone_patient=models.CharField(max_length=60)
    phone_doc=models.CharField(max_length=60)
    appointment_time=models.CharField(max_length=60)
    doc_name=models.CharField(max_length=60)
    patient_name=models.CharField(max_length=60)
    time=models.CharField(max_length=60)
    price=models.IntegerField(default=100)
    appointment_Date=models.CharField(max_length=60)
    patient_remove=models.IntegerField(default=0)
    doctor_remove=models.IntegerField(default=0)
    class Meta:
        
        db_table = "appointment"
    def __str__(self):
        return self.id
class registration_patient(models.Model):
         id=models.AutoField(primary_key=True)
         first_name= models.CharField(max_length=60)
         last_name= models.CharField(max_length=60)
         gender= models.CharField(max_length=60)
         pasword= models.CharField(max_length=60)
         email= models.CharField(max_length=60)
         phone= models.CharField(max_length=60)
         age= models.CharField(max_length=60)
         image= models.CharField(max_length=60)
         address= models.CharField(max_length=60)
         problem = models.CharField(max_length=60)
         question= models.CharField(max_length=60)
         answer=models.CharField(max_length=60,default=None)

         pincode = models.ForeignKey(Area,null=True,on_delete=models.SET_NULL, db_column='area_id')
         class Meta:
             
             db_table = "registration_patient"
     
         def __str__(self):
             return self.email
class registration_doctor(models.Model):
        id=models.AutoField(primary_key=True)
        first_name=models.CharField(max_length=60) 
        last_name=models.CharField(max_length=60)
        gender=models.CharField(max_length=60)
        pasword=models.CharField(max_length=60)
        email=models.CharField(max_length=60)
        phone=models.CharField(max_length=60)
        select=models.CharField(max_length=60)
        time=models.IntegerField()
        image=models.CharField(max_length=60)
        address=models.CharField(max_length=60)
        dgree=models.CharField(max_length=60)
        price=models.IntegerField(default=0)
        payid=models.CharField(max_length=100,default=None)
        answer=models.CharField(max_length=100,default=None)
        question=models.CharField(max_length=100,default=None)
        class Meta:
             
             db_table = "registration_doctor"
     
        def __str__(self):
             return self.email
       
        

class ProductCategory(models.Model):
    
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    class Meta:
        managed: True
        db_table = "ProductCategory"

    def __str__(self):
        return self.title
    

class ProductSubCategory(models.Model):
    
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    pcategory = models.ForeignKey(ProductCategory,to_field='id',on_delete=models.SET_NULL,null=True)
    psubimage = models.ImageField(upload_to="psubcatImage",null=True,blank=True)
    class Meta:
        managed: True
        db_table = "ProductSubCategory"
    def __str__(self):
        return self.title
class Offer(models.Model):
    idoffer = models.AutoField(primary_key=True)
    offer_value = models.DecimalField(max_digits=2, decimal_places=0)
    offer_start_date = models.DateField()
    offer_end_date = models.DateField()
    offer_description = models.CharField(max_length=200,)

    class Meta:
        managed = True
        db_table = 'offer'
    
    def __str__(self):
        return self.offer_description

class Product(models.Model):
    
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    selling_price = models. FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    psubcategory= models.ForeignKey(ProductSubCategory,to_field='id',on_delete=models.SET_NULL,null=True)
   # brand = models.ForeignKey(Brand,on_delete=models.SET_NULL,null=True)
    product_image=models.ImageField(upload_to='productimg')
    offer_price = models.FloatField(default=0)
    offer_idoffer=models.ForeignKey(Offer,on_delete=models.SET_NULL,null=True,blank=True)
    # pincode = models.ForeignKey(Area,null=True,on_delete=models.SET_NULL, db_column='area_pincode')
    class Meta:
        managed: True
        db_table = "Product"
 
    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(registration_patient,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True,blank=True)
    offer_record = models.IntegerField(default=1,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
 
    def __str__(self):
     return str(self.user)
    
    @property
    def total_cost(self):
        return self.quantity *self.product.discounted_price
    

class Order(models.Model):
    idorder = models.AutoField(primary_key=True)
    orderfname = models.CharField(max_length=150,null=True)
    orderlname = models.CharField(max_length=150,null=True)
    orderemail = models.CharField(max_length=150,null=True)
    ordermobile = models.CharField(max_length=150,null=True)
    order_date = models.DateField(auto_now_add=True)
    cancel_order_date = models.DateTimeField(blank=True,null=True)
    order_delivery_date = models.DateTimeField(auto_now_add=True)
    order_delivery_address = models.TextField(null=False)
    city = models.CharField(max_length=150,null=False)
    total_amount = models.FloatField(null=False)
    order_payment_method = models.CharField(max_length=150,null=False)
    payment_id = models.CharField(max_length=250,blank=True,null=True)
    STATUS_CHOICES = (
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('On The Way', 'On The Way'),
        ('Delivered', 'Delivered')
    )
    order_status = models.CharField(max_length=150,choices=STATUS_CHOICES,default='Pending')
    message = models.TextField(blank=True,null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    is_cancel_order = models.IntegerField(default=0)
    area_pincode = models.ForeignKey(Area,on_delete=models.SET_NULL,null=True, db_column='area_pincode')
    user_iduser = models.ForeignKey(registration_patient, on_delete=models.SET_NULL,null=True, db_column='id')
    created_at = models.DateTimeField(null=True)

    class Meta:
        managed = True
        db_table = 'order'
    
    def __str__(self):
        return '{} - {}'.format(self.idorder,self.tracking_no)

class OrderedProduct(models.Model):
    order_idorder = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True,to_field='idorder')
    product_idProduct = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    price = models.FloatField(null=True)
    quantity = models.IntegerField(null=True)

    class Meta:
        managed = True
        db_table = 'ordered_product'
class Review(models.Model):
           idreview = models.AutoField(primary_key=True)
           subject = models.CharField(max_length=100,blank=True)
           review_description = models.TextField(max_length=500,blank=True)
           rating_value = models.FloatField(null=True)
           status = models.BooleanField(default=True)
           reviewDate = models.DateField(datetime.date.today,null=True)
           created_at = models.DateTimeField(auto_now_add=True)
           updated_at = models.DateTimeField(auto_now=True)
           user_iduser = models.ForeignKey(registration_patient,on_delete=models.SET_NULL,null=True,db_column='user_iduser')
           item_iditem = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,db_column='item_iditem')
       
           class Meta:
               managed = True
               db_table = 'review'
           
           def _str_(self):
               return '{} - review'.format(self.user_iduser.first_name)
       
    