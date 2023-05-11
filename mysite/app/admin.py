from django.contrib import admin

from .models import ( log,appointment,ProductCategory,ProductSubCategory,
                     Product,registration_patient,Cart,City,Area,OrderedProduct,
                     Order,registration_doctor
)
@admin.register(log)
class UserAdmin(admin.ModelAdmin):
    list_display = ( "email","pasword","type")

@admin.register(registration_patient)
class UserAdmin(admin.ModelAdmin):
    list_display = (  
        
        "id",
        "first_name",
         "last_name",
         "gender",
         "pasword",
         "email",
         "phone",
         "age",
         "image",
         "address",
         "problem",
         "question",
         "answer")
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title','description']
    search_fields=('id','title',)

@admin.register(ProductSubCategory)
class ProductSubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','psubimage',"pcategory"]
    search_fields=('id','title',)
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','description','product_image','psubcategory']
    search_fields=('id','title',)
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity','created_at']
    list_per_page=5
    search_fields=('id',)

@admin.register(appointment)
class UserAdmin(admin.ModelAdmin):
    list_display = ( "id","emailpatient","emaildoc","phone_patient",
                    "phone_doc","appointment_time","doc_name","patient_name","time","appointment_Date")
    search_fields=('id','emailpatient','emaildoc',)
@admin.register(City)
class CityModelAdmin(admin.ModelAdmin):
    list_display = ['idcity','city_name']
    list_per_page=5
    search_fields=('city_name',)

@admin.register(Area)
class AreaModelAdmin(admin.ModelAdmin):
    list_display = ['id','area_name','area_delivery_charges','city_idcity']
    list_per_page=5
    search_fields=('area_name',)
    
@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display=['idorder','orderfname','orderlname','orderemail','ordermobile','order_date','cancel_order_date','order_delivery_date','order_delivery_address','city','total_amount','order_payment_method','payment_id','order_status','message','tracking_no','is_cancel_order','area_pincode','user_iduser','created_at']
    list_per_page=5
    search_fields=('tracking_no',)

@admin.register(OrderedProduct)
class OrderProductModelAdmin(admin.ModelAdmin):
    list_display=['order_idorder','product_idProduct','price','quantity']
    list_per_page=5
    search_fields=('order_idorder',)
@admin.register(registration_doctor)
class registration_doctor(admin.ModelAdmin):
        list_display = (  
        
        "id",
        "first_name",
         "last_name",
         "gender",
         "pasword",
         "email",
         "phone",
         "select",
         
         "address",
         "dgree",
         "price",
         "answer")