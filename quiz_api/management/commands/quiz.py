import json
import os

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model
from quiz_api.models import Document, Quiz, Question, Reponse


User = get_user_model()


class Command(BaseCommand):
    help = 'Crée des quiz complets à partir d\'un fichier JSON'

    def handle(self, *args, **kwargs):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, 'quizzes_data.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"Fichier {json_path} introuvable."))
            return

        with open(json_path, 'r', encoding='utf-8') as f:
            quizzes_data = json.load(f)

        user = User.objects.first()
        if not user:
            self.stdout.write(self.style.ERROR("Aucun utilisateur trouvé pour attribuer la création."))
            return

        for quiz_data in quizzes_data:
            document, _ = Document.objects.get_or_create(nom=quiz_data.get('document_nom', 'Document par défaut'))

            quiz = Quiz.objects.create(
                document=document,
                titre=quiz_data['titre'],
                ordre=quiz_data.get('ordre', 1),
                created_by=user,
                updated_by=user,
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            self.stdout.write(self.style.SUCCESS(f"Quiz créé : {quiz.titre}"))

            for question_data in quiz_data.get('questions', []):
                question = Question.objects.create(
                    quiz=quiz,
                    texte=question_data['texte']
                )
                self.stdout.write(self.style.SUCCESS(f"  Question créée : {question.texte}"))

                for reponse_data in question_data.get('reponses', []):
                    reponse = Reponse.objects.create(
                        question=question,
                        texte=reponse_data['texte'],
                        est_correcte=reponse_data['est_correcte']
                    )
                    self.stdout.write(self.style.SUCCESS(f"    Réponse créée : {reponse.texte} (Correcte: {reponse.est_correcte})"))

        self.stdout.write(self.style.SUCCESS("Import JSON terminé avec succès."))
