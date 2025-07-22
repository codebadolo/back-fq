from django.db import models

class Document(models.Model):
    nom = models.CharField(max_length=255)
    fichier = models.FileField(upload_to='documents/')
    date_import = models.DateTimeField(auto_now_add=True)

class Quiz(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    ordre = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    texte = models.TextField()

class Reponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='reponses')
    texte = models.CharField(max_length=500)
    est_correcte = models.BooleanField(default=False)
