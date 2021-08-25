from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('courses/', include("courses.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=str(settings.MEDIA_ROOT))
