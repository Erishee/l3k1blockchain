from django.urls import path,include,re_path
from rest_framework import routers
from . import views

app_name='myapi'

router = routers.DefaultRouter()
router.register(r'BTC_Utilisateur',views.UtilisateurViewSet)
router.register(r'BTC_Bloc',views.BlocViewSet)
router.register(r'BTC_Transations',views.TransactionsViewSet)
router.register(r'BTC_Inputs',views.InputsViewSet)
router.register(r'BTC_Outputs',views.OutputsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/',include('rest_framework.urls'))
]