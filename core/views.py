from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import  IsAuthenticated, AllowAny
from rest_framework import status
from .serializer import CustomUserSerializer, LoginSerializer, ChildSerializer
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



# Email verification message
def EmailVerification(request,user):
    try:
        # Creating Verification Email
        print(user)
        user             = CustomUser.objects.get(email=user['email'].lower())
        
        token_generator  = EmailVerificationTokenGenerator()
        token            = token_generator.make_token(user)
        uidb64           = urlsafe_base64_encode(force_bytes(user.pk))
        current_site     = get_current_site(request)
        verification_url = f"https://{current_site.domain}/core/activate/{uidb64}/{token}/"
        
        # Sending the email 
        subject         = 'Email verification'
        message         = f'Hi {user.name}\nPlease Verify Your Email\n{verification_url}'
        email_from      = settings.EMAIL_HOST_USER
        recipient_list  = [user.email.lower(),]
        send_mail(subject, message,email_from,recipient_list)
        return "Email has been sent successfully"
    except Exception as e:
        return str(e)
    


# Email Activation
def activate_Email(request, uidb64, token):  
    
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = CustomUser.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and EmailVerificationTokenGenerator().check_token(user, token):  
        user.is_active = True  
        user.save()  
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!') 



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
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def Login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email'].lower()
        password = serializer.validated_data['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_active:
            parent = CustomUser.objects.get(email=email.lower())
            parent_id = parent.id            
            try:
                refresh = RefreshToken.for_user(user)

                # Customize the payload with user information
                refresh['email'] = email.lower()
                refresh['role']  = "parent"       # Add other necessary user information to the payload
                refresh['iss']   = 'OYaghi'
                refresh['id']    = parent_id
                
                
                token = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response({"Message":"parent Login Successfuly","Token":token}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"Message": "Error at generating token"}, status= status.HTTP_400_BAD_REQUEST)
        else:
            # User authentication failed or not a parent
            return Response({"Message": "Invalid email or password"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"Message": "Enter correct email and password"}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def child_register(request):
    if request.method == 'POST':
        serializer = ChildSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)