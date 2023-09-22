import datetime

from rest_framework import generics
from rest_framework.exceptions import ParseError, NotFound
from django.shortcuts import get_object_or_404

from reactors.models import Reactor, StatusEntry
from .serializers import ReactorSerializer, StatusEntrySerializer


class ListAllReactors(generics.ListAPIView):
    """List individual data for all reactors."""
    queryset = Reactor.objects.all()
    serializer_class = ReactorSerializer


class ListReactorsByState(generics.ListAPIView):
    """
    List individual data for all reactors within a specified state. The state parameter must be the state's two-letter
    abbreviation.
    """
    serializer_class = ReactorSerializer

    def get_queryset(self):
        return Reactor.objects.filter(state=self.kwargs.get('state').upper())


class ListOutagesByDate(generics.ListAPIView):
    """
    List the status entries for all reactors that had an outage on the specified date. The date parameter must be in
    'YYYY-MM-DD' format.
    """
    serializer_class = StatusEntrySerializer

    def get_queryset(self):
        try:
            date = datetime.datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date()
        except ValueError:
            raise ParseError(detail='Invalid date entered. Date must be in YYYY-MM-DD format.')
        return StatusEntry.objects.filter(date=date, power=0)


class DetailReactorByDocket(generics.RetrieveAPIView):
    """Get the individual reactor data for the reactor specified by the given docket number."""
    queryset = Reactor.objects.all()
    serializer_class = ReactorSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, docket_number=self.kwargs['docket_num'])
        return obj


class DetailLastOutageByDocket(generics.RetrieveAPIView):
    """
    Get the status entry for the most recent date that the specified reactor had an outage. The reactor is specified by
    the given docket number. The date parameter must be in 'YYYY-MM-DD' format.
    """
    queryset = StatusEntry.objects.all()
    serializer_class = StatusEntrySerializer

    def get_object(self):
        queryset = self.get_queryset()
        try:
            return queryset.filter(reactor__docket_number=self.kwargs['docket_num'], power=0).latest('date')
        except StatusEntry.DoesNotExist:
            raise NotFound()


class DetailLastOutageByName(generics.RetrieveAPIView):
    """
    Get the status entry for the most recent date that the specified reactor had an outage. The reactor is specified by
    the given short name, which is the name that can be found on the 'powerreactorstatusforlast365days.txt' document.
    The date parameter must be in 'YYYY-MM-DD' format.
    """
    queryset = StatusEntry.objects.all()
    serializer_class = StatusEntrySerializer

    def get_object(self):
        queryset = self.get_queryset()
        try:
            return queryset.filter(reactor__short_name=self.kwargs['short_name'], power=0).latest('date')
        except StatusEntry.DoesNotExist:
            raise NotFound()


class DetailStatusByDocketOnDate(generics.RetrieveAPIView):
    """
    Get the status entry for the specified reactor on the date provided. The reactor is specified by the given docket
    number. The date parameter must be in 'YYYY-MM-DD' format.
    """
    queryset = StatusEntry.objects.all()
    serializer_class = StatusEntrySerializer

    def get_object(self):
        try:
            date = datetime.datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date()
        except ValueError:
            raise ParseError(detail='Invalid date entered. Date must be in YYYY-MM-DD format.')

        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, reactor__docket_number=self.kwargs['docket_num'], date=date)
        return obj


class DetailStatusByNameOnDate(generics.RetrieveAPIView):
    """
    Get the status entry for the specified reactor on the date provided. The reactor is specified by the given short
    name, which is the name that can be found on the 'powerreactorstatusforlast365days.txt' document. The date
    parameter must be in 'YYYY-MM-DD' format.
    """
    queryset = StatusEntry.objects.all()
    serializer_class = StatusEntrySerializer

    def get_object(self):
        try:
            date = datetime.datetime.strptime(self.kwargs['date'], '%Y-%m-%d').date()
        except ValueError:
            raise ParseError(detail='Invalid date entered. Date must be in YYYY-MM-DD format.')

        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, reactor__short_name=self.kwargs['short_name'], date=date)
        return obj
