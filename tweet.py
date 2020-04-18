# Librairies importées pour la bonne exécution de la fonction
import tweepy
import random
import csv
import tempfile
import requests
import mimetypes

# Fichier contenant les données permettant de se connecter à l'API de Twitter
from auth import *

# Fonctions


def telechargement_image(url):
    """
    Fonction qui permet de télécharger et d'ouvrir une image à partir d'un url
    :param url: url extrait de Wikidata
    :return: image ouverte
    """

    response = requests.get(url)
    content_type = response.headers['content-type']
    extension = mimetypes.guess_extension(content_type)
    img = response.content
    f = tempfile.NamedTemporaryFile(suffix=extension)
    f.write(img)
    return f


def tweeter():
    """
    Fonction qui permet de tweeter le nom, le portrait et le lien Wikipédia d'un.e des révolutionnaires
    choisi.e au hasard
    """

    # Authentification à Twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # Création d'une API et vérification du succès de l'authentification
    api = tweepy.API(auth)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    # Récupération des données issues du fichier csv
    with open ('/Users/alexandrebartz/PycharmProjects/Bot/Revolutionnaires.csv', 'r') as file:
        liste_revo = list(csv.reader(file))
        revolutionnaire = random.choice(liste_revo)
        nom = revolutionnaire[0]
        url_image = revolutionnaire[1]
        url_wikipedia = revolutionnaire[2]
        portrait = telechargement_image(url_image)
        uploaded = api.media_upload(filename= portrait.name)

    # Publication du tweet
    api.update_status(status="Notre révolutionnaire du jour est " + nom + ". Cliquez sur ce lien pour en savoir plus : "
                    + url_wikipedia + " #wikidata #BotRevolution", media_ids=[uploaded.media_id])

    portrait.close()


# Lancement de la fonction

if __name__ == "__main__":
    tweeter()

