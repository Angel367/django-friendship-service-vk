from django.contrib.auth.decorators import login_required
from .models import User, FriendStatus
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def friends_view(request, user_id):
    user = User.objects.get(id=user_id)
    friend_statuses = FriendStatus.objects.filter(user1=user)

    friends = []
    for friend_status in friend_statuses:
        friends.append(friend_status.user2)

    context = {
        'user': user,
        'friends': friends
    }
    return render(request, 'friends.html', context)


@login_required
def add_friend(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)

        if FriendStatus.objects.filter(user1=request.user, user2=user).exists():
            pass
        else:
            friend_status = FriendStatus()
            friend_status.user1 = request.user
            friend_status.user2 = user
            friend_status.save()

        return redirect('user_list')
    else:
        return redirect("/user_list/")


@login_required
def user_list(request):
    users = User.objects.exclude(pk=request.user.pk)  # Exclude the authenticated user
    statuses = []
    for user in users:
        friend_status = FriendStatus.objects.filter(user1=request.user, user2=user)
        if friend_status.exists():
            pass # if friend_status[0].user1 ==
        else:
            statuses.append("Нет ничего")


    return render(request, 'user_list.html', {'users': users, 'statuses': statuses})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/friends/1')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def index_view(request):
    return render(request, 'index.html', {'isAuth': request.user.is_authenticated})


def create_friend_status(user1, user2):
    # Check if FriendStatus already exists
    if FriendStatus.objects.filter(user1=user1, user2=user2).exists():
        return None  # FriendStatus already exists

    # Create a new FriendStatus
    friend_status = FriendStatus(user1=user1, user2=user2)
    friend_status.save()
    return friend_status
