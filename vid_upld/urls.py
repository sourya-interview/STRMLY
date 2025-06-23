from django.urls import path

from authentication.views import Signup,Login,ApiLogin,Profile, Profile_Details #Auth

from .views import Video_Uploading, Video_Streaming

urlpatterns = [
    path('signup/', Signup.as_view(), name='Signup'), #Auth --- Signup
    path('login/', Login.as_view(), name='Login'), # Auth --- Web Browser Login
    path('api_login/',ApiLogin.as_view(),name='Api_Login'), # Auth --- Api Login
    path('profile/', Profile.as_view(), name = "Profile"), #Auth -- Profile Loads
    path('profile/details', Profile_Details.as_view(), name = "Details"), #Auth -- Profile Details
    
    path('upload/', Video_Uploading.as_view(), name='VidUpload'), #Upload Video
    path('videos/', Video_Streaming.as_view(), name='Stream') #Stream Videos
]