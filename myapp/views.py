from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Student
from .serializers import UserSerializer, StudentSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

class UserSignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self,request):
        # Retrieve the serializer instance
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the user object
            serializer.save()
            return Response({'Status':200,"Message":'Registeration Done SuccessFully','Results':serializer.data})
        else:
            return Response({'Status':404,"Message":'Error'})
        
class ForgotPasswordView(generics.GenericAPIView):

    def post(self, request):
        # Retrieve email and password from request data
        email = request.data.get('email')
        user_password = request.data.get('password')
        # Check if email field is present
        if not email:
            return Response({'Status':404,"Message":'email field cannot be blank'})
        # Check if password field is present
        if not user_password:
            return Response({'Status':404,"Message":'password not found'})
        try:
            # Retrieve the user based on the provided email
            user = User.objects.filter(email=email).first()
        except User.DoesNotExist:
            return Response({'Status':404,"Message":'Error'})
        # Set the user's password and save the user
        user.set_password(user_password)
        user.save()

        return Response({'Status': 200, 'Message': 'Password updated successfully.'})


class LoginView(generics.GenericAPIView):

    def post(self, request):
        # Retrieve username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            # generate access token
            access_token = str(refresh.access_token)

            return Response({'access_token': access_token})
        else:
            return Response({'error': 'Invalid credentials'})
        
class StudentDetailView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # student can fetch own details
        if request.user.user_level == 'Student':
            try:
                # Retrieve the user
                student = Student.objects.get(user=request.user)
                serializer = StudentSerializer(student)
                return Response(serializer.data, status=200)
            except Student.DoesNotExist:
                return Response({'Message': 'Student information not found.'}, status=404)
        else:
            return Response({'Message': 'Access forbidden.'}, status=403)
        

class TeacherStudentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve a list of all students
        if request.user.user_level == 'Teacher':
            students = Student.objects.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({'Message': 'Access forbidden.'}, status=403)

    def post(self, request):
        # Create a new user
        if request.user.user_level == 'Teacher':
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({'Message': 'Access forbidden.'}, status=403)


class AdminUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve a list of all users
        if request.user.user_level == 'Super-admin':
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response({'Message': 'Access forbidden.'}, status=403)
        
    def post(self, request):
        # Create a new user
        if request.user.user_level == 'Super-admin':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)
        else:
            return Response({'Message': 'Access forbidden.'}, status=403)
    