from django.db import models
from django.contrib.auth.models import User


class FriendRequest(models.Model):
    """
    Main model of app.
    Provides 3 fields:
        1) sender_user - arrows to user who tried to add new friend
        2) receiver_user - arrows to user who get request from receiver_user
        3) current_status - has 2 options:
            a) pending (0),
            b) accepted (1)
        It is used for explicit declare of current status of request.
    """
    status_pending = 0
    status_accepted = 1

    statuses = (
        (status_pending, 'Pending'),
        (status_accepted, 'Accepted'),
    )

    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_user')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_user')
    current_status = models.IntegerField(choices=statuses, default=status_pending)

    def accept_request(self):
        """
        Method for secure accepting requests.
        :return:
        """
        if self.current_status == self.status_pending:
            self.current_status = self.status_accepted
            self.save()
            return
        raise Exception("Exception: cannot accept cause already accepted")

    def remove(self):
        """
        Method for secure removing requests.
        :return:
        """
        if self.current_status == self.status_pending:
            self.delete()
            return
        raise Exception("Exception: cannot cancel cause already accepted")
