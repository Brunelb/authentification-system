# 🔐 Django Authentication System with Email Verification

## 📌 Description

Ce projet est une application web développée avec **Django** qui implémente un système complet d’authentification des utilisateurs avec :

* inscription (register)
* connexion (login)
* déconnexion (logout)
* envoi d’email de bienvenue
* activation du compte par email (email verification)

👉 L’utilisateur doit **confirmer son adresse email avant de pouvoir se connecter**.

---

## 🚀 Fonctionnalités

* ✅ Création de compte utilisateur
* ✅ Validation des données (username, email, mot de passe)
* ✅ Envoi d’un email de bienvenue
* ✅ Envoi d’un email d’activation avec lien sécurisé
* ✅ Activation du compte via token
* ✅ Blocage de connexion si compte non activé
* ✅ Authentification sécurisée avec Django
* ✅ Messages utilisateur (succès / erreur)

---

## 🧠 Logique du système

### 🔹 1. Inscription

* L’utilisateur remplit le formulaire
* Le compte est créé avec `is_active = False`
* Deux emails sont envoyés :

  * 📧 Email de bienvenue
  * 📧 Email d’activation avec lien sécurisé

---

### 🔹 2. Activation du compte

* L’utilisateur clique sur le lien reçu
* Django vérifie :

  * `uid`
  * `token`
* Si valide :

  ```python
  user.is_active = True
  ```
* Le compte est activé

---

### 🔹 3. Connexion

* Si `is_active = False` → accès refusé
* Si `is_active = True` → accès autorisé

---

## 🛠️ Technologies utilisées

* Python 3.x
* Django 5.x
* SMTP Gmail (envoi d’email)
* HTML / CSS
* Bootstrap
* Django Messages Framework



---

## ⚙️ Configuration Email (Gmail SMTP)

Créer un fichier `Info.py` :


EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
EMAIL_PORT = 587

Puis dans `settings.py` :


from .Info import EMAIL_USE_TLS, EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = EMAIL_USE_TLS
EMAIL_HOST = EMAIL_HOST
EMAIL_HOST_USER = EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD
EMAIL_PORT = EMAIL_PORT
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


---

## 🔐 Sécurité importante

* Activer la **validation en deux étapes (2FA)** sur Gmail
* Utiliser un **mot de passe d’application**
* Ne jamais publier ses identifiants sur GitHub ❌

---

## 🔗 Activation du compte

##URL utilisée :


path('activate/<uidb64>/<token>/', views.activate, name='activate')

##Lien généré dans l’email :


http://{{ domain }}{% url 'activate' uidb64=uid token=token %}



## ▶️ Lancer le projet

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

---

## 📌 Améliorations possibles

* 🔐 Authentification avec Google OAuth
* 🔄 Réinitialisation de mot de passe par email
* 📱 Interface moderne (Bootstrap / Tailwind)
* 🧾 Journalisation des connexions
* 🌐 Déploiement (Render / Heroku / VPS)

---

## ⭐ Objectif du projet

Mettre en place un système d’authentification sécurisé avec :

* validation email
* gestion des utilisateurs
* intégration SMTP réelle
