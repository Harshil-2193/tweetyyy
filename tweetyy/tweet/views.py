from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
# Create your views here.
def index(request):
    return render(request, "index.html")


@login_required
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