from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# viewset
router = DefaultRouter()
router.register(prefix="guests", viewset=views.viewsets_guest)
router.register(prefix="movies", viewset=views.viewsets_movie)
router.register(prefix="reservations", viewset=views.viewsets_reservation)


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

    # 5 mixins CBV
    path("mixins/", views.mixins_list.as_view()),

    path("mixins/<int:pk>", views.mixins_pk.as_view()),

    # 6 generics CBV
    path("generics/", views.generics_list.as_view()),
    path("generics/<int:pk>", views.generics_pk.as_view()),

    # 7: viewsets
    path("viewsets/", include(router.urls)),

    # ---------------------------- #
    # FBV
    path("findmovie/", views.FindMovie),

    path("newreserve/", views.NewReservation)

]