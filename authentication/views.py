from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import re
import bcrypt
import datetime
import jwt

from vid_upld.models import Video_Upld

from .models import User
from stream.settings import JWT_SECRET
# Create your views here.

class Signup(View):
    template_name = 'auth/signup.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects(__raw__ = {"$or": [
            {"name":username},
            {"email" : email}
        ]}).first() :
            messages.error(request, 'The User exists')
            return redirect('Signup')
        
        elif not (len(password) >= 8 and all(map(lambda pattern: re.search(pattern,password), [r'[a-z]', r'[A-Z]', r'\d']))):
            messages.error(request, 'Invalid Password. It must be of : atleast 8 characters, include a uppercase, lowercase and a digit')
            return redirect('Signup')
        
        else:
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user = User(name = username, email=email, password=hashed_pw.decode('utf-8'))
            user.save()
            messages.success(request,'User Created Successfully')
            return redirect('Login')
            
class Login(View):
    template_name = 'auth/login.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
    
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        
        user = User.objects(__raw__ = {'$or': [
            {'name' : user_id},
            {'email' : user_id}
        ]}).first()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            messages.success(request, 'Signed In')
            payload = {
                "user_id": str(user.id),
                "email": user.email,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(payload,JWT_SECRET,algorithm='HS256')
            return JsonResponse({"token" : token})    
        else: 
            return JsonResponse({"error": "Invalid credentials"}, status=401)
        
class Profile(View):
    template_name = 'auth/profile.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
class Profile_Details(View):
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not (auth_header or auth_header.startswith('Bearer')):
            return JsonResponse({'error' : 'Unauthorized Access'}, status = 401)
        
        auth_token = auth_header.split(" ")[1]
        
        try:
            token = jwt.decode(auth_token, JWT_SECRET, algorithms='HS256')  
            user = User.objects.get(id = token['user_id'])
            videos = Video_Upld.objects.filter(uploaded_by=user).order_by('-uploaded_at')
            
            video_data = [
                {
                    "title" : vid.title,
                    "video_url" : vid.video_url,
                    "description" : vid.description,
                    "uploaded_at" : vid.uploaded_at.isoformat()
                }
                for vid in videos]
            
            return JsonResponse({
                'user': {
                    'name': user.name,
                    'email': user.email,
                    'password' : user.password,
                },
                'videos': video_data})
                    
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error' : 'Login Again'}, status = 401)
        
        except jwt.InvalidTokenError:
            return JsonResponse({'error' : 'Login Again'}, status = 401)
        
        

@method_decorator(csrf_exempt,name='dispatch')
class ApiLogin(View):
    template_name = 'auth/login.html'
    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
    
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        
        user = User.objects(__raw__ = {'$or': [
            {'name' : user_id},
            {'email' : user_id}
        ]}).first()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode):
            messages.success(request, 'Signed In')
            payload = {
                "user_id": str(user.id),
                "email": user.email,
                "exp": datetime.datetime.now() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(payload,JWT_SECRET,algorithm='HS256')
            return JsonResponse({"token" : token})  
        else: 
            return JsonResponse({"error": "Invalid credentials"}, status=401)           
            
            
            
        
        
            
        
        
        