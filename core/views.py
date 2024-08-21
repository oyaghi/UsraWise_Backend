from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import  IsAuthenticated, AllowAny
from rest_framework import status
from .serializer import CustomUserSerializer, LoginSerializer
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


from django.core.mail import send_mail
from django.conf import settings
from .tokens import EmailVerificationTokenGenerator, PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode  # For encoding the user ID
from django.utils.encoding import force_bytes  # For ensuring consistent byte representation
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode




#Register API
@api_view(['POST'])
@permission_classes([AllowAny]) 
@csrf_exempt
def register(request):
    if request.method == 'POST':
        
        
            seri = CustomUserSerializer(data=request.data)
        
            if seri.is_valid():
                
                user=seri.save() #Error/ Object
                if 'Error Message'in user: 
                    return Response({"Message":user }, status=status.HTTP_200_OK)
                
                else:
                    message = EmailVerification(request,user)
                    return Response({"Message":message}, status=status.HTTP_200_OK)

            else:
                return Response({"Message": "Error in validating data"}, status= status.HTTP_400_BAD_REQUEST)
        


#Login API
