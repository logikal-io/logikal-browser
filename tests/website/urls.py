from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('downloads/', TemplateView.as_view(template_name='downloads.html'), name='downloads'),
    path('accounts/login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('video/', TemplateView.as_view(template_name='video.html'), name='video'),
    path('slideshow/', TemplateView.as_view(template_name='slideshow.html'), name='slideshow'),
    re_path(
        '^internal/',
        login_required(TemplateView.as_view(template_name='internal.html')),
        name='internal',
    ),
]
