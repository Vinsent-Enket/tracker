from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from tracker.models import Addiction, NiceAddiction, Periodicity
from tracker.paginators import AddictionPagination
from tracker.serializers import AddictionSerializer, PeriodicitySerializer
from users.permission import IsProprietor, IsPublic


def index(request):
    return render(request, 'tracker/index.html')


# Create your views here.


class AddictionViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для вывода привычек
    """
    queryset = Addiction.objects.all()
    serializer_class = AddictionSerializer
    pagination_class = AddictionPagination

    def get_permissions(self):
        """
        Права доступа к привычкам, лист и ретрив доступны либо владельцу, либо если объект публичный
        :return:
        """
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, IsProprietor | IsPublic]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsProprietor | IsPublic]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, IsProprietor]
        elif self.action == 'partial_update':
            self.permission_classes = [IsAuthenticated, IsProprietor]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, IsProprietor]
        return [permission() for permission in self.permission_classes]


class PeriodicityUpdateAPIView(generics.UpdateAPIView):
    serializers = PeriodicitySerializer
    permission_classes = [IsAuthenticated, IsProprietor]

    def update(self, *args, **kwargs):
        """
        Для обновления периодичности привычки нужно передать ее id и новые данные
        :param args:
        :param kwargs:
        :return:
        """

        periodicity_id = self.request.data.get('periodicity_id')
        try:
            periodicity = get_object_or_404(Periodicity, pk=periodicity_id)
            periodicity.on_Monday = self.request.data.get('on_Monday')
            periodicity.on_Tuesday = self.request.data.get('on_Tuesday')
            periodicity.on_Wednesday = self.request.data.get('on_Wednesday')
            periodicity.on_Thursday = self.request.data.get('on_Thursday')
            periodicity.on_Friday = self.request.data.get('on_Friday')
            periodicity.on_Saturday = self.request.data.get('on_Saturday')
            periodicity.on_Sunday = self.request.data.get('on_Sunday')
            periodicity.save()
            message = f'У привычки {periodicity.addiction_set} произведена смена периодичности'
        except periodicity.DoesNotExist:
            message = f'Передан некоректный id - {periodicity_id}'
        except KeyError:
            message = 'Не переданы все поля'

        return Response({'message': message})
