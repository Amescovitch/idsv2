from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('ids/', admin.site.urls),
    path('ids-demande/', include('applicationidsdemande.urls')),
    path('ids-demande/', include ( "django.contrib.auth.urls" )),
    path('', lambda request: redirect("ids-demande/",permament=False)),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "applicationidsdemande.views.handler404"
    