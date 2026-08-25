from django.urls import path

from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('signup/', views.UserSignUpView.as_view(), name='signup'),

    path('password-reset/', views.UserPasswordResetView.as_view(),name='password_reset'),
    path('password-reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/',views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
