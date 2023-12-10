from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
from .models import User, FlashcardSets, Flashcard, PremiumAccount, ProfilePhoto
from .forms import RegisterForm, LoginForm, CardSetForm, FlashcardForm, PremiumForm, UpdateProfileForm, ProfilePhotoForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core import serializers
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.template.defaultfilters import yesno
from django.db.models import Q
import os
from PIL import Image
from django.contrib.auth.forms import SetPasswordForm


def premium_upgrade(request,user_id):
    # print(user)
    host = request.get_host()
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '200',
        'item_name': 'Quiztion Premium Subscription',
        'invoice':uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('setPremium', args=[user_id])}",
        'console_url': f"http://{host}{reverse('dashboard')}",
    }
    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    context = {
        'form':paypal_payment
    }

    return render(request,'users/premiumupgrade.html',context)

def setPremium(request,user_id):
    user = User.objects.get(pk=user_id)
    print(user)
    PremiumAccount.objects.create(user=user, isPremium=True)
    logout(request)
    return redirect('dashboard')


def login_view(request):
    if(request.method == 'GET'):
        if request.user.is_authenticated:
            return redirect('dashboard')
        
        form = LoginForm()
        return render(request,'users/login.html', {'form': form})
    elif request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
        else:
            form = LoginForm(request.POST)
        
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(request,username=username,password=password)
                if user:
                    login(request, user)
                    user = User.objects.get(username=username)
                    premiumUser = None
                    try:
                        premiumUser = PremiumAccount.objects.get(user = user)
                    except PremiumAccount.DoesNotExist:
                        premiumUser = False
                    
                    if premiumUser is not False:
                        is_premium_js = yesno(premiumUser.isPremium, "true,false")
                    else:
                        is_premium_js = "false"

                    request.session['isPremium'] = is_premium_js
                    # messages.success(request,f'Hi {username.title()}, welcome back!')
                    request.session['username'] = username
                    request.session['id'] = user.id
                    return redirect('dashboard')
        
        
        messages.error(request,f'Invalid username or password')

        return render(request,'users/login.html',{'form':form})




@login_required
def createSet(request):
    if request.method == 'GET':
        context = {'form': CardSetForm()}
        return render(request, 'users/create_set.html', context)
    elif request.method == 'POST':
        form = CardSetForm(request.POST)
        message = None
        if form.is_valid():  # Validate the form before accessing cleaned_data
            set = FlashcardSets.objects.filter(author=request.user)
            for items in set:
                if(items.setTitle == form.cleaned_data['setTitle']):
                    message = "Duplicate Set Title Entry"
                    return render(request, 'users/create_set.html', {'form': form,'message':message})
            if message == None:
                card_set = form.save(commit=False)
                card_set.author = request.user
                card_set.save()
                return redirect('dashboard')
        
        
        
@login_required
def create_flashcard(request,title,id):
    if(request.method == 'GET'):
        context = {'form': FlashcardForm(),'title':title,'id':id}
        return render(request,'users/create_flashcard.html',context)
    elif request.method == 'POST':
        # myTitle = FlashcardSets.objects.get(setTitle=title)
        form = FlashcardForm(request.POST)
        if(form.is_valid()):
            card_set = form.save(commit=False)
            card_set.author = request.user
            card_set.setTitle_id = id
            if request.user == '' or title == '':
                return redirect('dashboard')
            form.save()
            return redirect(reverse('viewSet', args=(title,id,)))
        else:
            messages.error(request,'Please enter valid values')
            return render(request, 'users/create_flashcard.html', {'form':form,'title':title,'id':id})
        
@login_required
def delete_flashcard(request,title,set_id,flashcard_id):
    card = get_object_or_404(Flashcard,id=flashcard_id)
    if(request.method == 'GET'):
        card.delete()
        viewset_url = reverse('viewSet',args=(title,set_id))
        return redirect(viewset_url)
    
@login_required
def edit_flashcard(request,set_id,flashcard_id):
    card = get_object_or_404(Flashcard,id=flashcard_id)
    myTitle=FlashcardSets.objects.get(pk=set_id)
    if(request.method == "GET"):
        context = {'form':FlashcardForm(instance = card),'id':set_id}
        return render(request,'users/edit_flashcard.html',context)
    
    elif(request.method == "POST"):
        form = FlashcardForm(request.POST,instance = card)
        if form.is_valid():
            form.save()
            viewset_url = reverse('viewSet',args=(myTitle.setTitle,set_id,))
            return redirect(viewset_url)
        else:
            return render(request,'user/edit_flashcard.html',{'form':form,'username':set.author,'title':set.setTitle})



@login_required
def editSet(request,id):
    set = get_object_or_404(FlashcardSets,id=id)
    if request.method=="GET":
        context = {'form':CardSetForm(instance=set),'id':id}
        return render(request,'users/edit_set.html',context)

    elif request.method =='POST':
        form = CardSetForm(request.POST,instance = set)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        else:
            return render(request,'user/edit_set.html',{'form':form,'username':set.author,'title':set.setTitle})


@login_required
def viewSet(request,title,id):
    user = None
    flashcard_set = get_object_or_404(FlashcardSets, id=id)
    if(request.method == 'GET'):
        flashcards = Flashcard.objects.filter(setTitle__id=id)
        if request.user == flashcard_set.author:
            user = 'true'
        else:
            user = 'false'
        context = {'flashcards':flashcards,'title':title,'id':id,'user':user,'shareKey':flashcard_set.shareKey}
        return render(request,'users/view_flashcards.html',context)

@login_required
def deleteSet(request,id):
    post = get_object_or_404(FlashcardSets,id=id)
    if request.method == 'GET':
        post.delete()
        return redirect('dashboard')
    if request.method == 'POST':
        post.delete()
        return redirect('dashboard')


def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login') 

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', { 'form': form})  

    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            # login(request, user)
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form': form}) 
        


@login_required
def dashview(request):
    user = User.objects.get(username=request.session['username'])
    photo = ProfilePhoto.objects.filter(owner=request.user).first()
    
    # Filter sets created by the user or where the user has access
    sets = FlashcardSets.objects.filter(
        Q(author=user) | Q(access=user)
    ).distinct()

    quantity = {}
    premiumUser = None
    try:
        premiumUser = PremiumAccount.objects.get(user=user)
    except PremiumAccount.DoesNotExist:
        premiumUser = False

    for set in sets:
        flashcards_count = Flashcard.objects.filter(setTitle=set).count()
        quantity[set] = flashcards_count

    context = {'posts': sets, 'quantity': quantity, 'isPremium': request.session['isPremium'],'photo':photo}
    return render(request, 'users/dashboard.html', context)

def about_us(request):
    return render(request, "users/about.html")

@login_required
def practice_set(request,setID):
    #retrieves items from sqlite that matches the setTitle sent from template
    pracset = list(Flashcard.objects.filter(setTitle__id=setID))
    #if pracset is empty, sends an empty JSON string array
    if not pracset:
        flashcard_list = "[]"
    else:
    #if practset is not empty, serializes the retrieved pracset database objects into json objects then sent to template as flashcard list in context
        flashcard_list = serializers.serialize('json', pracset)
    return render(request,"users/practice.html",{
        "pracset":flashcard_list
    })

def import_set(request):
    if request.method == 'GET':
        return render(request,'users/importSet.html')
    
def import_setShareKey(request,shareKey):
    flashcard_set = get_object_or_404(FlashcardSets, shareKey=shareKey)
    if request.user.is_authenticated:
        if request.user != flashcard_set.author:
            flashcard_set.access.add(request.user)
    return redirect('dashboard')

def editProfile(request):
    if request.method == 'GET':
        photo_instance = ProfilePhoto.objects.filter(owner=request.user).first()
        user_form = UpdateProfileForm(instance=request.user)
        photo_form = ProfilePhotoForm()
        return render(request, 'users/edit_profile.html', {'form': user_form, 'photo_form': photo_form,'photo':photo_instance})
    elif request.method == 'POST':
        photo_instance = ProfilePhoto.objects.filter(owner=request.user).first()
        user_form = UpdateProfileForm(request.POST, instance=request.user)
        photo_form = ProfilePhotoForm(request.POST, request.FILES, instance=photo_instance)
        if 'image' in request.FILES:
            try:
                os.remove(photo_instance.image.path)
                print(photo_instance.image.path)
            except Exception as e:
                print(e)
        if user_form.is_valid() and photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.owner = request.user
            photo.save()
            user_form.save()
            return redirect('dashboard')
        else:
            print("Form errors:", user_form.errors, photo_form.errors)
            return redirect('dashboard')
    print("nope")
    return redirect('dashboard')


def changePassword(request):
    if request.method == 'GET':
        form = SetPasswordForm(request.user)
        print(form)
        return render(request,'users/changepassword.html',{'form':form})
    else:
        return redirect('editProfile')
