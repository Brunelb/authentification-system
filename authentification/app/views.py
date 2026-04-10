# from django.http import HttpResponse
# from django.shortcuts import render,redirect
# from django.contrib.auth import authenticate,login,logout
# from django.contrib import messages
# from django.contrib.auth.models import User
# from authentification import settings
# from django.core.mail import send_mail

# # Create your views here.

# def home(request):
#     return render(request,'app/index.html')

# def register(request):
#     if request.method =="POST":
#         username = request.POST['username']
#         firstname = request.POST['firstname']
#         lastname = request.POST['lastname']
#         email = request.POST['email']
#         password = request.POST['password']
#         password1 = request.POST['password1']

#         if User.objects.filter(username=username):
#             messages.error(request,'ce nom a deja ete utilise')
#             return redirect('register')
        
#         if User.objects.filter(email=email):
#             messages.error(request,'cet email a deja ete utilise')
#             return redirect('register')
        
#         if not username.isalnum():
#             messages.error(request,' le nom doit etre alphanumerique')
#             return redirect('register')
        
#         if password != password1:
#             messages.error(request,'les deux passwords ne coincident pas')
#             return redirect('register')



#         mon_utilisateur = User.objects.create_user(username,email,password)
#         mon_utilisateur.first_name=firstname
#         mon_utilisateur.last_name=lastname
#         mon_utilisateur.save()
#         messages.success(request,'votre compte est bien cree')

#         subject = "bienvenue sur la formation d'authentification avec brunel"
#         message = "bienvenue"+ mon_utilisateur.first_name + " " + mon_utilisateur.last_name + "\n nous sommes heureux de vous compter parmi nous \n\n\n Merci \n brunel programmeur" 
#         from_email = settings.EMAIL_HOST_USER
#         to_list = [mon_utilisateur.email]
#         send_mail(subject, message, from_email, to_list, fail_silently=False)
#         return redirect('login')
#     return render(request,'app/register.html')
 
# def logIn(request):
 
#     if request.method =="POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username,password=password)
#         if user is not None:
#             login(request,user)
#             firstname = user.first_name
#             return render(request, 'app/index.html',{'firstname':firstname})
#         else:
#             messages.error(request,'mauvaise authentification')
#             return redirect('login')
#     return render(request, 'app/login.html')   

# def logOut(request):
#     logout(request)
#     messages.success(request,'vous avez ete bien deconnecte')
#     return redirect('home')

from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from .token import generatorToken


def home(request):
    return render(request, 'app/index.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'ce nom a deja ete utilise')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'cet email a deja ete utilise')
            return redirect('register')

        if not username.isalnum():
            messages.error(request, 'le nom doit etre alphanumerique')
            return redirect('register')

        if password != password1:
            messages.error(request, 'les deux passwords ne coincident pas')
            return redirect('register')

        mon_utilisateur = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        mon_utilisateur.first_name = firstname
        mon_utilisateur.last_name = lastname
        mon_utilisateur.is_active = False
        mon_utilisateur.save()

# envoie d'email de bienvenue

        subject = "Bienvenue sur la formation d'authentification avec Brunel"
        body = (
            f"Bienvenue {mon_utilisateur.first_name} {mon_utilisateur.last_name}\n\n"
            "Nous sommes heureux de vous compter parmi nous.\n\n"
            "Merci,\n Brunel programmeur"
        )

        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [mon_utilisateur.email],
                fail_silently=False
            )
            messages.success(request, 'Votre compte a bien été créé. Un email a été envoyé.')
        except Exception as e:
            messages.warning(request, f"Compte créé, mais l'email n'a pas pu être envoyé : {e}")
# envoie d'email de bienvenue de verification de mail 
        current_site = get_current_site(request)
        email_subject = "Confirmation de l'adresse email sur brunel "
        messageConfirm = render_to_string("emailconfirm.html", {
            "name": mon_utilisateur.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(mon_utilisateur.pk)),
            'token': generatorToken.make_token(mon_utilisateur)
        })
        
        email = EmailMessage(
            email_subject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [mon_utilisateur.email],

        )
        email.fail_silently=False
        email.send()
        return redirect('login')

    return render(request, 'app/register.html')





# def logIn(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         my_user = User.objects.get(username=username)
#         if user is not None:
#             login(request, user)
#             return render(request, 'app/index.html', {'firstname': user.first_name})
#         elif my_user.is_active == False:
#              messages.error(request, 'vous avez pas confirmer votre adresse vous devez le faire avant de vous connecter Merci !!')
#         else:
#             messages.error(request, 'mauvaise authentification')
#             return redirect('login')
#     return render(request, 'app/login.html')

def logIn(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        try:
            my_user = User.objects.get(username=username)
        except User.DoesNotExist:
            my_user = None

        if user is not None:
            login(request, user)
            return render(request, 'app/index.html', {'firstname': user.first_name})
        elif my_user is not None and not my_user.is_active:
            messages.error(request, 'Vous n’avez pas confirmé votre adresse email. Faites-le avant de vous connecter.')
            return redirect('login')
        else:
            messages.error(request, 'Mauvaise authentification')
            return redirect('login')

    return render(request, 'app/login.html')


def logOut(request):
    logout(request)
    messages.success(request, 'vous avez ete bien deconnecte')
    return redirect('home')



# def activate (request,uidb64,token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError,ValueError,OverflowError,User.DoesNotExist):
#         user = None

#     if user is not None and generatorToken.check_token(user,token):
#         user.is_active = True
#         user.save()
#         messages.success(request, 'Votre compte a bien été activer , connectez vous maintenant ')
#         return redirect('login')
#     else:
#         messages.error(request, 'votre compote pas active , ressayer!!!!')
#         return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Votre compte a bien été activé, connectez-vous maintenant.')
        return redirect('login')
    else:
        messages.error(request, 'Votre compte n’a pas été activé, réessayez.')
        return redirect('home')