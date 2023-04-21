from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .settings import DEBUG


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('board.urls')),

]
if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
