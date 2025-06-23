from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse

from stream.cloudinary_confg import cloudinary

import cloudinary.uploader
import jwt
import datetime

from .models import Video_Upld
from authentication.models import User
from stream.settings import JWT_SECRET
# Create your views here.

class Video_Uploading(View):
    template_name = 'video_upload/video_upload.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        
        user = get_user_frm_request(request)
        if not user:
            return JsonResponse({"error" : "Unauthorized Access"}, status = 401)
        
        title = request.POST.get('title')
        description = request.POST.get('description')
        video = request.FILES.get('video')
        
        if not title or not description:
            return JsonResponse({"error": "Title and Description are required"}, status=400)

        
        if not video:
            return JsonResponse({"error" : "No file uploaded"}, status = 400)
        if not video.name.endswith('.mp4'):
            return JsonResponse({"error" : "Only .mp4 files allowed"}, status = 400)
        else:
            vid_upld_rslt = cloudinary.uploader.upload_large( video, resource_type = 'video', folder = "strmly_videos")
        
        try:
            Video_Upld(title=title,
                    description = description,
                    video_url = vid_upld_rslt['secure_url'],
                    uploaded_by = user,
                    uploaded_at = datetime.datetime.now()
                    ).save()
            return JsonResponse({'success' : True, 'message' : 'Video Uploaded'})
        except Exception:
            return JsonResponse({'error': 'Error encountered. Please try again.'}, status=500)
        
class Video_Streaming(View):
    template_name = 'video_upload/video_feed.html'
    def get(self, request, *args, **kwargs):
        
        videos = Video_Upld.objects.order_by('-uploadedat')
        
        context = {
            'videos' : videos
        }
        
        return render(request, self.template_name, context)
            
        
def get_user_frm_request(request):
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer"):
        return None
    
    auth_token = auth_header.split(" ")[1]
    try:
        decode = jwt.decode(auth_token,JWT_SECRET, algorithms='HS256')
        user_id = decode['user_id']
        user = User.objects.get(id=user_id)
        return user
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None