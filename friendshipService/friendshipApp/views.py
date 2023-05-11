from django.contrib.auth.decorators import login_required
from .models import User, FriendRequest
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def friends_view(request):
    """
    View for page /friends/
    :param request:
    :return:
    """
    friends = FriendshipHandler.get_friends(request.user)

    context = {
        'user': request.user,
        'friends': friends
    }
    return render(request, 'friends.html', context)


@login_required
def add_friend(request):
    """
    View for page "/add_friend/"
    :param request:
    :return:
    """
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)

        FriendshipHandler.send_friend_request(request.user, user)
        return redirect('/')


@login_required
def user_list(request):
    """
    View for page "/user_list/"
    :param request:
    :return:
    """
    users = User.objects.exclude(pk=request.user.pk)  # Exclude the authenticated user
    result = []
    for user in users:
        one_record = [user, FriendshipHandler.get_friendship_status(request.user, user)]
        result.append(one_record)
    print(result)
    return render(request, 'user_list.html', context={'result': result})


def register_view(request):
    """
    View for registration page "/register/"
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def index_view(request):
    """
    View for main index page "/", "/index/"
    :param request:
    :return:
    """
    return render(request, 'index.html', {'isAuth': request.user.is_authenticated})


@login_required
def received_requests_view(request):
    """
    View for page "/received_requests/"
    :param request:
    :return:
    """
    received_requests = FriendRequest.objects.filter(receiver_user=request.user,
                                                     current_status=FriendRequest.status_pending)
    return render(request, 'received_requests.html',
                  context={'user': request.user, 'received_requests': received_requests})


@login_required
def sent_requests_view(request):
    """
    View for page "/received_requests/"
    :param request:
    :return:
    """
    sent_requests = FriendRequest.objects.filter(sender_user=request.user,
                                                 current_status=FriendRequest.status_pending)
    return render(request, 'received_requests.html',
                  context={'user': request.user, 'sent_requests': sent_requests})


@login_required
def all_requests_view(request):
    """
    View for page "/received_requests/"
    :param request:
    :return:
    """
    all_requests = set(FriendRequest.objects.filter(sender_user=request.user,
                                                                      current_status=FriendRequest.status_pending) |
                       FriendRequest.objects.filter(receiver_user=request.user,
                                                    current_status=FriendRequest.status_pending))
    return render(request, 'all_requests.html',
                  context={'user': request.user, 'all_requests': all_requests})


class FriendshipHandler:
    """
    Contains methods fot interaction with model "FriendRequest".
    It adds failsafe methods with explicit and understandable error messages
    """

    @staticmethod
    def send_friend_request(from_user, to_user):
        """
        Creates new FriendRequest implementation or edit old if it is match (X-request)
        :param from_user: Object user - sender
        :param to_user: Object user - receiver
        :return:
        """
        if from_user != to_user:
            old_friendship, new_friendship = FriendRequest.objects.get_or_create(sender_user=from_user,
                                                                                 receiver_user=to_user)
            if new_friendship:
                cross_request = FriendRequest.objects.filter(sender_user=to_user, receiver_user=from_user,
                                                             current_status=FriendRequest.status_pending).first()
                if cross_request:
                    old_friendship.accept_request()
                    cross_request.accept_request()
            else:
                raise Exception("Friend request already exists")
        else:
            raise Exception("Attempt to send request from this user to this user")

    @staticmethod
    def remove_friend(from_user, to_user):
        """
        deletes FriendRequest connection between users
        :param from_user: Object user - sender
        :param to_user: Object user - receiver
        :return:
        """
        FriendRequest.objects.filter(sender_user=from_user,
                                     receiver_user=to_user, current_status=FriendRequest.status_accepted).remove()
        FriendRequest.objects.filter(sender_user=to_user,
                                     receiver_user=from_user, current_status=FriendRequest.status_accepted).remove()

    @staticmethod
    def get_friendship_status(from_user, to_user):
        """
        Interface for getting status of FriendRequest between 2 users in comfortable format
        :param from_user:
        :param to_user:
        :return:
        """
        if FriendRequest.objects.filter(sender_user=from_user, receiver_user=to_user,
                                        current_status=FriendRequest.status_accepted).exists():
            return "Друзья"
        elif FriendRequest.objects.filter(sender_user=to_user, receiver_user=from_user,
                                          current_status=FriendRequest.status_accepted).exists():
            return "Друзья"
        elif FriendRequest.objects.filter(sender_user=from_user, receiver_user=to_user,
                                          current_status=FriendRequest.status_pending).exists():
            return "Исходящий запрос"
        elif FriendRequest.objects.filter(sender_user=to_user, receiver_user=from_user,
                                          current_status=FriendRequest.status_pending).exists():
            return "Входящий запрос"
        else:
            return "Ничего"

    @staticmethod
    def get_friends(user):
        """
        returns all user friends without duplicates
        :param user:
        :return:
        """
        friends = []
        sent_friendships = FriendRequest.objects.filter(sender_user=user, current_status=FriendRequest.status_accepted)
        received_friendships = FriendRequest.objects.filter(receiver_user=user,
                                                            current_status=FriendRequest.status_accepted)
        for friendship in sent_friendships:
            friends.append(friendship.receiver_user)
        for friendship in received_friendships:
            if friendship.sender_user not in friends:
                friends.append(friendship.sender_user)
        return friends

    @staticmethod
    def get_outgoing_requests(user):
        return FriendRequest.objects.filter(sender_user=user, current_status=FriendRequest.status_pending)
