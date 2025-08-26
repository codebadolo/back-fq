from django.contrib import admin
from .models import Document, Quiz, Question, Reponse

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('nom', 'date_import')
    search_fields = ('nom',)
    readonly_fields = ('date_import',)

class ReponseInline(admin.TabularInline):
    model = Reponse
    extra = 1
    fields = ('texte', 'est_correcte')

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('texte',)
    inlines = [ReponseInline]  # Inline imbriqué possible via admin.StackedInline si complexe

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('titre', 'ordre', 'document', 'created_at')
    list_filter = ('document',)
    search_fields = ('titre',)
    ordering = ('ordre',)
    inlines = [QuestionInline]  # Intègre questions dans la fiche quiz

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('texte', 'quiz')
    list_filter = ('quiz',)
    search_fields = ('texte',)
    inlines = [ReponseInline]  # Réponses dans la fiche question

@admin.register(Reponse)
class ReponseAdmin(admin.ModelAdmin):
    list_display = ('texte', 'question', 'est_correcte')
    list_filter = ('est_correcte',)
    search_fields = ('texte',)
