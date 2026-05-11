from rest_framework import serializers
from .models import Case, Document, Hearing, Party

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'

class HearingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hearing
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class CaseSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    hearings = HearingSerializer(many=True, read_only=True)
    party_set = PartySerializer(many=True, read_only=True)

    class Meta:
        model = Case
        fields = '__all__'