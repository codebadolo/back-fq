from rest_framework import serializers
from .models import Document, Quiz, Question, Reponse

class ReponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reponse
        fields = ['id', 'texte', 'est_correcte']

class QuestionSerializer(serializers.ModelSerializer):
    reponses = ReponseSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'texte', 'reponses']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ['id', 'titre', 'ordre', 'questions']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'nom', 'fichier', 'date_import']

# serializers.py

from rest_framework import serializers
from .models import Document

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['fichier']  # seul champ uploadé par le client
