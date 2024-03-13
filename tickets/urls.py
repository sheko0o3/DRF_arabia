from django.urls import path
from . import views

urlpatterns = [
    # 1:
    path("jsonresponsenomodel/", views.no_rest_no_model),

    # 2:
    path("jasonresponsefrommodel/", views.no_rest_from_model),

    # 3.1: GET POST from rest framework FBV @api_view decorator
    path("restfbv/", views.FBV_List),

    # 3.2: GET PUT DELETE from rest_framework FBV @api_view decorator
    path("restfbv/<int:pk>", views.FBV_pk),

    # 4.1: GET POST from rest_framework CBV APIView (inheritance)
    path("restcbv/", views.CBV_List.as_view()),

    path("restcbv/<int:pk>", views.CBV_pk.as_view()),

    # 5 mixins
    path("mixins/", views.mixins_list.as_view()),

    path("mixins/<int:pk>", views.mixins_pk.as_view()),

    # 6 generics
    path("generics/", views.generics_list.as_view()),
    path("generics/<int:pk>", views.generics_pk.as_view()),

]