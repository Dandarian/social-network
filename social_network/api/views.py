from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from django.contrib.auth.models import User
from .models import Post, Like, UserActivity
from .permissions import IsOwnerOrReadOnly, IsNotFanOrReadOnly
import datetime as DT

# Create your views here.


class UserList(generics.ListAPIView):
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
