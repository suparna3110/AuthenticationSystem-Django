from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.views import status
from rest_framework.response import Response
from blog.models import Persons
import re
from django.contrib.auth.hashers import check_password, make_password
# Create your views here.


def home(request):
    content = "<h1>Home</h1>"
    return HttpResponse(content)


regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def check(email):

    # pass the regualar expression
    # and the string in search() method
    if(re.search(regex, email)):
        return True
    else:
        return False


class Signup(APIView):
    def get(self, request):
        userid = request.GET.get('userid')
        details = Persons.objects.filter(userid=userid).first()
        user = {'fname': details.fname, 'lname': details.lname}
        print(user)
        return Response(user, status.HTTP_200_OK)

    def post(self, request):
        fname = request.data.get('first name', 'suparna')
        lname = request.data.get('last name')
        email = request.data.get('email')
        password = request.data.get('password')
        dob = request.data.get('dob')
        check1 = check(email)
        details=Persons.objects.filter(email=email).first()
        if details:
            return Response({"message": "User already exist"}, status=status.HTTP_400_BAD_REQUEST)

        if not fname or not lname or not password or not dob or not email:
            return Response({"message": "Please fill required fields"}, status=status.HTTP_400_BAD_REQUEST)
        elif not check1:
            return Response({"message": "Bad email"}, status=status.HTTP_400_BAD_REQUEST)
        password_hash = make_password(password)
        # print( fname,lname,email,password,dob)
        Persons.objects.create(fname=fname, lname=lname,
                               email=email, password=password_hash, dob=dob)

        # print(x.userid,x.fname)
        return Response({"result": "successful signup"}, status.HTTP_200_OK)


class Signin(APIView):
    def post(self, request):
      email = request.POST.get('email')
      password = request.POST.get('password')
      details = Persons.objects.filter(email=email, flag=1).first()
      if details:
         if not email or not password:
            return Response({'message': 'Missing email/password'}, status=status.HTTP_400_BAD_REQUEST)
         if check_password(password, details.password):
            return Response({'message': 'Signin succesful'}, status=status.HTTP_200_OK)
         else:
            return Response({'message': 'Invalid email/password'}, status=status.HTTP_400_BAD_REQUEST)
      else:
            return Response({'message': "User doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
      
