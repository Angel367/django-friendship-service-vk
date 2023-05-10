from django.shortcuts import render
from .models import User, FriendStatus


def view_friends(request, user_id):
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
