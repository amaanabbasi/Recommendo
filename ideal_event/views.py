from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from ideal_event.forms import UserForm, AppUserForm, KeyValForm
from ideal_event.models import AppUser, Interest, KeyVal, Grp
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from . import recommender
import math
from django.contrib.auth.models import User

@login_required
def index(request):
    ol = Grp.objects.all()
    print(request.user.id)
    logged_user = AppUser.objects.get(user_id=request.user.id)
    interests_logged_user = logged_user.interests.all()
    context = {
        "ol": ol,
        "it": interests_logged_user,
        "username": logged_user
    }
    return render(request, 'ideal_event/index.html', context)


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


# @login_required
# def process(request):  # data algo
#     persons = list(data.keys())
#     for person in persons:
# 	    print(f"er")
    # return render(request, 'ideal_event/process.html')
    # return redirect(request, "ideal_event/process.html")


@login_required
def select_interests(request):
    # select_interest_form = Interest2Form(request.POST or None)
    interest_count = Interest.objects.all().count()
    # for i in range(interest_count):
    form = KeyValForm(request.POST or None)
    interest = Interest.objects.all()
    instance = None
    if request.method == "POST":
        if form.is_valid():
            interest2 = form.save(commit=False)
            interest2.save()
            form.save_m2m()
            return redirect("ideal")

    context = {
        "form": form,
        "instance": instance,
        "interest": interest,
        "interest_count": interest_count
    }

    return render(request, 'ideal_event/select_interest.html', context=context)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        AppUser_form = AppUserForm(data=request.POST)
        if user_form.is_valid() and AppUser_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)   # Is this neccesary ??
            user.save()
            appUser = AppUser_form.save(commit=False)
            appUser.user_id = user

            if 'profile_pic' in request.FILES:
                print('found it')
                appUser.profile_pic = request.FILES['profile_pic']
                appUser.save()
                registered = True
            
            appUser.save()
            registered = True
        else:
            print(user_form.errors, AppUser_form.errors)
    else:
        user_form = UserForm()
        AppUser_form = AppUserForm()
    return render(request, 'ideal_event/registration.html',
                  {'user_form': user_form,
                           'AppUser_form': AppUser_form,
                           'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(
                username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'ideal_event/login.html', {})

@receiver(post_save, sender=User)
def add_to_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance) 

@receiver(post_save, sender=KeyVal)
def add_to_profile(sender, instance, created, **kwargs):
    if created:
        users = AppUser.objects.all()
        # This is required. 
        subject_user = AppUser.objects.all().latest('id')
        # print(subject_user)
        latest = users[::-2][0]  # latest user created
        data = {}
        for user in users:
            interests = user.interests.all()
            data[user.name] = {}
            for interest in interests:
                # data[user.name] = {interest.container.name:float(interest.interest_level)}
                data[user.name].update(
                    {interest.container.name: float(interest.interest_level)})
    persons = list(data.keys())
    l = []
    for person in persons:
        l.append((person, (recommender.euclidean_similarity(
            datas=data, person1=person, person2=latest.name))))
    l.sort()
    l.reverse()
    print(l)
    # print(l)
    group = [subject_user]
    for u in l[:3]:
        # print(u[0])
        group.append(AppUser.objects.get(name=u[0]))

    g = Grp.objects.create()
    g.appUsers.add(*group)
    g.save()