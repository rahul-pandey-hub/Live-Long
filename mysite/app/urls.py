
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   # path('admin/', admin.site.urls),
   # path('', views.index,name="index"),
   # path('video',views.video,name="video"),
    path('appointment',views.appointment,name="a"),
    path('patient',views.patient,name="patient"),
    path('doc_appointment',views.doc,name="doc"),
    path('sub',views.sub,name="sub"),
    path('add-to-cart',views.addToCart,name='add-to-cart'),
    path('doc',views.doctors,name="doctors"),
    path('login',views.login,name="login"),
    path('',views.reg,name="reg"),
    path('doctor',views.doctor,name="reg"),
    path('reg1',views.reg1,name="reg1"),
    path('reg2',views.reg2,name="reg2"),
    path('log_user',views.log_user,name="log"),
    path('logout',views.logout,name="log"),
    #path('abc',views.abc,name="log1"),
    path('Update_Profile',views.Update_Profile,name="Update_Profile"),
    path('doctor_info',views.doctor_info,name="log1"),
    path('doc_profile',views.doc_profile,name="log1"),
    path('appoint',views.appoint,name="log1"),
    path('User_profile',views.User_profile,name="User_profile"),
    path('Update_docinfo',views.Update_docinfo,name="Update_docinfo"),
    path('report/',views.report,name='report'),
    path('productCategory/<int:prodCatId>/',views.ProductSubCategoryListView.as_view(),name='productCat'),
    path('productCategory/<int:prodCatId>/<int:prodSubId>/',views.ProductListView.as_view(),name='productOfSubCat'),
    path('productCategory/<int:prodCatId>/<int:prodSubId>/<int:prodId>/',views.productDetailsViewAllData,name='productDetailsViewPage'),
    path('cart',views.cartUser,name='userCurrentCart'),
    path('delete-cart-product',views.deleteCartProduct,name='delete-cart-product'),
    path('update-cart',views.updateUserCart,name='update-cart'),
    path('checkout/',views.checkoutProduct,name='checkout'),
    path('place-order',views.placeorder,name='place-order'),
    path('my-orders',views.orderpage,name='my-orders'),
    path('my-appointment',views.my_appointment,name='my-appointment'),
    path('orderview/<str:t_no>/',views.orderdetailspage,name='orderview'),
    path('appointmentdetailspage/<str:t_no>/',views.appointmentdetailspage,name='appointmentdetailspage'),
    path('orderInvoice/<str:t_no>/',views.orderInvoicePdf.as_view(),name='orderInvoice'),
    path('cancelOrder',views.orderCancel,name='cancelOrder'),
    path('cancelappointment',views.cancelappointment,name="cancelappointment"),
    path("doctor_appointment",views.doc_appointment,name='doc_appointment'),
    path("canceldocappointment",views.canceldocappointment,name='canceldocappointment'),
    path("forgetPassword",views.forget,name='forget'),
    path("change-city",views.change_city,name='changecity'),
    path('submit_review/<int:item_id>',views.reviewsubmit,name='submit_review'),
    #report
    path("change_password",views.change_password,name='forget'),
    path('change-charges',views.changecharges,name='change-charges'),
    path('show_products_report/',views.pdf_report_create,name='show_products_report'),
    path('show_products/',views.show_product,name='show_products'),
    path('appointmentconfi',views.appointmentconfi,name='appointmentconfi'),

    path('pdf_report_create_category/',views.pdf_report_create_category,name='pdf_report_create_category'),
    path('show_product_category/',views.show_product_category,name='show_product_category'),

    path('pdf_report_create_subcategory/',views.pdf_report_create_subcategory,name='pdf_report_create_subcategory'),
    path('show_product_subcategory/',views.show_product_subcategory,name='show_product_subcategory'),

   
    path('pdf_report_create_order/',views.pdf_report_create_order,name='pdf_report_create_order'),
    path('show_order/',views.show_order,name='show_order'),

    path('pdf_report_create_cart/',views.pdf_report_create_cart,name='pdf_report_create_cart'),
    path('show_cart/',views.show_cart,name='show_cart'),

    path('show_appointmet',views.show_appointmet,name="show_appointmet"),
    path('pdf_appointmentReport_create',views.pdf_appointmentReport_create,name="pdf_appointmentReport_create"),

    path('show_doctors_appointmet',views.show_doctors_appointmet,name="show_doctors_appointmet"),
    path('pdf_doctors_appointment_report',views.pdf_doctors_appointment_report,name="pdf_doctors_appointment_report")

    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
