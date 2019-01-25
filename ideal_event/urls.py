<<<<<<< HEAD
from django.conf.urls import url
from django.urls import path
from ideal_event import views
# SET THE NAMESPACE!
app_name = 'ideal_event'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^select_interest/$', views.select_interests, name='select_interest'),
    # path('/process/', views.process, name='process'),
    # url('/process/', views.process, name='process'),

]
=======
from django.conf.urls import url
from django.urls import path
from ideal_event import views
# SET THE NAMESPACE!
app_name = 'ideal_event'
# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^user_login/$', views.user_login, name='user_login'),
    url(r'^select_interest/$', views.select_interests, name='select_interest'),
    # path('/process/', views.process, name='process'),
    # url('/process/', views.process, name='process'),
]
>>>>>>> 359dc539132ae69e53444a44f86b4acbccec2aa1
