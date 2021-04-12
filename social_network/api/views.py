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
        # определяется юзер айди
        user_id = user.id
        print(user_id)
        # берём нужного юзера
        user_activity_object = UserActivity.objects.filter(id=user_id)[0]
        # и потом в базу данных записывается время этому юзеру
        user_activity_object.last_login = DT.datetime.now(
            tz=get_current_timezone())
        user_activity_object.save()

    def get_final_list(self, body):
        body_loads = json.loads(body)
        user_objects = User.objects.filter(
            username=body_loads['username'])
        # Проверка существования юзера
        if user_objects.count() == 1:
            user = user_objects[0]
            # Проверка верности пароля
            if check_password(body_loads['password'], user.password):
                self.save_last_login(user)
                return self.get_tokens_for_user(user)
            else:
                return False
        else:
            return False

    def post(self, request):
        final_list = self.get_final_list(request.body)
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


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class PostList(generics.ListCreateAPIView):
    '''ListCreateAPIView предоставляет распространенный обработчик
    API-методов: get и post для списка.
    '''
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    # IsAuthenticatedOrReadOnly встроен в rest_framework
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        ''' Чтобы при создании указывался авторизованный юзер
        '''
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    '''RetrieveUpdateDestroyAPIView предоставляет распространенный обработчик
    API-методов: get, update и delete для одной сущности.
    '''
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    # IsOwnerOrReadOnly мы создали в файле permissions
    # Здесь нужны оба разрешения, поскольку обновлять или удалять пост должен
    # только залогиненный пользователь, а также его владелец.
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
    '''RetrieveDestroyAPIView здесь отличается, что только
    API-методы: get и delete для одной сущности.
    '''
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class AnalyticsList(APIView):
    def get_analytics_one_date(self, date):
        '''Возвращает аналитику за одну дату
        '''
        # Считает кол-во лайков за определённую дату
        number_of_likes = Like.objects.filter(
            created=date).count()
        return {'date': date, 'number_of_likes': number_of_likes}

    def get_dates(self, query_params):
        '''Возвращает список дат от начальной до конечной
        '''
        date_from = DT.datetime.strptime(
            query_params['date_from'], '%Y-%m-%d').date()
        date_to = DT.datetime.strptime(
            query_params['date_to'], '%Y-%m-%d').date()
        dates_period = [date_from, date_to]
        print (dates_period)
        delta = date_to - date_from
        dates = [date_from + DT.timedelta(i) for i in range(delta.days + 1)]
        print (dates)
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
    '''ListCreateAPIView предоставляет распространенный обработчик
    API-методов: get для списка.
    '''
    queryset = UserActivity.objects.all()
    serializer_class = serializers.UserActivitySerializer


class UserActivityDetail(generics.RetrieveAPIView):
    queryset = UserActivity.objects.all()
    serializer_class = serializers.UserActivitySerializer
