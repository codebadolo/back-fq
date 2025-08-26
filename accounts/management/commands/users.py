import random
from django.core.management.base import BaseCommand
from accounts.models import CustomUser

class Command(BaseCommand):
    help = "Crée 20 utilisateurs CustomUser avec emails basés sur nom et prénom."

    def handle(self, *args, **kwargs):
        noms = ['Badolo', 'Ouedraogo', 'Nacoulma', 'Diallo', 'Kiendrebeogo', 'Traore']
        prenoms_chretiens = ['Jean', 'Paul', 'Marie', 'Jacques', 'Sophie', 'Pierre']
        prenoms_musulmans = ['Ahmed', 'Omar', 'Fatima', 'Youssef', 'Amina', 'Mamadou']
        prenoms = prenoms_chretiens + prenoms_musulmans

        domaines = ['example.com', 'mail.com', 'domain.com']  # à changer selon besoin

        for i in range(20):
            nom = random.choice(noms).lower()
            prenom = random.choice(prenoms).lower()
            domaine = random.choice(domaines)

            # Exemple email prenom.nom@domaine.com
            email = f"{prenom}.{nom}@{domaine}"

            # Mot de passe simple pour test
            password = "password123"

            if CustomUser.objects.filter(email=email).exists():
                self.stdout.write(f"{email} existe déjà, ignoré.")
                continue

            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                nom=f"{prenom.capitalize()} {nom.capitalize()}",
                niveau_etude=random.choice(['bac', 'licence', 'master', 'doctorat', 'autre']),
                telephone=f'06{random.randint(10000000, 99999999)}',
            )
            self.stdout.write(f'Créé : {user.email} / {user.nom}')
