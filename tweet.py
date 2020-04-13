import tweepy
import random
import csv
import tempfile
import requests
import mimetypes

from auth import *

# Fonctions


def telechargement_image(url):
    "Fonction qui permet d'ouvrir une image"
    response = requests.get(url)
    content_type = response.headers['content-type']
    extension = mimetypes.guess_extension(content_type)
    img = response.content
    f = tempfile.NamedTemporaryFile(suffix=extension)
    f.write(img)
    return f


def tweeter():
    "Fonction qui permet de tweeter un message"

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

    # Récupération des données
    with open ('/Users/alexandrebartz/PycharmProjects/Bot/revo.csv', 'r') as file:
        liste_revo = list(csv.reader(file))
        revolutionnaire = random.choice(liste_revo)
        nom = revolutionnaire[0]
        url = revolutionnaire[1]
        portrait = telechargement_image(url)
        uploaded = api.media_upload(filename= portrait.name)

    # Publication du tweet
    api.update_status(status="Notre révolutionnaire du jour est " + nom + " #Révolution #BotRevolution",
                          media_ids=[uploaded.media_id])
    portrait.close()


# Publication du tweet

if __name__ == "__main__":
    tweeter()

