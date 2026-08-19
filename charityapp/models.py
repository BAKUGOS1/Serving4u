import time

from django.db import models
from django.core.validators import FileExtensionValidator
from collections import namedtuple

from django.utils.safestring import mark_safe
# Create your models here.
class login_table(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_no = models.IntegerField()
    ROLE = (
        ("NGO", "NGO"),
        ("User", "User")
    )
    role = models.CharField(max_length=10, choices=ROLE)
    STATUS = (
        ("0", "unapproved"),
        ("1", "approved")
    )
    status = models.CharField(max_length=10, choices=STATUS)

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        from django.contrib.auth.hashers import check_password
        if self.password == raw_password:
            return True
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name

class detail_table(models.Model):
    login_id = models.ForeignKey(login_table, on_delete=models.CASCADE)
    display_pic = models.ImageField(upload_to="photos")
    website=models.CharField(max_length=50)
    ngo_helpline=models.CharField(max_length=50)
    ngo_desc=models.CharField(max_length=100)
    address=models.CharField(max_length=50)

    def admin_photos(self):
       return mark_safe('<img src="{}" width="100"/>'.format(self.display_pic.url))

    admin_photos.allow_tags = True


class event_table(models.Model):
    event_name = models.CharField(max_length=100)
    event_pic = models.ImageField(upload_to="photos")
    event_desc= models.CharField(max_length=1000)
    ngo_id = models.ForeignKey(login_table,on_delete=models.CASCADE)
    volunteer = models.IntegerField(default=0)
    event_date = models.DateField(default="2022-06-06")
    event_time = models.TimeField(null=True, blank=True)
    event_location = models.CharField(max_length=25)

    def event_photos(self):
       return mark_safe('<img src="{}" width="100"/>'.format(self.event_pic.url))

    event_photos.allow_tags = True

    def __str__(self):
        return self.event_name

class volunteer_applications(models.Model):
    l_id = models.ForeignKey(login_table,on_delete=models.CASCADE)
    event_id = models.ForeignKey(event_table,on_delete=models.CASCADE)
    STATUS = (
        ("0", "unapproved"),
        ("1", "approved"),
        ("2", "rejected")
    )
    status = models.CharField(max_length=10, choices=STATUS)
    show_interest_button = models.BooleanField(default=True)
    rejected = models.BooleanField(default=False)

class donate_money(models.Model):
    l_id = models.ForeignKey(login_table,on_delete=models.CASCADE)
    ngo_id = models.ForeignKey(detail_table,on_delete=models.CASCADE)
    amount= models.CharField(max_length=100)

class donate_books(models.Model):
    l_id = models.ForeignKey(login_table,on_delete=models.CASCADE)
    ngo_id = models.ForeignKey(detail_table,on_delete=models.CASCADE)
    book_name = models.CharField(max_length=100)
    book_desc = models.CharField(max_length=100)
    book_quantity= models.CharField(max_length=100)

class donate_clothes(models.Model):
    l_id = models.ForeignKey(login_table,on_delete=models.CASCADE)
    ngo_id = models.ForeignKey(detail_table,on_delete=models.CASCADE)
    age_group = models.CharField(max_length=100)
    gender = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Both", "Both"),
    )
    suitable_gender = models.CharField(max_length=10, choices=gender)
    pairs = models.CharField(max_length=100)

class donate_food(models.Model):
    l_id = models.ForeignKey(login_table,on_delete=models.CASCADE)
    ngo_id = models.ForeignKey(detail_table,on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    food_kg = models.CharField(max_length=100)
    making_datetime = models.DateTimeField()
    expiry_datetime = models.DateTimeField()
    donation_date = models.DateField()
    samplefood_pic = models.ImageField(upload_to="photos")

    def donation_photos(self):
       return mark_safe('<img src="{}" width="100"/>'.format(self.samplefood_pic.url))

    donation_photos.allow_tags = True


class Contact(models.Model):
    message = models.CharField(max_length=500)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)


