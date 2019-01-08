from django.shortcuts import render
from ideal_event.forms import UserForm, AppUserForm, Interest2Form
from ideal_event.models import AppUser, Interest, Interest2
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


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
    import pdb
    pdb.set_trace()
    pass
    # return render(request, 'ideal_event/process.html')
    # return redirect(request, "ideal_event/process.html")


@login_required
def select_interests(request):
    select_interest_form = Interest2Form(request.POST or None)
    interest = Interest.objects.all()
    instance = None
    if request.method == "POST":
        if select_interest_form.is_valid():
            print(select_interest_form.cleaned_data['interest_name'])
            print(select_interest_form.cleaned_data['interest_level'])
            interest2 = select_interest_form.save(commit=False)
            interest2.save()
            select_interest_form.save_m2m()
    if select_interest_form.errors:
        print(select_interest_form.errors)
    context = {
        "select_interest_form": select_interest_form,
        "interest": interest,
        "instance": instance
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
