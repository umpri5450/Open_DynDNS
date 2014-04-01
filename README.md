ricm4BoeyGuo
============

Projet RICM4 2014 (BOEY Lionel et GUO Tianming)



****Version sécurisé Public OpenDynDNS****
-Verifier que la machine a accès à internet

-Il faut que le serveur DNS marche avec configurations normal (ici j'ai mis seuelement le fichier de zone à manipuler dans la repertoire pour tester )

-Installer psutil
	$ pip install psutil
	
-Installer OpenSSL
	sudo apt-get install openssl

-Installer Flask
	$ pip install flask-restful
      
-Lancer le serveur REST dans un terminal en mode sudo
      $ sudo python rest.py
      
-On peut interroger le serverweb avec un navigateur sur l'adresse https://127.0.0.1:5000/hosts/host1
      
-Lancer le client dans un autre terminal
      $ python client_ordi.py
      
Login : admin     MDP : admin
            
PS : format de texte un peu pourri pour le README..
