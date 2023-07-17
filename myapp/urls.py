from django.urls import path
from .views import UserSignUpView, ForgotPasswordView, StudentDetailView, LoginView, TeacherStudentsView, AdminUserView

urlpatterns = [
    path('signup', UserSignUpView.as_view(), name='user-signup'),
    path('forgot-password', ForgotPasswordView.as_view(), name='user-forgot-password'),
    path('student', StudentDetailView.as_view(), name='student-info'),
    path('login', LoginView.as_view(), name='login'),
    path('teacher/students', TeacherStudentsView.as_view(), name='teacher-student-list'),
    path('users', AdminUserView.as_view(), name='admin-user-list'),
]
