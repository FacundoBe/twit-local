from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Meep
from .forms import MeepForm, SignUpForm, AvatarForm
from django.contrib.auth import authenticate, login, logout 
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def home(request):
    if request.user.is_authenticated:
        form = MeepForm(request.POST or None)
        
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False) #commit=false para crear la instancia del Meep desde MeepForm pero
                                              # que no la guarde todavia por que falta definir el user
                meep.user=request.user         
                meep.save()                  #Ahora que ya esta definido el user si guardo           
                messages.success(request,(' Yor Message has been posted'))
                return redirect ('home')
            else: #if form is not valid 
                messages.success(request,(' There was an error in your submission'))

        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"meeps" : meeps,"form":form })
    else:
        meeps = Meep.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"meeps" : meeps})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request,(' You must be Logged to View this Page'))
        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:        
        profile = Profile.objects.get(user_id=pk) # profile que estoy viendo actualmente
        meeps=Meep.objects.filter(user_id=pk).order_by("-created_at")
        # POST form logic
        if request.method == "POST":
            # Get current user profile (que usuario esta loggeado)
            current_user_profile = request.user.profile
            # Get form data
            action = request.POST['follow']
            # decide to follow or unfollow
            if action =='unfollow':
                current_user_profile.follows.remove(profile)
            elif action =='follow':
                current_user_profile.follows.add(profile)
            current_user_profile.save()  # Las operaciones a bases de datos hay que confirmarlas
            return redirect(reverse('profile', args=[pk]))

        return  render(request, 'profile.html',{'profile':profile, "meeps":meeps}) # 
        
    else:
        messages.success(request,(' You must be Logged to View this Page'))
        return redirect('home')


def login_user(request):
    if request.user.is_authenticated:  # Si ya esta loggeado lo redirige a home en vez de mostrarle el login
        messages.success(request,(' You are Already Logged In '))
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username']
        password= request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,(f' You Have Been Logged In: {username}  Start Texting '))
            return redirect('home')
        else:
            messages.success(request,(' There Was an Error Loggin In please Try Again '))
            return redirect('login')

    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request,(' You Have Benn Logged Out. Come Back Soon!! '))
    return redirect('home')


def signup_view(request):
    if request.user.is_authenticated:
        messages.success(request,(' You Cant register while Logged In '))
        return redirect('home')

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Logg in the new user
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request,(' Registration Succesfull. Wellcome!!  '))
            return redirect('home')
        else:
            messages.success(request,(' There Was an Error please Try Again '))
    else:
        form= SignUpForm()

    return render(request,'signup.html',{'form':form} )


def search(request):
    if request.method == 'POST':
        searched = request.POST['search_input']
        meeps = Meep.objects.filter(body__contains=searched)
        return render(request,'search.html',{'searched':searched,'meeps':meeps} )
    else:
        return render(request,'search.html',{} )


def update_user(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id) #obtengo el objeto User para el usuario actual para modificarlo en la base de datos
        form=SignUpForm(request.POST or None, instance=current_user)
        if form.is_valid(): #Esto ya se activa al enviar la forma
            form.save() #Guardo los datos modificados
            login(request,current_user) # Lo reloggueo al usuario por que al actualizarlo en la base de datos django lo desloggea
            messages.success(request,(' Your Information Has Been Updated '))
            return redirect(reverse('profile', args=[current_user.id]))

        return render(request,'update_user.html',{'form':form} )

    else:
        messages.success(request,(' You must Be Logged In To View That Page '))
        return redirect('home')
        


def edit_image(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=request.user.id) # profile del usuario loggeado        
        
        formAvatar = AvatarForm()
       
        if request.method == "POST":
            if  "imagen_de_usuario" in request.POST: # si esto existe significa que se activo el boton de subir imagen de usuario
                formAvatar = AvatarForm(request.POST, request.FILES) #Ojo los archivos viajan separados en request.FILES
                if formAvatar.is_valid():
                    try: # Replace the image in avatar model if it already exists 
                        profile.avatar # There is no avatar object yet, then we create a new one
                        avatar=profile.avatar
                        avatar.uploaded_image= formAvatar.cleaned_data.get("uploaded_image")   
                        avatar.save()
                        messages.success(request,(' entro como formulario valido '))
                        return redirect(reverse('profile', args=[profile.user.id]))
                    except ObjectDoesNotExist: # Ther isnt an avatar object related to this profile so we create it
                        avatar=formAvatar.save(commit=False) #commit=false para crear la instancia del Meep desde MeepForm pero
                        avatar.profile=profile         # que no la guarde todavia por que recien ahora incrporo el profile
                        avatar.save()                  #Ahora que ya esta definido el user si guardo      
                        messages.success(request,(' Image Updated'))
                        return redirect(reverse('profile', args=[profile.user.id]))
                        
            # estoy en post pero no por el formulario si no por las imagenes preseteadas
            if 'image_number' in request.POST:            #en caso que se haya activado el formulario de alguna imagen predeterminada 
                image_number=request.POST['image_number'] #el diccionario de request.POST vuelve con un valor de image_number
                profile.preset_image = f"default{image_number}.jpg" 
                try:
                    profile.avatar.delete()  # Selecting a preset image deletes existing uploaded image
                except ObjectDoesNotExist:
                    pass # if it doesnt exist theres notihing o delete 
                profile.save()
                
                return redirect(reverse('profile', args=[profile.user.id]))
                

        return render(request, 'edit_image.html', {'formAvatar':formAvatar})
        
    else:
        messages.success(request,(' You are Not Logged In !!   '))
        return redirect('home') 
    
