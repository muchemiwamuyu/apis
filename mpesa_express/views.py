from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import base64
from decouple import config
import requests
import datetime
# Create your views here.

def index(request):
   return HttpResponse('Hello from mpesa endpoint')
   

def get_mpesa_access_token(request):
 if request.method == 'POST':
    # Get the credentials from environment variables
    consumer_key = config('MPESA_CONSUMER_KEY')
    consumer_secret = config('MPESA_CONSUMER_PASSWORD')
    api_url = config('MPESA_EXPRESS_AUTH_ENDPOINT')

    # Encode the credentials
    api_credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(api_credentials.encode()).decode()

    # Set the headers
    headers = {
    'Authorization': f'Basic {encoded_credentials}',
    'Content-Type': 'application/json',
    }

    # Make the request to get the access token
    response = requests.post(f"{api_url}", headers=headers)

    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        return None

def get_password():
   timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
   shortcode = config('MPESA_SHORTCODE')
   passkey = config('MPESA_PASSKEY')

   password_str =  f'{shortcode}{passkey}{timestamp}'

   password_bytes = password_str.encode()

   return base64.b64encode(password_bytes).decode('utf-8')



@api_view(['POST'])
def stk_push(request):
 if request.method == 'POST':
    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

    access_token = get_mpesa_access_token()
    if not access_token:
        return Response({"error": "Failed to get access token"}, status=status.HTTP_400_BAD_REQUEST)

    api_url = config('MPESA_EXPRESS_SIMULATE_ENDPOINT')

    headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
    }

    payload = {
    "BusinessShortCode": config('MPESA_BIS_SHORTCODE'),
    "Password": get_password(),
    "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"),
    "TransactionType": "CustomerPayBillOnline",
    "Amount": serializer.validated_data['amount'],
    "PartyA": serializer.validated_data['phone_number'],
    "PartyB": config('MPESA_BIS_SHORTCODE'),
    "PhoneNumber": serializer.validated_data['phone_number'],
    "CallBackURL": config('MPESA_CALLBACK_URL'),
    "AccountReference": "Test123",
    "TransactionDesc": "Payment for testing"
    }

    response = requests.post(api_url, json=payload, headers=headers)

 if response.status_code == 200:
    return Response(serializer.data, status=status.HTTP_201_CREATED)
 else:
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   