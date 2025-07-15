import csv
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .models import User, TemporaryManager
from .serializers import ManagerCreateSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import status


@extend_schema(
    request=ManagerCreateSerializer,
    responses={201: ManagerCreateSerializer},
    description="Create a new manager user with one-time password"
)
class ManagerCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ManagerCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "username": user.username,
            "one_time_password": getattr(user, '_raw_password', 'N/A'),
            "role": user.role
        }, status=status.HTTP_201_CREATED)


@extend_schema(
    parameters=[],
    responses={200: None},
    description="Export selected manager user(s) as CSV file. Use ?username=testuser to filter"
)
class ManagerExportCSVView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        username = request.query_params.get('username')
        queryset = User.objects.filter(role='manager')

        if username:
            queryset = queryset.filter(username=username)

        if not queryset.exists():
            return Response({"detail": "No matching manager found."}, status=404)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="managers.csv"'

        writer = csv.writer(response)
        writer.writerow(['URL', 'Username', 'OneTimePassword', 'Current Role'])

        for manager in queryset:
            reset_url = f"https://yourdomain.com/login/"
            try:
                raw_password = manager.temp_data.raw_password
            except TemporaryManager.DoesNotExist:
                raw_password = 'Not available'
            writer.writerow([
                reset_url,
                manager.username,
                raw_password,
                manager.role
            ])

        return response


