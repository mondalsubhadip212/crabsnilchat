from .models import User_Friends


# searching a friend
class Friend_Search:

    def __init__(self, current_user):
        self.current_user = current_user
        self.current_user_friends_model = User_Friends.objects.get(pk=current_user.email)
        self.current_user_friends = self.current_user_friends_model.friend['friends']
        self.current_user_friend_request = self.current_user_friends_model.friend_request['friend_request']
        self.current_user_friend_block_list = self.current_user_friends_model.friend_block_list['friend_block_list']
        self.current_user_friend_request_pending = self.current_user_friends_model.friend_request_pending[
            'friend_request_pending']

    def check_in(self, find_user_username, find_user_email, current_details):
        for data in current_details:
            if find_user_username == data['username'] and find_user_email == data['email']:
                return True

    def check_find_user_in_friend(self, find_user_username, find_user_email):
        if self.check_in(find_user_username, find_user_email, self.current_user_friends):
            return True

    def check_find_user_in_friend_request(self, find_user_username, find_user_email):
        if self.check_in(find_user_username, find_user_email, self.current_user_friend_request):
            return True

    def check_find_user_in_friend_block_list(self, find_user_username, find_user_email):
        if self.check_in(find_user_username, find_user_email, self.current_user_friend_block_list):
            return True

    def check_find_user_in_friend_request_pending(self, find_user_username, find_user_email):
        if self.check_in(find_user_username, find_user_email, self.current_user_friend_request_pending):
            return True


# add a friend
class Add_friend(Friend_Search):

    def __init__(self, current_user, add_friend_user):
        self.add_friend_user = add_friend_user
        Friend_Search.__init__(self, current_user)

    def check_if_include_in_other_list(self, find_user_username, find_user_email):
        in_friends = self.check_find_user_in_friend(find_user_username, find_user_email)
        in_friend_request = self.check_find_user_in_friend_request(find_user_username, find_user_email)
        in_block = self.check_find_user_in_friend_block_list(find_user_username, find_user_email)
        in_pending = self.check_find_user_in_friend_request_pending(find_user_username, find_user_email)

        if (in_friends or in_friend_request or in_block or in_pending) is True:
            return True
        else:
            try:
                # adding this user (find user) to my sent request list friend_request(model name)
                my_sent_request = User_Friends.objects.get(user=self.current_user)
                my_sent_request.friend_request_pending["friend_request_pending"].append({
                    "username": "{}".format(find_user_username),
                    "email": "{}".format(find_user_email)
                })
                my_sent_request.save()

                # adding me into the find user pending request list
                friend_receive_request = User_Friends.objects.get(user=self.add_friend_user)
                friend_receive_request.friend_request['friend_request'].append({
                    "username": "{}".format(self.current_user.username),
                    "email": "{}".format(self.current_user.email)
                })
                friend_receive_request.save()
                return False
            except:
                return True


# cancel a sent request
class Cancel_request:
    def __init__(self, current_user, cancel_request_user):
        self.current_user = current_user
        self.current_user_friends_model = User_Friends.objects.get(pk=current_user.email)
        self.current_user_friend_request_pending = self.current_user_friends_model.friend_request_pending[
            'friend_request_pending']
        self.cancel_request_user = cancel_request_user
        self.cancel_request_user_friends_model = User_Friends.objects.get(pk=cancel_request_user)
        self.cancel_request_user_friend_request = self.cancel_request_user_friends_model.friend_request[
            'friend_request']

    def cancel(self):

        valid_1 = False
        valid_2 = False

        # to check if the current user is present on cancel request user pending list
        for data in self.cancel_request_user_friend_request:
            if self.current_user.username == data['username'] and self.current_user.email == data['email']:
                valid_1 = True
                break

        # to check if the cancel request user is present on current user sent request list
        for data in self.current_user_friend_request_pending:
            if self.cancel_request_user.username == data['username'] and self.cancel_request_user.email == data[
                'email']:
                valid_2 = True
                break

        # if both are valid then the data will remove from both the user
        if valid_1 and valid_2:
            # removing cancel_request user from my sent request list
            self.current_user_friend_request_pending.remove({
                "username": self.cancel_request_user.username,
                "email": self.cancel_request_user.email
            })
            self.current_user_friends_model.save()

            # removing me from cancel_request user pending list
            self.cancel_request_user_friend_request.remove({
                "username": self.current_user.username,
                "email": self.current_user.email
            })
            self.cancel_request_user_friends_model.save()
            return True
        else:
            return False


# accept a pending request
class Accept_request:
    def __init__(self, current_user, accept_request_user):
        self.current_user = current_user
        self.current_user_friends_model = User_Friends.objects.get(pk=current_user.email)
        self.current_user_friend_request = self.current_user_friends_model.friend_request[
            'friend_request']
        self.current_user_friend_list = self.current_user_friends_model.friend['friends']
        self.accept_request_user = accept_request_user
        self.accept_request_user_friends_model = User_Friends.objects.get(pk=accept_request_user)
        self.accept_request_user_friend_request_pending = self.accept_request_user_friends_model.friend_request_pending[
            'friend_request_pending']
        self.accept_request_user_friend_list = self.accept_request_user_friends_model.friend['friends']

    def remove_from_list(self):
        valid_1 = False
        valid_2 = False

        # to check if the current user is present on accept request user pending list
        for data in self.accept_request_user_friend_request_pending:
            if self.current_user.username == data['username'] and self.current_user.email == data['email']:
                valid_1 = True
                break

        # to check if the accept request user is present on current user sent request list
        for data in self.current_user_friend_request:
            if self.accept_request_user.username == data['username'] and self.accept_request_user.email == data['email'
            ]:
                valid_2 = True
                break

        # if both are valid then the data will remove from both the user
        if valid_1 and valid_2:
            # removing accept_request user from my friend request list
            self.current_user_friend_request.remove({
                "username": self.accept_request_user.username,
                "email": self.accept_request_user.email
            })
            self.current_user_friends_model.save()

            # removing me from accept_request user sent request list
            self.accept_request_user_friend_request_pending.remove({
                "username": self.current_user.username,
                "email": self.current_user.email
            })
            self.accept_request_user_friends_model.save()
            return True
        else:
            return False

    def accept(self):

        if self.remove_from_list():
            # adding accept_user in my friend list
            self.current_user_friend_list.append({
                "username": self.accept_request_user.username,
                "email": self.accept_request_user.email
            })
            self.current_user_friends_model.save()

            # adding me in accept_user friend_list
            self.accept_request_user_friend_list.append({
                "username": self.current_user.username,
                "email": self.current_user.email
            })
            self.accept_request_user_friends_model.save()
            return True
        else:
            return False


class Unfriend:

    def __init__(self, current_user, unfriend_user):
        self.current_user = current_user
        self.current_user_friends_model = User_Friends.objects.get(pk=current_user.email)
        self.current_user_friend_list = self.current_user_friends_model.friend['friends']
        self.accept_request_user = unfriend_user
        self.accept_request_user_friends_model = User_Friends.objects.get(pk=unfriend_user)
        self.accept_request_user_friend_list = self.accept_request_user_friends_model.friend['friends']

    def unfriend(self):
        valid_1 = False
        valid_2 = False

        # to check if the current user is present unfriend_user friend list
        for data in self.accept_request_user_friend_list:
            if self.current_user.username == data['username'] and self.current_user.email == data['email']:
                valid_1 = True
                break

        # to check if the unfriend_user is present on current user friend list
        for data in self.current_user_friend_list:
            if self.accept_request_user.username == data['username'] and self.accept_request_user.email == data['email'
            ]:
                valid_2 = True
                break

        # if both are valid then the data will remove from both the user friend list
        if valid_1 and valid_2:
            # removing accept_request user from my friend list
            self.current_user_friend_list.remove({
                "username": self.accept_request_user.username,
                "email": self.accept_request_user.email
            })
            self.current_user_friends_model.save()

            # removing me from accept_user friend list
            self.accept_request_user_friend_list.remove({
                "username": self.current_user.username,
                "email": self.current_user.email
            })
            self.accept_request_user_friends_model.save()
            return True
        else:
            return False