from django.urls import path
from . import views


urlpatterns = [
    path('',views.upload_file,name='home'),
    # path('success/',views.success)

]
