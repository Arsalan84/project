from django.urls import path
from .views import (
    event_list, event_detail, event_create, participant_register,
    task_create, send_task_list, user_register, user_login, user_logout,
    participant_list, task_update 
)

urlpatterns = [
    path('', event_list, name='event_list'),
    path('<int:event_id>/', event_detail, name='event_detail'),
    path('create/', event_create, name='event_create'),
    path('<int:event_id>/register/', participant_register, name='participant_register'),
    path('<int:event_id>/tasks/create/', task_create, name='task_create'),
    path('<int:event_id>/tasks/send/', send_task_list, name='send_task_list'),
    path('<int:event_id>/participants/', participant_list, name='participant_list'),
    path('tasks/<int:task_id>/update/', task_update, name='task_update'),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]
