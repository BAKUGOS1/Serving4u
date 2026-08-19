from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum
from django.conf import settings

from .models import (
    login_table,
    detail_table,
    event_table,
    volunteer_applications,
    donate_clothes,
    donate_books,
    donate_food,
    donate_money,
    Contact,
)
from .forms import (
    UserSignupForm,
    UserLoginForm,
    ContactForm,
    CompleteProfileForm,
    EventForm,
    DonateMoneyForm,
    DonateBooksForm,
    DonateClothesForm,
    DonateFoodForm,
    ChangePasswordForm,
)
from .services import AuthService, PaymentService, ContextService

def index(request):
    session_ctx = ContextService.get_user_session_context(request)
    allevents = event_table.objects.all().order_by('-id')
    context = {
        'ngo': session_ctx['ngo'],
        'profiledata': session_ctx['profiledata'],
        'user': session_ctx['user'],
        'allevents': allevents,
    }
    return render(request, 'index.html', context)

def basic(request):
    return render(request, 'basic.html')

def about(request):
    session_ctx = ContextService.get_user_session_context(request)
    context = {
        'ngo': session_ctx['ngo'],
        'profiledata': session_ctx['profiledata'],
        'user': session_ctx['user'],
    }
    return render(request, 'about.html', context)

def contact(request):
    session_ctx = ContextService.get_user_session_context(request)
    context = {
        'ngo': session_ctx['ngo'],
        'profiledata': session_ctx['profiledata'],
        'user': session_ctx['user'],
    }
    return render(request, 'contact.html', context)

def submitcontact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Response Recorded')
            return redirect(index)
        else:
            # Fallback to direct field reading if form validation fails partially
            message = request.POST.get("message")
            name = request.POST.get("name")
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            Contact.objects.create(message=message, name=name, email=email, subject=subject)
            messages.success(request, 'Response Recorded')
            return redirect(index)
    else:
        messages.error(request, 'error occured')
        return redirect(index)

def login(request):
    return render(request, 'login.html')

def signup(request):
    return render(request, 'signup.html')

def viewdata(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        role = request.POST.get("usertype")

        AuthService.register_user(
            name=name,
            email=email,
            password=password,
            phone=phone,
            role=role
        )

        if role == "NGO":
            messages.info(request, 'Registration Done Successfully. Please wait for your profile Approval. It will take around 2-3 days.')
        else:
            messages.success(request, 'Data Inserted Successfully. you can login now')
        return redirect(index)
    else:
        messages.error(request, 'error occured')
        return redirect(index)

def checklogin(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = AuthService.authenticate_user(username, password)

        if user is not None:
            if user.role == "NGO" and user.status == "0":
                messages.error(request, 'Your Profile is Under Approval Process. This may take upto 3 working days.')
            else:
                request.session['log_user'] = user.email
                request.session['log_id'] = user.id
                request.session.save()
                messages.success(request, 'Successfully Logged In')
                return redirect(index)
        else:
            messages.error(request, 'Invalid USER ID')
    return redirect(login)

def logout(request):
    try:
        del request.session['log_user']
        del request.session['log_id']
    except KeyError:
        pass
    return redirect(index)

def completeprofile(request):
    session_ctx = ContextService.get_user_session_context(request)
    context = {
        'ngo': session_ctx['ngo'],
        'profiledata': session_ctx['profiledata'],
    }
    return render(request, 'completeprofile.html', context)

def completeprofilesubmit(request):
    uid = request.session.get('log_id')
    if request.method == 'POST' and uid:
        nwebsite = request.POST.get("website")
        ngophone = request.POST.get("ngophone")
        file = request.FILES.get('dp')
        naddress = request.POST.get("address")
        ndescription = request.POST.get("description")

        user_obj = login_table.objects.get(id=uid)
        userdata = detail_table(
            login_id=user_obj,
            website=nwebsite,
            display_pic=file,
            ngo_helpline=ngophone,
            ngo_desc=ndescription,
            address=naddress
        )
        userdata.save()
        messages.success(request, 'Data Inserted Successfully.')
        return redirect(index)
    else:
        messages.error(request, 'error occured')
        return redirect(index)

def ngoprofile(request):
    session_ctx = ContextService.get_user_session_context(request)
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
    }
    return render(request, 'ngoprofile.html', context)

def editprofilengo(request):
    session_ctx = ContextService.get_user_session_context(request)
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
    }
    return render(request, 'editprofilengo.html', context)

def datasave(request):
    uid = request.session.get('log_id')
    if request.method == 'POST' and uid:
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        website = request.POST.get("website")
        ngophone = request.POST.get("ngophone")
        address = request.POST.get("address")
        description = request.POST.get("description")

        cuser = detail_table.objects.filter(login_id=uid).first()
        if cuser:
            cuser.website = website
            cuser.ngo_helpline = ngophone
            cuser.ngo_desc = description
            cuser.address = address
            cuser.save(update_fields=['website', 'ngo_helpline', 'ngo_desc', 'address'])

        cuser1 = login_table.objects.filter(id=uid).first()
        if cuser1:
            cuser1.name = name
            cuser1.phone_no = phone
            cuser1.save(update_fields=['name', 'phone_no'])

        messages.success(request, 'Data Updated Successfully. ')
        return redirect(editprofilengo)
    else:
        messages.error(request, 'error occured')
        return redirect(editprofilengo)

def changepw(request):
    uid = request.session.get('log_id')
    if request.method == 'POST' and uid:
        cpw = request.POST.get("oldpassword")
        npw = request.POST.get("password")

        cusercheck = login_table.objects.filter(id=uid).first()
        if cusercheck and cusercheck.check_password(cpw):
            cusercheck.set_password(npw)
            cusercheck.save(update_fields=['password'])
            messages.success(request, 'Password Changed Successfully. ')
        else:
            messages.error(request, 'Current Password is wrong.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def changedp(request):
    uid = request.session.get('log_id')
    if request.method == 'POST' and uid and 'changedp' in request.FILES:
        file = request.FILES['changedp']
        cuser1 = detail_table.objects.filter(login_id=uid).first()
        if cuser1:
            cuser1.display_pic = file
            cuser1.save(update_fields=['display_pic'])
            messages.success(request, 'Picture Changed Successfully. ')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def profile(request):
    session_ctx = ContextService.get_user_session_context(request)
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
    }
    return render(request, 'profile.html', context)

def editprofile(request):
    session_ctx = ContextService.get_user_session_context(request)
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
    }
    return render(request, 'editprofile.html', context)

def datasaveuser(request):
    uid = request.session.get('log_id')
    if request.method == 'POST' and uid:
        name = request.POST.get("name")
        phone = request.POST.get("phone")

        cuser1 = login_table.objects.filter(id=uid).first()
        if cuser1:
            cuser1.name = name
            cuser1.phone_no = phone
            cuser1.save(update_fields=['name', 'phone_no'])

        messages.success(request, 'Data Updated Successfully. ')
        return redirect(editprofile)
    else:
        messages.error(request, 'error occured')
        return redirect(editprofile)

def addevent(request):
    session_ctx = ContextService.get_user_session_context(request)
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
    }
    return render(request, 'addevent.html', context)

def addeventsubmit(request):
    uid = request.session.get('log_id')
    if request.method == 'POST' and uid:
        name = request.POST.get("name")
        date = request.POST.get("date")
        time = request.POST.get("time")
        file = request.FILES.get('dp')
        location = request.POST.get("location")
        volunteer = request.POST.get("volunteer")
        description = request.POST.get("description")

        user_obj = login_table.objects.get(id=uid)
        eventdata = event_table(
            event_name=name,
            event_desc=description,
            event_pic=file,
            ngo_id=user_obj,
            volunteer=volunteer,
            event_location=location,
            event_date=date,
            event_time=time
        )
        eventdata.save()
        messages.success(request, 'Data Inserted Successfully.')
        return redirect(addevent)
    else:
        messages.error(request, 'error occured')
        return redirect(addevent)

def manageevent(request):
    session_ctx = ContextService.get_user_session_context(request)
    uid = request.session.get('log_id')
    myevents = event_table.objects.filter(ngo_id=uid) if uid else []
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'myevents': myevents,
    }
    return render(request, 'myevents.html', context)

def deleteevent(request, deid):
    event_table.objects.filter(id=deid).delete()
    messages.error(request, 'Event Deleted')
    return redirect(manageevent)

def reqcan(request):
    session_ctx = ContextService.get_user_session_context(request)
    uid = request.session.get('log_id')
    myevents = event_table.objects.filter(ngo_id=uid) if uid else []
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'myevents': myevents,
    }
    return render(request, 'reqcan.html', context)

def reqcansubmit(request):
    if request.method == 'POST':
        canno = request.POST.get("canno")
        eventid = request.POST.get("eventname")

        selevent = event_table.objects.filter(id=eventid).first()
        if selevent:
            selevent.volunteer = canno
            selevent.save(update_fields=['volunteer'])
            messages.success(request, 'Data Inserted Successfully. ')
            return redirect(reqcan)
    messages.error(request, 'error occured')
    return redirect(reqcan)

def allngo(request):
    session_ctx = ContextService.get_user_session_context(request)
    filterngouser = login_table.objects.filter(role="NGO", status="1").values_list('id', flat=True)
    allngodata = detail_table.objects.filter(login_id__in=filterngouser)
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'allngodata': allngodata,
    }
    return render(request, 'program.html', context)

def viewevents(request, veid):
    session_ctx = ContextService.get_user_session_context(request)
    myevents = event_table.objects.filter(ngo_id=veid)
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'myevents': myevents,
    }
    return render(request, 'viewevents.html', context)

def viewngo(request, vnid):
    session_ctx = ContextService.get_user_session_context(request)
    ngodetail = detail_table.objects.filter(id=vnid).first()
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'ngodetail': ngodetail,
    }
    return render(request, 'viewngo.html', context)

def events(request):
    session_ctx = ContextService.get_user_session_context(request)
    allevents = event_table.objects.all()
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'allevents': allevents,
    }
    return render(request, 'events.html', context)

def eventsingle(request, esid):
    session_ctx = ContextService.get_user_session_context(request)
    eventdetail = event_table.objects.filter(id=esid).first()
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'eventdetail': eventdetail,
    }
    return render(request, 'eventsingle.html', context)

def ngodet(request, ndid):
    session_ctx = ContextService.get_user_session_context(request)
    ngodetail = detail_table.objects.filter(login_id=ndid).first()
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'ngodetail': ngodetail,
    }
    return render(request, 'viewngo.html', context)

def beavol(request, bavid):
    uid = request.session.get('log_id')
    if uid:
        volaps = volunteer_applications.objects.filter(l_id=uid, event_id=bavid).first()
        if volaps is None:
            user_obj = login_table.objects.get(id=uid)
            event_obj = event_table.objects.get(id=bavid)
            voldata = volunteer_applications(l_id=user_obj, event_id=event_obj, status="0")
            voldata.save()
            messages.success(request, 'Applied for Volunteer. Please wait for approval.')
        else:
            messages.error(request, 'You Have already applied for this.')
    else:
        messages.error(request, 'Please Login.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def applyvolunteer(request):
    session_ctx = ContextService.get_user_session_context(request)
    eventsdata = event_table.objects.all()
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'eventsdata': eventsdata,
    }
    return render(request, 'applyvolunteer.html', context)

def applyforvol(request):
    uid = request.session.get('log_id')
    if request.method == 'POST' and uid:
        eventid = request.POST.get("eventid")
        volaps = volunteer_applications.objects.filter(l_id=uid, event_id=eventid).first()
        if volaps is None:
            user_obj = login_table.objects.get(id=uid)
            event_obj = event_table.objects.get(id=eventid)
            voldata = volunteer_applications(l_id=user_obj, event_id=event_obj, status="0")
            voldata.save()
            messages.success(request, 'Applied for Volunteer. Please wait for approval.')
        else:
            messages.error(request, 'You Have already applied for this.')
    else:
        messages.error(request, 'Please Login.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def viewcan(request):
    session_ctx = ContextService.get_user_session_context(request)
    uid = request.session.get('log_id')
    appliedcandata = None
    if uid:
        mylogindata = event_table.objects.filter(ngo_id=uid).values_list('id', flat=True)
        appliedcandata = volunteer_applications.objects.filter(event_id__in=mylogindata)
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'appliedcandata': appliedcandata,
    }
    return render(request, 'viewcan.html', context)

def acceptcan(request, acid):
    upvolstat = volunteer_applications.objects.filter(id=acid).first()
    if upvolstat:
        volcount = upvolstat.event_id.volunteer
        selevent = upvolstat.event_id
        if volcount > 0:
            upvolstat.status = "1"
            upvolstat.show_interest_button = False
            upvolstat.save(update_fields=['status', 'show_interest_button'])
            volcount -= 1
            selevent.volunteer = volcount
            selevent.save(update_fields=['volunteer'])
            messages.success(request, 'Candidate Approved. ')
        else:
            messages.error(request, 'Required number of volunteers are selected already. ')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def rejectcan(request, rcid):
    upvolstat = volunteer_applications.objects.filter(id=rcid).first()
    if upvolstat:
        upvolstat.status = "2"
        upvolstat.rejected = True
        upvolstat.save(update_fields=['status', 'rejected'])
        messages.error(request, 'Candidate Rejected. ')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def viewmyapplications(request):
    session_ctx = ContextService.get_user_session_context(request)
    uid = request.session.get('log_id')
    myappdata = volunteer_applications.objects.filter(l_id=uid) if uid else []
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'myappdata': myappdata,
    }
    return render(request, 'viewmyapplications.html', context)

def donateclothes(request):
    session_ctx = ContextService.get_user_session_context(request)
    fetchngo = detail_table.objects.all()
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'fetchngo': fetchngo,
    }
    return render(request, 'donateclothes.html', context)

def donateclothessubmit(request):
    uid = request.session.get('log_id')
    if request.method == 'POST' and uid:
        agegroup = request.POST.get("agegroup")
        pairs = request.POST.get("pairs")
        gender = request.POST.get("gender")
        ngoid = request.POST.get("ngoid")

        user_obj = login_table.objects.get(id=uid)
        ngo_obj = detail_table.objects.get(id=ngoid)
        donatedata = donate_clothes(
            l_id=user_obj,
            ngo_id=ngo_obj,
            age_group=agegroup,
            suitable_gender=gender,
            pairs=pairs
        )
        donatedata.save()
        messages.success(request, 'Donation Done Successfully.')
        return redirect(donateclothes)
    messages.error(request, 'error occured')
    return redirect(donateclothes)

def donatebooks(request):
    session_ctx = ContextService.get_user_session_context(request)
    fetchngo = detail_table.objects.all()
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'fetchngo': fetchngo,
    }
    return render(request, 'donatebooks.html', context)

def donatebooksubmit(request):
    uid = request.session.get('log_id')
    if request.method == 'POST' and uid:
        bookname = request.POST.get("bookname")
        quan = request.POST.get("quan")
        bookdesc = request.POST.get("bookdesc")
        ngoid = request.POST.get("ngoid")

        user_obj = login_table.objects.get(id=uid)
        ngo_obj = detail_table.objects.get(id=ngoid)
        donatedata = donate_books(
            l_id=user_obj,
            ngo_id=ngo_obj,
            book_name=bookname,
            book_desc=bookdesc,
            book_quantity=quan
        )
        donatedata.save()
        messages.success(request, 'Donation Done Successfully.')
        return redirect(donatebooks)
    messages.error(request, 'error occured')
    return redirect(donatebooks)

def donatefood(request):
    session_ctx = ContextService.get_user_session_context(request)
    fetchngo = detail_table.objects.all()
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'fetchngo': fetchngo,
    }
    return render(request, 'donatefood.html', context)

def donatefoodsubmit(request):
    uid = request.session.get('log_id')
    if request.method == 'POST' and uid:
        foodname = request.POST.get("foodname")
        foodweight = request.POST.get("foodweight")
        makingdatetime = request.POST.get("makingdatetime")
        expdatetime = request.POST.get("expdatetime")
        donationdate = request.POST.get("donationdate")
        ngoid = request.POST.get("ngoid")
        file = request.FILES.get('foodsample')

        user_obj = login_table.objects.get(id=uid)
        ngo_obj = detail_table.objects.get(id=ngoid)
        donatedata = donate_food(
            l_id=user_obj,
            ngo_id=ngo_obj,
            food_name=foodname,
            food_kg=foodweight,
            making_datetime=makingdatetime,
            expiry_datetime=expdatetime,
            donation_date=donationdate,
            samplefood_pic=file
        )
        donatedata.save()
        messages.success(request, 'Donation Done Successfully.')
        return redirect(donatefood)
    messages.error(request, 'error occured')
    return redirect(donatefood)

def donatemoney(request):
    session_ctx = ContextService.get_user_session_context(request)
    fetchngo = detail_table.objects.all()
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'fetchngo': fetchngo,
    }
    return render(request, 'donatemoney.html', context)

def donatemoneysubmit(request):
    uid = request.session.get('log_id')
    if request.method == 'POST' and uid:
        paytype = request.POST.get("paymentMethod")
        damount = request.POST.get("amount")
        ngoid = request.POST.get("ngoid")
        user_obj = login_table.objects.get(id=uid)
        ngo_obj = detail_table.objects.get(id=ngoid)

        if paytype == "card":
            cnumber = request.POST.get("number")
            cvv = request.POST.get("security-code")
            exp = request.POST.get("expiration-month-and-year")

            if cnumber == '4242424242424242' and cvv == '123' and exp == '01/25':
                donatedata = donate_money(l_id=user_obj, ngo_id=ngo_obj, amount=damount)
                donatedata.save()
                messages.success(request, 'Donation Done Successfully.')
                return redirect(donatemoney)
            else:
                messages.error(request, 'Payment Failed.')
                return redirect(donatemoney)
        elif paytype == "online":
            razorpay_order = PaymentService.create_razorpay_order(damount)
            donatedata = donate_money(l_id=user_obj, ngo_id=ngo_obj, amount=damount)
            donatedata.save()
            order_id = razorpay_order['id'] if razorpay_order else f"order_rcptid_{uid}"
            total_paise = int(float(damount) * 100)
            return render(request, "payment.html", {
                "razorpay_order_id": order_id,
                "amount": total_paise,
                "key": getattr(settings, 'RAZORPAY_KEY_ID', ''),
                "currency": "INR",
            })
    messages.error(request, 'error occured')
    return redirect(donatemoney)

def receivedmoney(request):
    session_ctx = ContextService.get_user_session_context(request)
    uid = request.session.get('log_id')
    ngomoney = None
    totaldonation = None
    if uid:
        myngo = detail_table.objects.filter(login_id=uid).first()
        if myngo:
            ngomoney = donate_money.objects.filter(ngo_id=myngo)
            totaldonation = donate_money.objects.filter(ngo_id=myngo).aggregate(Sum('amount'))
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'ngomoney': ngomoney,
        'totaldonation': totaldonation,
    }
    return render(request, 'receivedmoney.html', context)

def receivedfood(request):
    session_ctx = ContextService.get_user_session_context(request)
    uid = request.session.get('log_id')
    ngofood = None
    if uid:
        myngo = detail_table.objects.filter(login_id=uid).first()
        if myngo:
            ngofood = donate_food.objects.filter(ngo_id=myngo)
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'ngofood': ngofood,
    }
    return render(request, 'receivedfood.html', context)

def receivedclothes(request):
    session_ctx = ContextService.get_user_session_context(request)
    uid = request.session.get('log_id')
    ngoclothes = None
    if uid:
        myngo = detail_table.objects.filter(login_id=uid).first()
        if myngo:
            ngoclothes = donate_clothes.objects.filter(ngo_id=myngo)
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'ngoclothes': ngoclothes,
    }
    return render(request, 'receivedclothes.html', context)

def receivedbooks(request):
    session_ctx = ContextService.get_user_session_context(request)
    uid = request.session.get('log_id')
    ngobooks = None
    if uid:
        myngo = detail_table.objects.filter(login_id=uid).first()
        if myngo:
            ngobooks = donate_books.objects.filter(ngo_id=myngo)
    context = {
        'ngo': session_ctx['ngo'],
        'user': session_ctx['user'],
        'profiledata': session_ctx['profiledata'],
        'ngobooks': ngobooks,
    }
    return render(request, 'receivedbooks.html', context)