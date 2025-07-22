from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, DocumentUploadView
# Importez aussi vos autres ViewSets si besoin (QuizViewSet, QuestionViewSet, ReponseViewSet)
from .views import (
    DocumentViewSet,
    DocumentUploadView,
    QuizViewSet,
    QuestionViewSet,
    ReponseViewSet,dashboard_stats
)
router = DefaultRouter()
router.register(r'documents', DocumentViewSet)
# Si vous créez les ViewSets Quiz, Question, Reponse, ajoutez-les ici :

router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'reponses', ReponseViewSet)

urlpatterns = [
    # Endpoints CRUD automatiques pour documents
    path('', include(router.urls)),
path('dashboard_stats/', dashboard_stats, name='dashboard-stats'),
    # Endpoint upload document (POST)
    path('document/upload/', DocumentUploadView.as_view(), name='document-upload'),
]
