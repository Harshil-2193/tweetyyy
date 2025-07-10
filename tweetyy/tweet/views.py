from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import *
from .forms import *
# Create your views here.
def index(request):
    return render(request, "index.html")


def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, "tweet_list.html", {'tweets': tweets})

@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            messages.success(request, "Tweet posted successfully!")
            return redirect('tweet_list')
        else:
            print("Form Errors:", form.errors) 
            messages.error(request, "Something went wrong. Tweet is not posted.")
    else:
        form = TweetForm()
    return render(request, "tweet_form.html", {"form": form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            messages.success(request, "Tweet updated successfully")
            return redirect('tweet_list')
        else:
            messages.error(request, "Update failed. Something went wrong.")
            print(form.errors)
    else:
        form = TweetForm(instance=tweet)

    return render(request, "tweet_form.html", {"form": form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    
    tweet.delete()
    messages.success(request, "Tweet deleted successfully.")
    return redirect('tweet_list')  

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            messages.success(request, "User Registration Successfull.")
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register_page.html', {'form': form})

def login_view(request):
    form = None
    if request.method == "POST":
        form  = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            messages.success(request,"Login Successfull")
            return redirect('tweet_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login_page.html", {'form':form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('register_page')