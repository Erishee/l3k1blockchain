from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accueil.urls')),
    path('bitcoin/', include('bitcoin.urls')),
    path('contact/', include('contact.urls')),
    path('api',include('myapi.urls')),
    ###
    path('ethereum/', include('ethereum.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('django_plotly_dash',include('django_plotly_dash.urls')),

]
