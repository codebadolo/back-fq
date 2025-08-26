from rest_framework import serializers
from .models import Document, Quiz, Question, Reponse
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Quiz, Question, Reponse
User = get_user_model()
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nom']
from rest_framework import serializers
from .models import Question, Reponse


class ReponseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # nécessaire pour update imbriqué

    class Meta:
        model = Reponse
        fields = ['id', 'texte', 'est_correcte']


class QuestionSerializer(serializers.ModelSerializer):
    reponses = ReponseSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'texte', 'reponses']

    # Validation : une seule réponse correcte
    def validate_reponses(self, value):
        correct_count = sum(1 for rep in value if rep.get('est_correcte', False))
        if correct_count != 1:
            raise serializers.ValidationError('Une seule réponse correcte par question est autorisée.')
        return value

    def update(self, instance, validated_data):
        reponses_data = validated_data.pop('reponses')
        instance.texte = validated_data.get('texte', instance.texte)
        instance.save()

        # Récupérer les réponses existantes
        reponses_mapping = {rep.id: rep for rep in instance.reponses.all()}
        reponses_ids = [item.get('id') for item in reponses_data if item.get('id')]

        # Supprimer les réponses absentes
        for rep_id in reponses_mapping:
            if rep_id not in reponses_ids:
                reponses_mapping[rep_id].delete()

        # Mettre à jour ou créer les réponses
        for rep_data in reponses_data:
            rep_id = rep_data.get('id', None)
            if rep_id:
                reponse = reponses_mapping.get(rep_id, None)
                if reponse:
                    reponse.texte = rep_data.get('texte', reponse.texte)
                    reponse.est_correcte = rep_data.get('est_correcte', reponse.est_correcte)
                    reponse.save()
            else:
                Reponse.objects.create(question=instance, **rep_data)

        return instance


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    created_by = UserSimpleSerializer(read_only=True)
    updated_by = UserSimpleSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)

    class Meta:
        model = Quiz
        fields = [
            'id', 'titre', 'ordre', 'questions',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]

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
