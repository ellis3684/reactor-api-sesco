from rest_framework import serializers
from reactors.models import Reactor, StatusEntry


class ReactorSerializer(serializers.ModelSerializer):
    # Show model properties
    license_length = serializers.ReadOnlyField()
    current_reactor_age = serializers.ReadOnlyField()
    time_remaining = serializers.ReadOnlyField()

    class Meta:
        model = Reactor
        exclude = ('id',)  # This ID PK is meaningless to the user since lookup by docket num and name is supported


class StatusEntrySerializer(serializers.ModelSerializer):
    # Show fields in Reactor instead of PK
    reactor_short_name = serializers.CharField(source='reactor.short_name')
    docket_number = serializers.CharField(source='reactor.docket_number')

    class Meta:
        model = StatusEntry
        exclude = ('id', 'reactor')  # These ID PKs are meaningless to the user since lookup by docket num is supported
