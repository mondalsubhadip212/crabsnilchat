# from django.shortcuts import render

# Create your views here.
# custom import
from .serializer import SignUp_User_Creation_Serializer
from .friends import Friend_Search,\
    Add_friend, Cancel_request,\
    Accept_request, Unfriend
from .models import User, User_Friends

# python import
# import time
# import json

# django core import

from django.contrib.auth import authenticate

# rest api import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication

# simple jwt import
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

# constant variable
client_url = 'http://127.0.0.1:5501'


# <<<<<<<<<<<<<<<<<<<<<<< main function and classes starts from here >>>>>>>>>>>>>>>>>>>>>>
# <<<<<<<<<<<<<<<<<<<<<<< main function and classes starts from here >>>>>>>>>>>>>>>>>>>>>>


# user sign_up
class SignUp_User_Creation(APIView):

    def post(self, request):
        new_user_details = SignUp_User_Creation_Serializer(data=request.data)
        if new_user_details.is_valid():
            new_user_details.create(new_user_details)
            return Response({'success': 'account created :)'}, status=status.HTTP_201_CREATED)
        elif request.data['password1'] == '' or request.data['password1'] == '':
            return Response(
                {'error': 'no password given...seriously bro !'}, headers={
                    "Access-Control-Allow-Methods": "POST"
                })
        else:
            return Response(
                {'error': 'an account already exist with this credentials or email,username must be unique :('})


# user login and send user details - email,user_id,username
class Login(APIView):

    def get(self, request):
        return Response({'success': 'okay'}, headers={
            'Access-Control-Allow-Origin': client_url,
            'Access-Control-Allow-Headers': 'Authorization',
        }, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            login_user = authenticate(username=request.data['username'], password=request.data['password'])
            if login_user.is_authenticated:
                refresh_token = RefreshToken.for_user(user=login_user)
                user_details = User.objects.get(pk=login_user.email)
                res = Response(data={'success': 'successfully login :)',
                                     'username': user_details.username,
                                     'email': user_details.email,
                                     'userid': user_details.userid},
                               headers={
                                   'Authorization': 'refresh ' + str(refresh_token) + ';access ' + str(
                                       refresh_token.access_token),
                                   'Access-Control-Allow-Origin': client_url,
                                   'Access-Control-Expose-Headers': 'Authorization',
                               },
                               status=status.HTTP_200_OK)
                return res
            else:
                return Response(data={'error': 'invalid credential\'s :('}, status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(data={'error': 'user not found :('}, status=status.HTTP_404_NOT_FOUND)


# user details - sending user details
class user_details(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_friend = User_Friends.objects.get(user=request.user).friend
        user_friend_request = User_Friends.objects.get(user=request.user).friend_request
        user_friend_block_list = User_Friends.objects.get(user=request.user).friend_block_list
        user_friend_request_pending = User_Friends.objects.get(user=request.user).friend_request_pending

        return Response(data={'success': 'Okey',
                              'username': request.user.username,
                              'email': request.user.email,
                              'userid': request.user.userid,
                              'friends': user_friend['friends'],
                              'friend_request': user_friend_request['friend_request'],
                              'friend_block_list': user_friend_block_list['friend_block_list'],
                              'friend_request_pending': user_friend_request_pending['friend_request_pending']
                              }, headers={
            # 'Access-Control-Allow-Headers': "Authorization",
            # 'Access-Control-Allow-Origins': client_url,
            # 'WWW-Authenticate': "Bearer",
            # 'Access-Control-Allow-Methods': "get"
        }, status=status.HTTP_200_OK)


# user add friends
class friend_search(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data['email']
        try:
            find_user = User.objects.get(pk=email)
        except:
            return Response(status=status.HTTP_200_OK, data={'error': "no account found :("})

        # calling the friends.py for checking
        # if the find_user is already present or not in any place
        check_find_user = Friend_Search(request.user)

        # check if the find_user username is present in your friend list
        if check_find_user.check_find_user_in_friend(find_user_username=find_user.username,
                                                     find_user_email=find_user.email):
            return Response(status=status.HTTP_200_OK,
                            data={
                                'username': find_user.username,
                                'email': find_user.email,
                                'status': 'friend'
                            })

        # check if the find_user username is present in your friend request list
        elif check_find_user.check_find_user_in_friend_request(find_user_username=find_user.username,
                                                               find_user_email=find_user.email):
            return Response(status=status.HTTP_200_OK,
                            data={
                                'username': find_user.username,
                                'email': find_user.email,
                                'status': 'friend_request'
                            })

        # check if the find_user username is present in your friend block list
        elif check_find_user.check_find_user_in_friend_block_list(find_user_username=find_user.username,
                                                                  find_user_email=find_user.email):
            return Response(status=status.HTTP_200_OK,
                            data={
                                'username': find_user.username,
                                'email': find_user.email,
                                'status': 'friend_block_list'
                            })

        # check if the find_user username is present in your friend request pending list
        elif check_find_user.check_find_user_in_friend_request_pending(find_user_username=find_user.username,
                                                                       find_user_email=find_user.email):
            return Response(status=status.HTTP_200_OK,
                            data={
                                'username': find_user.username,
                                'email': find_user.email,
                                'status': 'friend_request_pending'
                            })

        # if the user is not present in your any above list or the same user is searched
        else:
            if find_user.username == request.user.username:
                return Response(status=status.HTTP_200_OK,
                                data={
                                    'username': find_user.username,
                                    'email': find_user.email,
                                    'status': 'same_user'
                                })

            return Response(status=status.HTTP_200_OK,
                            data={
                                'username': find_user.username,
                                'email': find_user.email,
                                'status': 'not_in_list'
                            })


class add_friend(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_user = request.user

        try:
            add_friend_user = User.objects.get(pk=request.data['email'])

        except:
            return Response(status=status.HTTP_200_OK, data={
                'error': 'user not found'
            })

        add_friend_obj = Add_friend(current_user, add_friend_user)
        if add_friend_obj.check_if_include_in_other_list(add_friend_user.username, add_friend_user.email):
            return Response(status=status.HTTP_200_OK, data={
                'error': 'something went wrong'
            })
        return Response(status=status.HTTP_200_OK, data={
            'success': 'request sent',
        })


class cancel_request(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_user = request.user
        try:
            cancel_request_user = User.objects.get(pk=request.data['email'])

        except:
            return Response(status=status.HTTP_200_OK, data={
                'error': 'user not found'
            })

        cancel_request_obj = Cancel_request(current_user, cancel_request_user)
        if cancel_request_obj.cancel():
            return Response(status=status.HTTP_200_OK, data={
                'success': 'Cancelled'
            })
        else:
            return Response(status=status.HTTP_200_OK, data={
                'error': "this action is not possible right now"
            })


class accept_request(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_user = request.user
        try:
            accept_request_user = User.objects.get(pk=request.data['email'])

        except:
            return Response(status=status.HTTP_200_OK, data={
                'error': 'user not found'
            })
        accept_request_obj = Accept_request(current_user, accept_request_user)
        if accept_request_obj.accept():
            return Response(status=status.HTTP_200_OK, data={
                'success': 'Accepted'
            })
        else:
            return Response(status=status.HTTP_200_OK, data={
                'error': "this action is not possible right now"
            })


class deny_request(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_user = request.user
        try:
            deny_user = User.objects.get(pk=request.data['email'])

        except:
            return Response(status=status.HTTP_200_OK, data={
                'error': 'user not found'
            })
        deny_user_obj = Accept_request(current_user, deny_user)
        if deny_user_obj.remove_from_list():
            return Response(status=status.HTTP_200_OK, data={
                'success': 'Removed'
            })
        else:
            return Response(status=status.HTTP_200_OK, data={
                'error': "this action is not possible right now"
            })


class unfriend(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_user = request.user
        try:
            unfriend_user = User.objects.get(pk=request.data['email'])

        except:
            return Response(status=status.HTTP_200_OK, data={
                'error': 'user not found'
            })
        unfriend_user_obj = Unfriend(current_user, unfriend_user)
        if unfriend_user_obj.unfriend():
            return Response(status=status.HTTP_200_OK, data={
                'success': 'Removed'
            })
        else:
            return Response(status=status.HTTP_200_OK, data={
                'error': "this action is not possible right now"
            })

# user logout - using memcached - (pending)
# class logout(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         # refresh_token_for_blacklist = RefreshToken(request.auth)
#         # refresh_token_for_blacklist.check_blacklist()
#         return Response({"post": "post method done"}, status=status.HTTP_200_OK)
