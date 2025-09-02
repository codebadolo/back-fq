from rest_framework import serializers
from .models import Document, Quiz, Question, Reponse
from rest_framework import serializers
from rest_framework import serializers
from .models import Question, Reponse
from django.contrib.auth import get_user_model
from .models import Quiz, Question, Reponse

from rest_framework import serializers
from .models import Document

User = get_user_model()
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nom']



class ReponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reponse
        fields = ['id', 'texte', 'est_correcte']


class QuestionSerializer(serializers.ModelSerializer):
    reponses = ReponseSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'texte', 'reponses']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'titre', 'ordre', 'questions', 'created_at', 'updated_at']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'nom', 'fichier', 'date_import']

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['fichier']  # seul champ uploadé par le client
