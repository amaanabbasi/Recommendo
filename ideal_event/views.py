from django.shortcuts import render
from ideal_event.forms import UserForm, AppUserForm, KeyValForm
from ideal_event.models import AppUser, Interest, Interest2,KeyVal
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from ideal_event.recommender import data, euclidean_similarity, pearson_similarity
import math

def index(request):
    return render(request, 'ideal_event/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def process(request):  # data algo
    persons = list(data.keys())
    for person in persons:
	    print(f"{person}: {euclidean_similarity(person, 'John Backus')}")
    # return render(request, 'ideal_event/process.html')
    # return redirect(request, "ideal_event/process.html")


@login_required
def select_interests(request):
    # select_interest_form = Interest2Form(request.POST or None)
    interest_count = Interest.objects.all().count()
    # for i in range(interest_count):
    form=KeyValForm(request.POST or None)
    interest = Interest.objects.all()
    print(interest_count)
    instance = None
    if request.method == "POST":
        if form.is_valid():
            interest2 = form.save(commit=False)
            interest2.save()
            form.save_m2m()
    # if form.errors:
    #     print(form.errors)
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
        profile_form = AppUserForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = AppUserForm()
    return render(request, 'ideal_event/registration.html',
                  {'user_form': user_form,
                           'profile_form': profile_form,
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

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=KeyVal)
def add_to_profile(sender, instance, created, **kwargs):
    if created:
        users=AppUser.objects.all()
        # latest=AppUser.objects.all().reverse()[0]
        latests=users[::-1][0]
        data = []
        for user in users:
            for i in range(user.interests.all().count()): 
                user_int=user.interests.all()[i].container.name
                user_int_lvl=float(user.interests.all()[i].interest_level)
                usertpl=(user_int, user_int_lvl)
                latest_int=latest.interests.all()[i].container.name
                latest_int_lvl=float(latest.interests.all()[i].interest_level)
                latesttpl=(latest_int,latest_int_lvl)
        for user in users:
            interests=user.interests.all()
            for interest in interests:
                data.append({user.name:{interest.container.name:float(interest.interest_level)}})

                print(data)