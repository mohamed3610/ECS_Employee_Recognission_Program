from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path("sign_up",views.register, name="register"),
    path("",views.login_view,name = "login"),
    path("logout",views.logout_view, name = "logout"),
    path("mass_upload_users",views.simple_upload , name = "mass_upload_users"),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterView.as_view(), name='auth_register'),
    path('login/', views.getRoutes)
]
