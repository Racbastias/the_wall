from django.shortcuts import redirect

def login_required(func):
    
    def wrapper(request, *args, **kwargs):
        if 'user' not in request.session:
            return redirect('/register')
        resp = func(request, *args, **kwargs)
        return resp
    
    return wrapper