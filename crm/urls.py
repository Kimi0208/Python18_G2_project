from django.contrib import admin
from django.urls import path, include

urls_api = [
    path('v1/', include('api.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webapp.urls')),
    path('accounts/', include('accounts.urls')),
    path('api/', include(urls_api)),
]
