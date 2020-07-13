from rest_framework import viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from base import pagination
from . import serializers
from apps.sheet import models
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from django.utils import timezone


class CheatSheetViewSet(viewsets.ModelViewSet):
    models = models.CheatSheet
    queryset = models.objects.filter(date_published__lte=timezone.now()).order_by('-id')
    serializer_class = serializers.CheatSheetSerializer
    permission_classes = permissions.AllowAny,
    pagination_class = pagination.Pagination
    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ['title']
    lookup_field = 'slug'

    def list(self, request, *args, **kwargs):
        if request.GET.get("all"):
            with connection.cursor() as cursor:
                cursor.execute("SELECT FETCH_SHEETS(%s)", [False])
                out = cursor.fetchone()[0]
            return Response(out)
        else:
            return super(CheatSheetViewSet, self).list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user and (request.user.id == instance.user.id) or request.user.is_staff:
            instance.save(db_status=-1)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        user_id = self.request.user.id if self.request.user.is_authenticated else None
        with connection.cursor() as cursor:
            cursor.execute("SELECT FETCH_SHEET(%s, %s)", [kwargs.get("slug"), user_id])
            out = cursor.fetchone()[0]
        return Response(out)
