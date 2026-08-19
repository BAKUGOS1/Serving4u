from django import forms
from .models import (
    login_table,
    detail_table,
    event_table,
    donate_money,
    donate_books,
    donate_clothes,
    donate_food,
    Contact,
)

class UserSignupForm(forms.ModelForm):
    usertype = forms.ChoiceField(
        choices=[("User", "User"), ("NGO", "NGO")],
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'usertype'})
    )
    phone = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )

    class Meta:
        model = login_table
        fields = ['name', 'email', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Message', 'rows': 5}),
        }

class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = detail_table
        fields = ['display_pic', 'website', 'ngo_helpline', 'ngo_desc', 'address']
        widgets = {
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'}),
            'ngo_helpline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Helpline Number'}),
            'ngo_desc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Organization Description', 'rows': 4}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = event_table
        fields = ['event_name', 'event_pic', 'event_desc', 'volunteer', 'event_date', 'event_time', 'event_location']
        widgets = {
            'event_name': forms.TextInput(attrs={'class': 'form-control'}),
            'event_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'volunteer': forms.NumberInput(attrs={'class': 'form-control'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'event_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'event_location': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DonateMoneyForm(forms.ModelForm):
    class Meta:
        model = donate_money
        fields = ['amount']
        widgets = {
            'amount': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Amount in INR'}),
        }

class DonateBooksForm(forms.ModelForm):
    class Meta:
        model = donate_books
        fields = ['book_name', 'book_desc', 'book_quantity']
        widgets = {
            'book_name': forms.TextInput(attrs={'class': 'form-control'}),
            'book_desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'book_quantity': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DonateClothesForm(forms.ModelForm):
    class Meta:
        model = donate_clothes
        fields = ['age_group', 'suitable_gender', 'pairs']
        widgets = {
            'age_group': forms.TextInput(attrs={'class': 'form-control'}),
            'suitable_gender': forms.Select(attrs={'class': 'form-control'}),
            'pairs': forms.TextInput(attrs={'class': 'form-control'}),
        }

class DonateFoodForm(forms.ModelForm):
    class Meta:
        model = donate_food
        fields = ['food_name', 'food_kg', 'making_datetime', 'expiry_datetime', 'donation_date', 'samplefood_pic']
        widgets = {
            'food_name': forms.TextInput(attrs={'class': 'form-control'}),
            'food_kg': forms.TextInput(attrs={'class': 'form-control'}),
            'making_datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'expiry_datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'donation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
