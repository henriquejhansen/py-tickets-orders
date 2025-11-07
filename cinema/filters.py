import django_filters
from .models import Movie, MovieSession


class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    genres = django_filters.ModelMultipleChoiceFilter(
        field_name="genres", queryset=Movie.objects.none()
    )
    actors = django_filters.ModelMultipleChoiceFilter(
        field_name="actors", queryset=Movie.objects.none()
    )

    class Meta:
        model = Movie
        fields = ["title", "genres", "actors"]


class MovieSessionFilter(django_filters.FilterSet):
    movie = django_filters.NumberFilter(field_name="movie_id")
    show_time = django_filters.DateFilter(field_name="show_time", lookup_expr="date")

    class Meta:
        model = MovieSession
        fields = ["movie", "show_time"]
