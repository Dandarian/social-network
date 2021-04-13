from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from django.contrib.auth.models import User
from .models import Post, Like, UserActivity
from .permissions import IsOwnerOrReadOnly, IsNotFanOrReadOnly
import datetime as DT
from django.utils.timezone import get_current_timezone
from rest_framework_simplejwt.tokens import RefreshToken
import json
from django.contrib.auth.hashers import check_password

# Create your views here.


class Login(generics.CreateAPIView):
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def save_last_login(self, user):
        user_id = user.id
        user_activity_object = UserActivity.objects.filter(id=user_id)[0]
        user_activity_object.last_login = DT.datetime.now(
            tz=get_current_timezone())
        user_activity_object.save()

    def get_final_list(self, body_loads):
        user_objects = User.objects.filter(
            username=body_loads['username'])
        # Is user exists?
        if user_objects.count() == 1:
            user = user_objects[0]
            # Is password correct?
            if check_password(body_loads['password'], user.password):
                self.save_last_login(user)
                return self.get_tokens_for_user(user)
            else:
                return False
        else:
            return False

    def post(self, request):
        body_loads = json.loads(request.body)
        if "username" not in body_loads:
            return Response(
                {
                    "username": [
                        "This field is required."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if "password" not in body_loads:
            return Response(
                {
                    "password": [
                        "This field is required."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        final_list = self.get_final_list(body_loads)
        if final_list is False:
            return Response(
                {
                    "detail":
                        "No active account found with the given credentials"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            return Response(
                final_list,
                status=status.HTTP_200_OK
            )


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserCreateSerializer


class PostList(generics.ListCreateAPIView):
    '''ListCreateAPIView gives a common handler of
    API-methods: get и post for the list.
    '''
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    # IsAuthenticatedOrReadOnly is from rest_framework.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        ''' Specify an authorized user when creating post.
        '''
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    '''RetrieveUpdateDestroyAPIView gives a common handler of
    API-methods: get, update и delete for one entity.
    '''
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    # IsOwnerOrReadOnly is from file permissions.py
    # Here we need both permissions, cause only
    # authorized owner can delete.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class LikeList(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsNotFanOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    '''RetrieveDestroyAPIView
    API-methods: get и delete for one entity.
    '''
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class AnalyticsList(APIView):
    ''' Total likes to all posts.
    '''
    def get_analytics_one_date(self, date):
        # For one date.
        number_of_likes = Like.objects.filter(
            created=date).count()
        return {'date': date, 'number_of_likes': number_of_likes}

    def get_dates(self, query_params):
        '''Returns date list from first date to last.
        '''
        date_from = DT.datetime.strptime(
            query_params['date_from'], '%Y-%m-%d').date()
        date_to = DT.datetime.strptime(
            query_params['date_to'], '%Y-%m-%d').date()
        delta = date_to - date_from
        dates = [date_from + DT.timedelta(i) for i in range(delta.days + 1)]
        return dates

    def get_final_list(self, query_params):
        dates = self.get_dates(query_params)
        final_list = []
        for date in dates:
            analytics_one_date = self.get_analytics_one_date(date)
            final_list.append(analytics_one_date)
        return final_list

    def get(self, request):
        final_list = self.get_final_list(request.query_params)
        return Response(
            final_list,
            status=status.HTTP_200_OK
        )


class UserActivityList(generics.ListAPIView):
    '''ListCreateAPIView
    API-methods: get for the list.
    '''
    queryset = UserActivity.objects.all()
    serializer_class = serializers.UserActivitySerializer


class UserActivityDetail(generics.RetrieveAPIView):
    queryset = UserActivity.objects.all()
    serializer_class = serializers.UserActivitySerializer
