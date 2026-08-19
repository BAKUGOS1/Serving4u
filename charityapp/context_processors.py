from .models import login_table, detail_table

def session_context(request):
    ngo = False
    profiledata = None
    user = None
    try:
        uid = request.session.get('log_id')
        if uid:
            user = login_table.objects.filter(id=uid).first()
            if user and user.role == "NGO":
                ngo = True
            profiledata = detail_table.objects.filter(login_id=uid).first()
    except Exception:
        pass
    return {
        'ngo': ngo,
        'profiledata': profiledata,
        'user': user,
        'current_user': user,
    }
