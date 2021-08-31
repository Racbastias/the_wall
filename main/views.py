from main.decorators import login_required
import bcrypt
from django.shortcuts import render, redirect
from main.models import Users, Publishers, Comments
from django.contrib import messages
from django.db import IntegrityError

def index(request):
    return redirect('/register')

def register(request):
    if request.method == 'GET':
        avatars = 'https://toppng.com/uploads/preview/roger-berry-avatar-placeholder-11562991561rbrfzlng6h.png'
        context={
        'avatars': avatars
        }
        return render(request, 'register.html', context)
    
    else:

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        gender = request.POST['gender']
        if gender == 1:
            avatar = 'https://www.terrainhopperusa.com/wp-content/uploads/2019/01/avatar-woman.png'
        else:
            avatar = 'https://cdn3.iconfinder.com/data/icons/avatars-round-flat/33/man5-512.png'
        
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        # validar que el formulario esté correcto
        errors = Users.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, mensaje_de_error in errors.items():
                messages.error(request, mensaje_de_error)
            return redirect('/register')
        
        # si llegamos hasta acá, estamos seguros que ambas coinciden
        user = Users.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = (bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()),
            avatar = avatar
        )
        request.session['user'] ={
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'avatar': avatar
            
        }
        messages.success(request, 'New user has been created')
        return redirect('/thewall')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    
    try:
        user = Users.objects.get(email=email)
    except Users.DoesNotExist:
        messages.error(request, 'User or password does not exist')
        return redirect('/register')
    
    if  not bcrypt.checkpw(password.encode(), user.password.encode()): 
        messages.error(request, 'User or password does not exist')
        return redirect('/register')
    
    request.session['user'] = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'avatar': user.avatar
    }
    
    messages.success(request, f'Bienvenido {user.first_name} {user.last_name}')
    return redirect('/thewall')

@login_required
def logout(request):
    avatars = 'https://toppng.com/uploads/preview/roger-berry-avatar-placeholder-11562991561rbrfzlng6h.png'
    del request.session['user']
    context={
        'avatars': avatars
    }
    return redirect('/register', context)

@login_required
def thewall(request):
    
    users = Users.objects.all()
    publishers = Publishers.objects.all().order_by('-updated_at')
    comments = Comments.objects.all()
    
    user = request.session['user']
    
    context = {
        "user": user,
        "publishers": publishers,
        "users": users,
        "comments": comments
    }
    return render(request, 'thewall.html', context)

@login_required
def publish(request): # Ok
    user = request.session['user']
    publish = request.POST['publish']
    context = {
        "publish": publish,
        "user": user
    }
    userid= request.session['user']['id']
    #import pdb; pdb.set_trace()
    usertemp = Users.objects.get(id=userid)
    usertemp.publishers.create(publish = publish)
    messages.success(request, f'Your message has ben published')
    return redirect('/thewall')
    

#@login_required
#def id(request, id):
    selectedshow = Shows.objects.get(id=id)
    channel = Tv.objects.all()
    show = Shows.objects.all()
    user = request.session['user']
    context = {
        "channel": channel,
        "show": show,
        "user": user,
        "selectedshow": selectedshow
    }
    return render(request, 'tv_show.html', context)

#@login_required
#def edit(request, id):
    selectedshow = Shows.objects.get(id=id)
    channel = Tv.objects.all()
    release_date = selectedshow.release_date.strftime('%Y-%m-%d')
    user = request.session['user']
    context = {
        "selectedshow": selectedshow,
        "channel": channel,
        "user": user,
        "release_date": release_date
    }
    return render(request, 'edit.html', context)

#@login_required
#def update(request, id):
    selectedshow = Shows.objects.get(id=id)
    errors = Shows.objects.basic_validator(request.POST)
    channel = Tv.objects.all()
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'../{selectedshow.id}/edit')
    else:
        showtitle = request.POST['title']
        idnetwork = int(request.POST['network'])
        date = request.POST['date'].strftime('%Y-%m-%d')
        desc = request.POST['desc']
        
        selectedshow.title = showtitle
        selectedshow.network_id = idnetwork
        selectedshow.release_date = date
        selectedshow.desc = desc
        selectedshow.save()
        messages.info(request, f'Your show {showtitle} has been updated')
        return redirect(f'../{selectedshow.id}')

#@login_required
#def destroy(request, id):
    selectedshow = Shows.objects.get(id=id)
    temp = selectedshow.title
    context = {
        "temp": temp
    }
    messages.error(request, f'Your show {temp} has been deleted')
    
    selectedshow.delete()
    return redirect("/shows", context)