ricm4BoeyGuo
============

Projet RICM4 2014 (BOEY Lionel et GUO Tianming)

**********************************
A faire auparavant :
**********************************
- Installer python-dev pour eliminer des erreurs de pip

    $ sudo apt-get install python-dev
    
- Installer psutil

    $ pip install psutil
  
- Installer requests
	
    $ pip install requests
	
- Installer OpenSSL

    $ sudo apt-get install openssl

- Installer Flask-RESTful

    $ pip install flask-restful
    
- Il faut que le serveur DNS marche avec configurations normal (ici j'ai mis seuelement le fichier de zone 'db.tesopendyn.com' à manipuler dans la repertoire courant pour tester )

- Verifier que "host1" est déja defini dans le fichier de zone DNS. Il faut redemarrer bind9 pour chaque modification manuelle ou directe sur le serveur DNS

    $ sudo /etc/init.d/bind9 restart

**********************************
Version sécurisé Public OpenDynDNS
**********************************

- Verifier que la machine a accès à internet

- Lancer le serveur REST dans un terminal en mode sudo

    $ sudo python rest.py
    
- On peut interroger le serverweb avec un navigateur sur l'adresse https://127.0.0.1:5000/hosts/host1

    Login : admin     MDP : admin
      
- Lancer le client dans un autre terminal
    
    $ python client_ordi.py

Notes : 

+ On peut interroger le serveur DNS par la commande dig. Example:
    $ dig ns.testopendyn.com @127.0.0.1
    cette commande va interroger l'hote "ns" dans le domaine testopendyn.com
    
**********************************
Version sécurisé Local OpenDynDNS
**********************************
- Verifier que le server REST/DNS sont branché sur un switch local (pas de connexion internet necessaire)

- Lancer le serveur REST dans un terminal en mode sudo

    $ sudo python rest.py
    
- Lancer le daemon mDNS 'mdns_dns.py' sur la meme machine que le serveur REST/DNS

    $ python mdns_dns.py
    
- Lancer le daemon mDNS 'mdns_client.py' sur une autre machine dans le reseau local (on a besoin de sudo car le daemon va modifier le nameserver du systeme)

    $ sudo python mdns_client.py
    
- Verifier le reseau par les pings et les digs entre machines. Les participants du mDNS doivent arriver à se voir juste par nom (ping client1.testopendyn.com)