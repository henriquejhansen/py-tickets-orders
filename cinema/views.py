@"
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from cinema.models import Genre, Actor, CinemaHall, Movie, MovieSession, Order
from cinema.serializers import (
    GenreSerializer,
    ActorSerializer,
    CinemaHallSerializer,
    MovieSerializer,
    MovieSessionSerializer,
    MovieSessionListSerializer,
    MovieDetailSerializer,
    MovieSessionDetailSerializer,
    MovieListSerializer,
    OrderSerializer,
)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class CinemaHallViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action == "list":
            return MovieListSerializer
        if self.action == "retrieve":
            return MovieDetailSerializer
        return MovieSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        title = self.request.query_params.get('title')
        genres = self.request.query_params.get('genres')
        actors = self.request.query_params.get('actors')
        
        if title:
            queryset = queryset.filter(title__icontains=title)
        if genres:
            genre_list = [genre.strip() for genre in genres.split(',')]
            queryset = queryset.filter(genres__name__in=genre_list).distinct()
        if actors:
            actor_list = [actor.strip() for actor in actors.split(',')]
            queryset = queryset.filter(
                Q(actors__first_name__in=actor_list) |
                Q(actors__last_name__in=actor_list)
            ).distinct()
        
        return queryset


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.all()
    serializer_class = MovieSessionSerializer
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action == "list":
            return MovieSessionListSerializer
        if self.action == "retrieve":
            return MovieSessionDetailSerializer
        return MovieSessionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        date = self.request.query_params.get('date')
        movie = self.request.query_params.get('movie')
        
        if date:
            queryset = queryset.filter(show_time__date=date)
        if movie:
            queryset = queryset.filter(movie_id=movie)
        
        return queryset


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'tickets__movie_session__movie',
            'tickets__movie_session__cinema_hall'
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
"@ | Out-File -FilePath cinema/views.py -Encoding UTF8
