from django.urls import path
from . import views


from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,)

urlpatterns = [
    path("",views.get_routes,name='get-routes'),
    path('token/',TokenObtainPairView.as_view(),name = 'token_obtain_pair'),
    path('token/refresh',TokenRefreshView.as_view(),name='token_refresh'),
    path('profile/', views.get_profile),
    path('create_user/',views.create_user)
]