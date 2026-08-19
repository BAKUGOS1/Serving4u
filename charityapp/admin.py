from django.contrib import admin
from .models import login_table
from .models import detail_table
from .models import event_table
from .models import volunteer_applications
from .models import donate_money
from .models import donate_books
from .models import donate_clothes
from .models import donate_food
from .models import Contact
# Register your models here.

class LOGIN(admin.ModelAdmin):
    list_display = ["email","name","password","phone_no","role","status"]
admin.site.register(login_table,LOGIN)

class DETAIL(admin.ModelAdmin):
    list_display = ["login_id","display_pic","website","ngo_helpline","ngo_desc","address"]
admin.site.register(detail_table,DETAIL)

class EVENT(admin.ModelAdmin):
    list_display = ["event_name","event_photos","event_desc","ngo_id","volunteer","event_date","event_location"]
admin.site.register(event_table,EVENT)

class VOLUNTEER(admin.ModelAdmin):
    list_display = ["id","l_id","event_id","status","show_interest_button","rejected"]
admin.site.register(volunteer_applications,VOLUNTEER)

class DONATEM(admin.ModelAdmin):
    list_display = ["l_id","ngo_id","amount"]
admin.site.register(donate_money,DONATEM)

class DONATEB(admin.ModelAdmin):
    list_display = ["l_id","ngo_id","book_name","book_desc","book_quantity"]
admin.site.register(donate_books,DONATEB)

class DONATEC(admin.ModelAdmin):
    list_display = ["l_id","ngo_id","age_group","suitable_gender","pairs"]
admin.site.register(donate_clothes,DONATEC)

class DONATEF(admin.ModelAdmin):
    list_display = ["l_id","ngo_id","food_name","food_kg","making_datetime","expiry_datetime","donation_date","donation_photos"]
admin.site.register(donate_food,DONATEF)

class Contact_us(admin.ModelAdmin):
    list_display = ["message","name","email","subject"]
admin.site.register(Contact,Contact_us)




