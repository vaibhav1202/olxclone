from django.urls import path
from django.urls.conf import include
from clone import views
from django.conf.urls import url
from django.views.generic.base import RedirectView
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework import routers

router = routers.DefaultRouter() 
router.register(r'item', views.ItemViewSet)

urlpatterns = [ 
    path('home/', views.about),
    path('about/', views.about),   
    path('contact/', views.contact),  
    path('notallow/', views.notallow), 
    path('item/', views.ItemList.as_view()),     
    path('item/create/', views.ItemCreate.as_view()), 
    url('item/(?P<pk>[0-9]+)$', views.ItemDetails.as_view()), 
    url('item/edit/(?P<pk>[0-9]+)$', views.ItemUpdate.as_view()), 
    url('item/delete/(?P<pk>[0-9]+)$', views.ItemDelete.as_view()), 
    url('item/buy/(?P<pk>[0-9]+)$', views.ItemBuy.as_view()), 
    url(r'^api/', include(router.urls)),
    url(r'^api-token-auth/', obtain_jwt_token),        
    url('^$', RedirectView.as_view(url="home/"))        
]
