ricm4BoeyGuo
============

Projet RICM4 2014 (BOEY Lionel et GUO Tianming)



****Version de test Public OpenDynDNS****
-Verifier que la machine a accès à internet

-Il faut d'abord installer Flask 
      $ pip install flask-restful
      
-Lancer le serveur REST dans un terminal
      $ python test.py 
      
-On peut interroger le serverweb avec un navigateur sur l'adresse http://127.0.0.1:5000/hosts
      
-Lancer le client dans un autre terminal
      $ python client.py
      
       
      
      
Effets: 

1) dans le fichier de base de donnée DNS (ici "db.testopendyn.com"), le ligne host1 avec l'adresse IP 99.99.99.99 au départ va être mise à jour avec la nouvelle adresse IP publique de votre machine
  
  2) un buffer existe sur le serveur REST pour enregister les mise-à-jours. Utile pour faire un IHM web si on a le temps..
  
  
  
Note : Le nginx viendra après