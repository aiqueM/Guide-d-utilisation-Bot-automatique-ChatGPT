# Guide-d-utilisation-Bot-automatique-ChatGPT
Ce programme va automatiquement :  
1. Prendre une image dans un dossier
2. L'envoyer à ChatGPT avec un message prédéfini
3. Attendre 5 minutes
4. Recommencer avec la prochaine image
5. Déplacer chaque image utilisée dans un dossier "used"

🛠️ ÉTAPE 1 — Installer Python

Aller sur https://www.python.org/downloads/
Cliquer sur le gros bouton jaune "Download Python"
Ouvrir le fichier téléchargé
⚠️ IMPORTANT : Avant de cliquer sur "Install Now", cocher la case "Add Python to PATH" en bas de la fenêtre
Cliquer sur "Install Now"
Attendre la fin de l'installation puis cliquer "Close"

🛠️ ÉTAPE 2 — Installer PyCharm

Aller sur https://www.jetbrains.com/pycharm/download/
Télécharger la version Community (gratuite) — cliquer sur "Download" sous "Community"
Ouvrir le fichier téléchargé et suivre les étapes d'installation
Laisser toutes les options par défaut et cliquer "Next" jusqu'à "Install"
À la fin, cliquer "Finish"

🛠️ ÉTAPE 3 — Télécharger EdgeDriver
EdgeDriver permet au script de contrôler le navigateur Edge.

Ouvrir Microsoft Edge
Dans la barre d'adresse, taper : edge://settings/help et appuyer sur Entrée
Noter le numéro de version affiché (exemple : 124.0.2478.51)
Aller sur https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
Télécharger la version qui correspond exactement à votre numéro de version
Décompresser le fichier ZIP téléchargé
Déplacer le fichier msedgedriver.exe dans un endroit facile à retrouver, par exemple :

🛠️ ÉTAPE 4 — Ouvrir le script dans PyCharm

Lancer PyCharm
Sur l'écran d'accueil, cliquer "Open"
Naviguer jusqu'au fichier chatgpt_image_bot.py et l'ouvrir
PyCharm va afficher le code du script

🛠️ ÉTAPE 5 — Installer la bibliothèque Selenium
Selenium est l'outil qui permet de contrôler le navigateur automatiquement.

Dans PyCharm, regarder en bas de l'écran — cliquer sur "Terminal"
Une petite fenêtre noire va s'ouvrir
Taper exactement ceci et appuyer sur Entrée :

python -m pip install selenium

Attendre que l'installation se termine (quelques secondes)

🛠️ ÉTAPE 6 — Modifier la configuration du script
En haut du fichier, il y a une section CONFIGURATION. Il faut modifier 3 lignes :
🔹 Ligne 1 — Le dossier contenant vos images
pythonIMAGES_FOLDER = r"C:\Users\VotreNom\Downloads\VosDossierImages"
Remplacer le chemin entre guillemets par le chemin vers votre dossier d'images.

💡 Comment trouver le chemin ?
Ouvrir le dossier dans l'Explorateur de fichiers → cliquer sur la barre d'adresse en haut → copier le texte qui apparaît

🔹 Ligne 2 — Le dossier "used" (images déjà utilisées)
pythonDONE_FOLDER = r"C:\Users\VotreNom\Downloads\VosDossierImages\used"
C'est le même chemin que ci-dessus, avec \used ajouté à la fin. Ce dossier sera créé automatiquement.
🔹 Ligne 3 — Le chemin vers msedgedriver.exe
pythonEDGE_DRIVER_PATH = r"C:\Users\VotreNom\Downloads\edgedriver_win64\msedgedriver.exe"
Remplacer par le chemin où vous avez placé le fichier msedgedriver.exe à l'Étape 3.

⚠️ Remplacer VotreNom par votre vrai nom d'utilisateur Windows dans tous les chemins.

🛠️ ÉTAPE 7 — Créer un profil Edge dédié et se connecter à ChatGPT
Cette étape se fait une seule fois.

Appuyer sur les touches Windows + R en même temps
Une petite fenêtre s'ouvre — taper exactement ceci et appuyer sur Entrée :

   powershell

Dans la fenêtre PowerShell qui s'ouvre, taper exactement ceci et appuyer sur Entrée :

   Start-Process "msedge.exe" "--user-data-dir=C:\EdgeAutomationProfile"

Une nouvelle fenêtre Edge va s'ouvrir
Dans cette fenêtre, aller sur https://chatgpt.com et se connecter avec votre compte ChatGPT
Une fois connecté, fermer complètement cette fenêtre Edge

✅ Le profil est maintenant sauvegardé. Le script utilisera ce profil à chaque fois.

🛠️ ÉTAPE 8 — Préparer vos images

Mettre toutes vos images (JPG, JPEG, PNG, etc.) dans le dossier que vous avez indiqué à l'Étape 6
Vérifier que le dossier ne contient que des images (pas d'autres fichiers)

▶️ ÉTAPE 9 — Lancer le script

⚠️ Fermer toutes les fenêtres Edge ouvertes avant de lancer
Dans PyCharm, cliquer sur le bouton ▶ (triangle vert) en haut à droite
Une fenêtre Edge va s'ouvrir automatiquement et commencer à travailler
Dans le terminal en bas de PyCharm, vous verrez l'avancement :

   [1/10] ── image1.jpg
     🌐  Opening ChatGPT...
     🖼️   Uploading image...
     ✍️   Typing prompt...
     📤  Sending message...
     ✅  Message sent successfully.
     ⏳  Next image in: 24:59

Ne pas fermer PyCharm ni la fenêtre Edge pendant que le script tourne

⏹️ COMMENT ARRÊTER LE SCRIPT

Cliquer sur le carré rouge ⏹ dans PyCharm (en bas ou en haut selon la version)
OU cliquer dans le terminal et appuyer sur Ctrl + C

🔄 CHANGER DE COMPTE CHATGPT
Si vous voulez utiliser un autre compte :

Ouvrir PowerShell (touches Windows + R → taper powershell → Entrée)
Taper ceci et appuyer sur Entrée :

   Remove-Item -Recurse -Force "C:\EdgeAutomationProfile"

Puis retaper ceci et appuyer sur Entrée :

   Start-Process "msedge.exe" "--user-data-dir=C:\EdgeAutomationProfile"

Se connecter avec le nouveau compte dans la fenêtre qui s'ouvre
Fermer la fenêtre Edge
Relancer le script normalement

