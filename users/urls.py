from django.urls import path

from users.views import *


urlpatterns = [
    path('get_annoucement_notification/<str:user_id>/', get_annoucement_notification, name='get_annoucement_notification'),
    path('set_notification_read/<str:notification_id>/', set_notification_read, name='set_notification_read'),
    path('set_Annoucment_read/<str:announcement_id>/<str:user_id>/', set_Annoucment_read, name='set_Annoucment_read'),
    path('answer_predict/<str:notificationId>/<str:answer>/', answer_predict, name='answer_predict'),

]
