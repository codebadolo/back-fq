from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Document, Quiz, Question, Reponse
from .serializers import DocumentSerializer, QuizSerializer, QuestionSerializer, ReponseSerializer

from rest_framework import viewsets
from .models import Document, Quiz, Question, Reponse
from .serializers import DocumentSerializer, QuizSerializer, QuestionSerializer, ReponseSerializer

from django.db.models import Count
from django.utils.timezone import now, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Quiz, Question, Document

@api_view(['GET'])
def dashboard_stats(request):
    total_quizzes = Quiz.objects.count()
    total_questions = Question.objects.count()
    total_documents = Document.objects.count()
    #total_users = User.objects.count()

    # Période : 7 derniers jours
    today = now().date()
    last_week = today - timedelta(days=6)
    date_range = [last_week + timedelta(days=i) for i in range(7)]

    # Stat: nombre de quiz créés chaque jour (courbe d'activité sur 7 jours)
    daily_counts = (
        Quiz.objects.filter(created_at__date__gte=last_week)
        .values('created_at__date')
        .annotate(count=Count('id'))
        .order_by('created_at__date')
    )
    histo = {entry['created_at__date']: entry['count'] for entry in daily_counts}
    quizzes_per_day = [{"date": d.strftime("%Y-%m-%d"), "quizzes": histo.get(d, 0)} for d in date_range]

    return Response({
        "total_quizzes": total_quizzes,
        "total_questions": total_questions,
        "total_documents": total_documents,
    #    "total_users": total_users,
        "quizzes_per_day": quizzes_per_day,
    })


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ReponseViewSet(viewsets.ModelViewSet):
    queryset = Reponse.objects.all()
    serializer_class = ReponseSerializer

# Vous pourrez créer aussi QuizViewSet, QuestionViewSet, ReponseViewSet selon besoins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from .models import Document, Quiz, Question, Reponse
import pdfplumber  # à installer via pip install pdfplumber
# views.py

# views.py
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import DocumentUploadSerializer
from .models import Document, Quiz, Question, Reponse
import pdfplumber
import re

class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]  # pour gérer correctement multipart/form-data

    def post(self, request, *args, **kwargs):
        # serializer qui accepte uniquement le fichier
        serializer = DocumentUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Sauvegarde fichier dans Document
        document = serializer.save(nom=serializer.validated_data['fichier'].name)

        # Extraction questions depuis PDF
        questions_data = self.extract_questions_from_pdf(document.fichier.path)

        # Découpage en quiz max 60 questions par quiz
        max_questions = 60
        total_questions = len(questions_data)
        nb_quizzes = (total_questions + max_questions - 1) // max_questions

        for i in range(nb_quizzes):
            start = i * max_questions
            end = start + max_questions
            quiz_questions = questions_data[start:end]

            quiz = Quiz.objects.create(document=document,
                                       titre=f"Quiz {i + 1} - {document.nom}",
                                       ordre=i+1)

            for q in quiz_questions:
                question = Question.objects.create(quiz=quiz, texte=q['question'])
                for rep in q['responses']:
                    Reponse.objects.create(question=question, texte=rep, est_correcte=False)

        return Response(
            {'message': f'{total_questions} questions extraites en {nb_quizzes} quiz depuis {document.nom}.'},
            status=status.HTTP_201_CREATED
        )

    def extract_questions_from_pdf(self, path):
        questions = []
        with pdfplumber.open(path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        # Regex simplifiée à adapter selon vos PDF
        pattern = re.compile(r'(\d+)\)\s*(.+?)\n([a-d]\).+?\n(?:[a-d]\).+?\n)+)', re.DOTALL)
        matches = pattern.findall(text)

        for _, question_text, answers_block in matches:
            responses = re.findall(r'[a-d]\)\s*(.+)', answers_block)
            questions.append({
                'question': question_text.strip(),
                'responses': [r.strip() for r in responses]
            })
        return questions
