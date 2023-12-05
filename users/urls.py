from django.urls import path
from . import views

urlpatterns = [
    path('',views.login_view,name='login'),
    path('logout', views.sign_out,name='logout'),
    path('register/', views.sign_up ,name='register'),
    path('dashboard/', views.dashview, name='dashboard'),
    # path('dashboard/create_set/<str:username>/create_card', views.create_flashcard, name='create_card'),
    path('create_set/', views.createSet, name='createSet'),
    path('edit_set/<int:id>/', views.editSet, name='edit_set'),
    path('delete_set/<int:id>/',views.deleteSet,name='delete_set'),
    path('view_set/<str:title>/<int:id>', views.viewSet, name='viewSet'),
    path('delete_card/<str:title>/<int:set_id>/<int:flashcard_id>',views.delete_flashcard,name='delete_card'),
    path('edit_card/<int:set_id>/<int:flashcard_id>',views.edit_flashcard,name='edit_card'),
    path('create_card/<str:title>/<int:id>/create_flashcard', views.create_flashcard, name='createCard'),
    path('practice_set/<int:setID>',views.practice_set,name='practice_set'),
    path('premiumupgrade/<int:user_id>',views.premium_upgrade,name='premiumupgrade'),
    path('setPremium/<int:user_id>',views.setPremium,name='setPremium'),
    path('about/',views.about_us, name="about_us"),
    path('import',views.import_set,name='importSet'),
    path('import/importSetKey/<str:shareKey>',views.import_setShareKey,name='importShareKey')
]

