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
        avatar = request.POST['gender']
        
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        # validar que el formulario esté correcto
        errors = Users.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, mensaje_de_error in errors.items():
                messages.error(request, mensaje_de_error)
            return redirect('/register')
        
        # si llegamos hasta acá, estamos seguros que ambas coinciden
        #import pdb; pdb.set_trace()
        try: 
            user = Users.objects.create(
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = (bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()),
                avatar = avatar
            )
        except IntegrityError:
            messages.error(request, 'This Email already exist')
            return redirect('/register')
        
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
    user = request.session['user']
    
    context = {
        "user": user,
        "publishers": publishers,
        "users": users,
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

@login_required
def comment(request):
    comment = request.POST['comment']
    publishid = int(request.POST['publishid'])
    userid= int(request.session['user']['id'])
    
    Comments.objects.create(
        comment = comment,
        author_id = userid,
        publish_id = publishid
        )
    messages.success(request, f'Your comment has ben published')
    return redirect('/thewall')

#@login_required
#def follow(request, id):
    publishid = int(request.POST['publishid'])
    userid= int(request.session['user']['id'])
    
    Comments.objects.create(
        comment = comment,
        author_id = userid,
        publish_id = publishid
        )
    messages.success(request, f'Your comment has ben published')
    return redirect('/thewall')

#@login_required
#def unfollow(request, id):
    publishid = int(request.POST['publishid'])
    userid= int(request.session['user']['id'])
    
    Comments.objects.create(
        comment = comment,
        author_id = userid,
        publish_id = publishid
        )
    messages.success(request, f'Your comment has ben published')
    return redirect('/thewall')


@login_required
def editpublish(request, id):
    selectedpublish = Publishers.objects.get(id=id)
    userid = request.session['user']['id']
    newpublish = request.POST['publish']

    if selectedpublish.author.id == userid:
        selectedpublish.publish = newpublish
        selectedpublish.save()
        messages.info(request, f'Your publish has been updated')
        return redirect(f'/thewall')
    
    else:
        messages.error(request, f'Your are not allowed to edit this')
        return redirect("/thewall")

@login_required
def editcomment(request, id):
    selectedcomment = Comments.objects.get(id=id)
    userid = request.session['user']['id']
    newcomment = request.POST['comment']
    
    if selectedcomment.author.id == userid:
        selectedcomment.comment = newcomment
        selectedcomment.save()
        messages.info(request, f'Your comment has been updated')
        return redirect(f'/thewall')
    
    else:
        messages.error(request, f'Your are not allowed to edit this')
        return redirect("/thewall")

@login_required
def deletepublish(request, id):
    userid= request.session['user']['id']
    selectedpublish = Publishers.objects.get(id=id)
    
    if selectedpublish.author.id == userid:
        selectedpublish.delete()
        messages.error(request, f'Your publish has been deleted')
        return redirect("/thewall")
    
    else:
        messages.error(request, f'Your are not allowed to delete this')
        return redirect("/thewall")

@login_required
def deletecomment(request, id):
    userid= request.session['user']['id']
    selectedcomment = Comments.objects.get(id=id)
    
    if selectedcomment.author.id == userid:
        selectedcomment.delete()
        messages.error(request, f'Your comment has been deleted')
        return redirect("/thewall")
    
    else:
        messages.error(request, f'Your are not allowed to delete this')
        return redirect("/thewall")