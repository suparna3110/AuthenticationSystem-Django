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

# for checking email using regular expression
regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
# checking email, if in right format or not

def check(email):

    # pass the regualar expression
    # and the string in search() method
    if(re.search(regex, email)):
        return True
    else:
        return False

# class for sign up. New user will register or make an account. 
# user will enter all details and then verification of all fields weather filled or not.
# Password is stored at backend in encrypted form using one way Bcrypt technique.
class Signup(APIView):
    # def get(self, request):
        # userid = request.GET.get('userid')
        # details = Persons.objects.filter(userid=userid).first()
        # user = {'fname': details.fname, 'lname': details.lname}
        # print(user)
        # return Response(user, status.HTTP_200_OK)

    def post(self, request):
        fname = request.data.get('first name')
        lname = request.data.get('last name')
        email = request.data.get('email')
        password = request.data.get('password')
        dob = request.data.get('dob')
        check1 = check(email)
        details = Persons.objects.filter(email=email).first()
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

# user is signing up to his account and then verification of email 
# and its corresponding password is being checked at backend from the database for signingin.
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
    

# showing details of the user after successful sign in from the database.
# On entering their userid (received during Sign-in), they can get their details.
    
class Showdetails(APIView):
    def get(self, request):
        userid = request.GET.get('userid')
        if not userid:
            return Response({"Message": "Please fill the empty field"},status.HTTP_400_BAD_REQUEST)
        else:
            details = Persons.objects.filter(userid=userid).first()
            if not details:
                return Response({"Message": "User doesn't exist"}, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'fname': details.fname, 'lname': details.lname,'dob':details.dob}, status.HTTP_200_OK)
      


class Update(APIView):
    def post(self, request):
        # This function is to execute updation of user details using the id they are given after Sign-in
        # The user-id is compulsorily accepted for retrieving that particular user's details.
        # The updated values are accepted for updation in the database.
        
        userid = request.data.get('userid')
        fname = request.data.get('fname')
        lname = request.data.get('lname')
        dob = request.data.get('dob')
        password = request.data.get('password')
        if not userid:
            return Response({"Message": "Please enter the user id you were given"}, status.HTTP_400_BAD_REQUEST)
        else:
            details = Persons.objects.filter(userid=userid).first()
            if not details:
                return Response({"Message": "User doesn't exist / You can't update your user id"}, status.HTTP_400_BAD_REQUEST)
            else:
                if not fname and not lname and not dob and not password:
                    return Response({"Message": "Please fill the field you want to update"}, status.HTTP_400_BAD_REQUEST)
                else:
                    if fname:
                        details.fname = fname
                    if lname:
                        details.lname = lname
                    if dob:
                        details.dob = dob
                    if password:
                        details.password = password
                    details.save()
                    return Response({"Message": "User details updated successfully!"}, status.HTTP_200_OK)

