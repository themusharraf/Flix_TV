from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from core import settings

from users.urls import app_name as user_app_name
from movie.urls import app_name as movie_app_name
from dashboard.urls import app_name as dash_app_name

# Swagger --------------------------------------------------------------------------------


schema_view = get_schema_view(
    openapi.Info(
        title="FlixTV API",
        default_version='v1.01',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),

    path('api/v1/users/', include('users.urls', namespace=user_app_name)),
    path('api/v1/movie/', include('movie.urls', namespace=movie_app_name)),
    path('api/v1/dashboard/', include('dashboard.urls', namespace=dash_app_name)),
    path('api/v1/find/', include('elastic_search.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
