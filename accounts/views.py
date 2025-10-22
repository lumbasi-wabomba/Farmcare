from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsAdminOrOwner
from django.contrib.auth import authenticate, get_user_model
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from .models import CustUser, Salary
from .serializer import CustUserSerializer, SalarySerializer

# Create your views here.
class RegisterClerkView(APIView):
    permission_classes =[IsAdminOrOwner, IsAuthenticated]
    authentication_classes = [TokenAuthentication]
   
    def post(self, request):
        serializer = CustUserSerializer(data=request.data)
        if serializer.is_valid():
            user = get_user_model()
            user = CustUser.objects.create_user(**serializer.validated_data)
            return Response({"user": CustUserSerializer(user).data},status=status.HTTP_201_CREATED, template_name='register_clerk')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username_or_email = request.data.get("username")
        user_password = request.data.get("password")
        user = authenticate(username=username_or_email, password=user_password)
        
        if not user:
            try:
                my_user = user.objects.get(email=username_or_email)
                user = authenticate(username= my_user.username, password=user_password)
            except:
                user = None
        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        token,_ = Token.objects.get_or_create(user= user)
        request.session['auth_token'] = token.key
        return Response({"token": token.key}, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    permission_classes =[IsAuthenticated]

    def destroy(self, request):
        request.auth.delete()
        request.session.pop({'token': None})
        return Response({"message": 'logged out successfully'},template_name='login', status=status.HTTP_200_OK)
    

class ProfileViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = CustUserSerializer
    queryset = CustUser.objects.all()

    def get_queryset(self):
        user = self.request.user
        if not  user.IsAdminOrOwner:
            return CustUser.objects.all()
        return CustUser.objects.filter(id=user.id)
       
        
    
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        if self.request.user !=IsAdminOrOwner:
            raise PermissionDenied("you need to be the admin to perform the following action!")
        return super().destroy(request, *args, **kwargs)
    
class SalaryViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = SalarySerializer
    queryset = Salary.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.IsAdminOrOwner:
            return Salary.objects.all()
        return Salary.objects.filter(id=user.id)
    
    @action(methods=['Patch'], detail=True, permission_classes=[IsAdmin])
    def partial_update(self, serializer):
        return super().perform_update(serializer)

