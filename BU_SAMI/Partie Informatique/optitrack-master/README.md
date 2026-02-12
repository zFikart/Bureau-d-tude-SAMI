# Optitrack
Développement d'un noeud Python pour gérer la communication entre les étudiants / chercheurs et Motive

- [Optitrack](#optitrack)
	- [Le Système Prime x22 (Motive et Optitrack)](#le-système-prime-x22-motive-et-optitrack)
		- [Présentation](#présentation)
		- [Mise en route](#mise-en-route)
	- [Noeud / client Python pour Optitrack (mode utilisateur)](#noeud--client-python-pour-optitrack-mode-utilisateur)
		- [Résumé](#résumé)
		- [Installation](#installation)
		- [Utilisation](#utilisation)
	- [Noeud / client Python pour Optitrack (mode développer)](#noeud--client-python-pour-optitrack-mode-développer)
		- [Prérequis](#prérequis)
		- [Installation](#installation-1)
		- [Démarrage rapide](#démarrage-rapide)
		- [Maintenance et développement](#maintenance-et-développement)



## Le Système Prime x22 (Motive et Optitrack)
### Présentation

Le nouveau [système OptiTrack](https://optitrack.com) vient en remplacement des anciennes caméra dont la précision été assez faible et dont le cout de réparation été prohibitif.

Les [caméras Prime x22](https://optitrack.com/cameras/primex-22/) fontionnent via Ethernet (RJ45) en PoE. Un nouveau switch Netgear GS728TPP sera donc installé (il faudra penser à retirer les câbles!). Elles diffusent une lumière dans l'infra-rouge et qui va illuminer des sphères de réflexion (grises). Le logiciel Motive déduit alors la distance séparant la sphère des caméras, puis par triangularisation, sa position dans l'espace.

Trois legos sont équipées de sphères définissant une empreinte unique.
**Veuillez ne pas y toucher!**

Le logiciel [Motive](https://optitrack.com/software/motive/) exécuté sur le PC ENSEM est capable de reconnaitre ces empreintes et ainsi d'identifié chaque robot. D'autre part, il mesure la localisation du centre de l'essieu et l'orientation du robot dans l'espace. Ces informations sont donnés dans le *repère de Motive* représenté en bleu sur la figure suivante.

![](/doc/repere_sami.png "Schéma de la salle SAMI avec les deux repères : SAMI (orange) et Motive (bleu)")

Les caméras Optitrack communiquent sur le réseau en s'appuyant sur un protocole propriétaire nommé [Natnet](https://v22.wiki.optitrack.com/index.php?title=OptiTrack_Documentation_Wiki). Afin de récupérer et décoder ces trames, il est nécessaire d'installer le client ou noeud Python détaillé dans la section suivante.



### Mise en route
Commencer par fermé les dijoncteurs situés dans le coffret électrique blanc au dessus de l'écran, à droite. Le routeur doit alors démarrer (lumières vertes allumées), ainsi que les six caméras (LED circulaires allumées).

![](/doc/boitier_elec.JPG "Photo 1: coffret électrique")

![](/doc/interrupteur_elec.JPG "Photo 2: interrupteur dijoncteur pour allumer Optitrack")

![](/doc/routeur.JPG "Photo 3: routeur")

Puis, appuyer sur le bouton de démarrage du PC. Ouvrir la session avec les logins suivants:
* utilisateur : .\ENSEM
* mot de passe : EnsemEnsem

Enfin, démarrer le logiciel MOTIVE. La fenètre principale s'ouvre, les LEGO 1, 2 et 3 sont automatiquement localisés et leur position diffusée sur le réseau.


## Noeud / client Python pour Optitrack (mode utilisateur)
### Résumé
Afin d'utiliser la localisation des robots dans une application, il est nécessaire de
1. déployer un client UDP sur votre machine
2. décoder les messages au format natnet diffusés par Motive
3. traiter les données brutes pour se ramener dans votre contexte applicatif.

Ces fonctions vous sont fournis via l'archive *Optitrack.zip*. Cette interface s'appuie sur trois objets : le client Natnet (`NatnetClient()`), les messages Natnet (`Packet()`) et le noeud d'interface (`MocapNode()`).

Afin de faciliter votre travail, les coordonnées sont convertis dans le *repère SAMI* représenté en orange sur la Figure.



### Installation 
Pour installer l'interface, veuillez décompresser le contenu de l'archive *Optitrack.zip* à la racine de votre programme. En supposant votre programme nommé *myprogram.py*, votre répertoire doit ressembler à :
* ./src/
* ./Tests/
* *config.ini*
* *myprogram.py*

Afin de tester l'installation, veuillez exécuter le programme *testAll.py* depuis la racine. Par exemple, ouvrez votre répertoire dans VisualStudio Code. Naviguez jusqu'à *./Tests/testAll.py*. Puis, pressez F5. L'ensemble des tests doit être validés que vous soyez connectés au réseau ou non.\\

### Utilisation
Pour utiliser l'interface, il est nécessaire de renseigner votre ip et celle du serveur Optitrack dans le fichier *config.ini*. Le serveur Optitrack de la salle SAMI répond à l'addresse : ``100.64.212.150``. Pour connaitre votre adresse ip, veuillez exécuter sous votre invite de commande : ``ipconfig``.

Une fois ces informations obtenues, ouvrez le fichier de configuration, ajoutez les lignes suivantes à fin du fichier (sans effacer ce qui existe déjà) en remplacant les champs par vos valeurs :

```ini
["MonNomDeConfig"]
srvAddr = "IPduServeur"
cltAddr = "MonIP"
\end{lstlisting}
 Par exemple, pour mon PC nommé \enquote{PC6} et travaillant sous l'ip: 100.64.212.156, j'inscris : 
\begin{lstlisting}
[PC6]
srvAddr = 100.64.212.150
cltAddr = 100.64.212.156
```

Dans votre programme, commencez par indiquer le chemin de l'interface :
```py
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'src'))
```

Ensuite, importez le module *mocap\_node.py* contenant la classe ``MocapNode()``. Ici, nous renommerons ce module ``mcn`` :

```py
import mocap_node as mcn
```


Créez un noeud Motion Capture (Mocap) à partir de votre configuration comme un objet ``MocapNode()``, soit :

```py
	mymcn = mcn.MocapNode("PC6")
```

Remarquez que le constructeur prend pour argument un string correspondant au champs ``MonNomDeConfig`` que vous venez de renseigner.\\

Lancez votre noeud à l'aide de la méthode ``run()`` :
```py
	mymcn.run()
```
A partir de cet instant, un client UDP est exécuté en tâche de fond. La communication avec les caméra est établie mais les messages ne peuvent pas encore être décryptés. Pour cela, il est nécessaire que le noeud récupère des méta-données transmises par le serveur. Ceci se réalise via la méthode ``updateModelInfo()`` :

```py
	mymcn.updateModelInfo()
```



Votre programme est maintenant prêt à acquérir des données de positions à l'aide de la méthode : ``getPos2DAndYaw(name (string))``.
Trois legos sont identifiés dans le noeud. Ils sont nommées : ``Lego1``, ``Lego2`` ou ``Lego3``. Pour obtenir la localisation du ``Lego2``, on exécute :

````
	pos2D, yaw = mymcn.getPos2DAndYaw("Lego2")
````
Cette méthode retourne:

* ``pos2D``, un tuplet de float composé des coordonnées en mètre selon les axes x et y
* ``yaw``, un float désignant l'orientation en radian selon l'axe z.
 
**IMPORTANT**: pensez à arrêter le noeud à la fin de votre programme via la méthode ``stop()``. Autrement, vous risquez de ne plus pouvoir relancer votre programme une seconde fois.
````
	mymcn.stop()
    
````



## Noeud / client Python pour Optitrack (mode développer)
Certaines applications nécessitent de modifier le client Python, soit pour ajouter de nouvelles fonctionnalités, soit pour modifier des paramètrage. **Toute modification du code doit être versionnée via Git et enregistrée sur le Gitlab de l'université !!**

### Prérequis
Vous devez disposez d'un client Git sur votre PC. Sous windows, nous vous recommandons [Git for Windows](https://gitforwindows.org/). 

Une première connexion au Gilab de l'université (https://gitlab.univ-lorraine.fr/) est nécessaire pour activer votre compte. Vos identifiants sont ceux de votre ENT.

Vous devez aussi demander les droits "développeur" aux responsables du dépots :
* Clément Fauvel (clement.fauvel@univ-lorraine.fr)
* Jean-Luc Metzger (jean-luc.metzger@univ-lorraine.fr)

### Installation
Afin de récupérer le projet, il est nécessaire d'exécuter :
``` bash
git clone https://gitlab.univ-lorraine.fr/coll/l-inp/ensem/projets-salle-sami/optitrack.git
```

### Démarrage rapide
Le projet doit être exécuté depuis un poste de la salle SAMI connecté en filaire au réseau. Le logiciel Motive doit être démarré. Le fichier de configuration ``` config.ini``` doit être paramétré correctement.

### Maintenance et développement
Pour mettre à jour le projet, il faut exécuter :
```bash
git pull
```

Veuillez créer vos propres branches afin de développer vos modification.
```bash
git checkout -b mybranch
```

Il est recommandé de nommer votre branche selon le format suivant : initial_fct. Par exemple, Jean Durand développe une nouvelle fonction de localisation dans l'espace pour Drone. Il créera la branch : "jd-3DLocDrone".

Ensuite, il faut "commiter" vos modifications / ajouts. Pour cela, ajouter les fichiers concernés :
```bash
git add my_files
```
Commiter en décrivant les changements :
```bash
git commit -m "Mon message"
```

 Puis il faut pousser le commit en désignant la branche du remote. Pour une nouvelle branche, tapez:
```bash
git push --set-upstream origin mybranch
```
puis, pour les ```push``` suivants :
```bash
git push -u
```

Une fois votre modification testée et validée, vous pouvez la soumettre aux mainteneur du dépot. Pour cela, veuillez utiliser la fonction "Merge request" de Gitlab.