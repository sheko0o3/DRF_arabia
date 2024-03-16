from django.shortcuts import render
from django.http.response import JsonResponse

from .models import Guest, Reservation, Movie, Post
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer, PostSerializer

from rest_framework.response import Response
from rest_framework import status, filters

# FBView
from rest_framework.decorators import api_view

# CBView
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import exceptions

# mixins, viewsets, generics  Views
from rest_framework import generics, mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend

# Authentication for View
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorOrReadOnly

# Create your views here.


# -------------- # FBV --> function based view # ----------------- #

# 1- without REST and no model query (static data)
def no_rest_no_model(request):
    guests = [
        {
            "id": 1,
            "name": "omar",
            "mobile": 54666,
        },
        {
            "id": 2,
            "name": "yassin",
            "mobile": 4646,
        },
    ]
    return JsonResponse(data=guests, safe=False)


# 2- model data default django without rest
def no_rest_from_model(request):
    queryset = Guest.objects.all()
    response = {
        "guests": list(queryset.values())
    }
    return JsonResponse(data=response)


#    list == GET ,
#    Create == POST,
#    pk query == GET
#    Update == PUT
#    Delete destroy == DELETE


# 3- Function based views
# 3.1 GET, POST
@api_view(http_method_names=["GET", "POST"])
def FBV_List(request):

    # GET
    if request.method == "GET":
        guests = Guest.objects.all()
        serializer = GuestSerializer(instance=guests, many=True)
        return Response(serializer.data)
    # POST
    elif request.method == "POST":
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 3.2 (GET, PUT, DELETE) --> pk
@api_view(http_method_names=["GET", "PUT", "DELETE"])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except :
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = GuestSerializer(instance=guest)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = GuestSerializer(instance=guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ----------------- CBV Class Based View --------------- #

# 4.1 List and Create == GET , POST
class CBV_List(APIView):

    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(instance=guests, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 4.2  GET, PUT, DELETE
class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk=pk)
        serializer = GuestSerializer(instance=guest)
        return Response(data=serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk=pk)
        serializer = GuestSerializer(instance=guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk=pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# 5 Mixins views
# 5.1 mixins list
class mixins_list(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request=request)

    def post(self, request):
        return self.create(request=request)


# 5.2 mixins GET PUT DELETE
class mixins_pk(mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                generics.GenericAPIView):

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request=request, pk=pk)

    def put(self, request, pk):
        return self.update(request=request, pk=pk)

    def delete(self, request, pk):
        return self.destroy(request=request, pk=pk)


# Generics
# 6.1 GET, POST
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    # authentication_classes = [BasicAuthentication]
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


# 6.2 GET, PUT, DELETE
class generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


# 7 ViewSets
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["movie"]


class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

# ------------------------------------------------------------ #


# Find movie FBV
@api_view(http_method_names=["GET"])
def FindMovie(request):
    movies = Movie.objects.filter(
        movie=request.data["movie"]
    )
    serializer = MovieSerializer(instance=movies, many=True)
    return Response(data=serializer.data)


# create new reservation
@api_view(http_method_names=["POST"])
def NewReservation(request):

    movie = Movie.objects.get(
        movie=request.data["movie"],
        hall=request.data["hall"]
    )

    guest = Guest()
    guest.name = request.data["name"]
    guest.mobile = request.data["mobile"]
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    return Response(data=request.data, status=status.HTTP_201_CREATED)


# POST author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
