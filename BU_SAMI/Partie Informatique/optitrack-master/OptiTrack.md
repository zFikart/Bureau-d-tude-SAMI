# Système Prime x 22 - OptiTrack

Le nouveau [système OptiTrack](https://optitrack.com) vient en remplacement des anciennes caméra dont la précision été assez faible et don tle cout de réparation été prohibitif.

Les [caméras Prime x22](https://optitrack.com/cameras/primex-22/) fontionnent via Ethernet (RJ45) en PoE. Un nouveau switch Netgear GS728TPP sera donc installé (il faudra penser à retirer les câbles!).

## documentation fournie et licence
Une enveloppe est livrée avec 5 pages A4

  * Quick Start Guide : Présentation de l'installation
  * Motive : initialisation de l'installation
  * Motive App Note concernant l'équerre de calibration (CS-200 dans notre cas)
  * CW-500 Quick Start Guide (le Wand dans l'ancien système)
  * V120:Duo&Trio : nous ne possédons pas ce système

 et un carton de licence :

  * Software : Motive:Tracker
  * License Serial Number : MVCL7533
  * License Hash Code : B7A5-93AA-BFF4-0E51

Le support est joignable à optitrack.com/support (tel 1-888-965-0435)

## Logiciel
Se rendre dans la partie [downloads de OptiTrack](https://optitrack.com/downloads/). Le logiciel Motive en est à la 2.2.0 (8 novenbre 2019). La documentation de la [version 2.2](https://v22.wiki.optitrack.com). Le logiciel utilisé est la version Motive:Tracker. Les deux autres plus complètes sont body et Expression. Motive:Tracker permet, en streaming, les format NatNet, VRPN et Trackd.

### Installation du logiciel
Après téléchargement de la version 2.2.0, l'éxcution de l'installeur indique qu'il va commencer par installer MS_Direct_9c_2009_August et OptiTrack_USB_Drivers_x64. Manifestement il installe aussi le framework .Net3.5. Puis l'instaleur de Motive proprement dit est lancé dans c:\Program Files\OptiTrack\Motive.

### Premier lancement
On commence par saisir la licence :

  * License Serial Number : MVCL7533
  * License Hash : B7A5-93AA-BFF4-0E51
  * Hardware Key Serial Number : 362527 (sur la clé USB)
  * E-mail Adress : jlm
  * First Name : jl
  * Last Name : M
  
Le fichier de licence est installé dans c:\ProgramData\OptiTrack\Lisense\Il faut insérer la clé USB pour pouvoir lancer le logiciel Motive ; sur un vie PC en W8 ça peut prendre un certain temps : 
 
### Menus

  * Files : C'est là que se font les sauvegardes.
  * Edit : on y trouve nottament l'Application Settings...
  * View : nombreuses otptions d'affichage à l'écran.
  * Layout : Calibrate, Create, Capture, Edit / Create Layout, Delete Layout, Update Current, Set Current As Default.
  * Tools : 2 options ; Mesuremente et Audio Settings. Pas d'utilité a priori
  * Community : pour aller plus loin.
  * Help : Show Quick Start est l'écran d'accueil au premier lancement. Il permet l'accès rapide à certaine fonctionnalité comme la calibration. Startup New Check permet d'avoir les dernière mise à jour au démarrage. L'option est désactivée pour une utilisation à l'ENSEM.

https://ensiwiki.ensimag.fr/index.php?title=Syst%C3%A8me_de_pointage_par_orientation_de_la_t%C3%AAte

## Configuration

### préparation de motive

Installer le logiciel téléchargé et renseigner les informations de licence. Il ne faut pas oublier d'installer le dongle USB sur un port de l'ordinateur pour pouvoir utiliser Motive. Il n'y a rien de bien particulier à faire d'autre.

### Calibration des de l'otitrack avec Motive (V2.2)

L'opration de calibration des caméras décrit ci-dessous est l'adaptation de la [documentaion touvée sur le site de l'ensimag](https://ensiwiki.ensimag.fr/index.php?title=Calibrage_de_l%27Optitrack_avec_Motive). 

  1. Placer les caméras. Dans le cadre du suivi des Robots Lego sur le plan de la salle SAMI, le choic a été d'orienter les caméras de façon à ce quelles observent chacune la (quasi)totalité du plateau. Pour se faire, les caméras x22 disposent d'un bouton "Aim assit" sencé permettre à un opérateur seul de faire la calibration... ce n'est pas aussi évident que ça ! Ce bouton, permet d'informer Motive que l'on veux régler la caméra et entraine l'ouverture d'une vue en niveau de gris (MJPEG) pour cette caméra. Ainsi on peut observer l'espace en noir et blanc et donc orienter correctement la caméra par rapport à l'image renvoyée sur l'écran.
  2. Metre au milieu de la scene une boule réfléchissante afin de faire la mise au point de la caméra (l'équere avec ses trois petites boulles est parfaite pour cela.
  3. Dans les propriété de la caméra on peut repasser en mode Objet et zoomer sur la (ou les) boule(s) sur la scène. Par défaut, les valeurs Exposure et Threshold sont respectivement à 250 et 200. Le seuil (Threshold) ne semble pas avoir une grande influance de notre cas ; on le laisse à 200. En revanche l'exposition (Exposure) placée au minimum à 10 micro s et suffisent pour voir les boules correctement. Si ce n'est pas le cas, il faut augmenter la valeur jusqu'à les voir. Cette valeur minimume permet d'effacer nombre de parasites lumineux détectés pas la caméra pour des valeurs plus élevées.
  4. Reste à faire la mise point. Les caméras sont équipées de 2 bagues pour le focus (vers l'avant sur les x22) et pour le diaphragme (F-stop et F-number vers l'arrière seu les x22) pour la luminosité absorbée f/x (rapport focale sur ouverture). Par défaut, de diaphragme est réglé au maximum à f/1,6. Cette valeur convient parfaitement. Avec un zoom important, il est possible de régler finement la focus en tournant délicatement la bague de devant. Elle n'a pas été vérouillée en sérant la vis qui modifie fortement le réglage.
  5. Une fois toutes les caméras correctement orientées et réglées, il faut enveler toutes les boules présentes dans l'espace observable des caméras et choisir dans l'onglet préview. Il faut alors cliquer sur le bouton "Mask visible markers" (auparavent on peut faire un reset des masques pour oublier l'ancienne configuration)
  6. Placer l'optiwand (l'espèce de chandelier avec les trois boules) dans le champ de vision des caméras, puis dans la fenêtre de droite, sous "Calibration Options", préciser la taille de l'OptiWand que vous utilisez(large, medium ou small), puis cliquer sur "Start Wanding".
  7. Si les 3 boules de l'OptiWand sont bien repérées, les faire bouger un peu partout dans l'espace de manière à recouvrir une bonne partie des écrans de chaque caméra, puis arrêter le wanding. Il y a alors un temps de calcul qui abouti à une qualité de calibration.
  8. Placer le U avec les trois boules (le calibration square) à un endroit où il est repérable par les caméras, puis, toujours dans la fenêtre de droite, dans l'onglet "Ground Plane", cliquer sur "Set Ground Plane".
  9. C'est fini...

### Définition des Mobiles

La page [suivi d'un corps rigide](https://translate.google.com/translate?hl=fr&sl=en&tl=fr&u=https%3A%2F%2Fv22.wiki.optitrack.com%2Findex.php%3Ftitle%3DAiming_and_Focusing) décrit la façon de configurer un mobile.

  1. Mettre le mobile dans le champs de vision des caméras
  2. Choisir le menu Layout/create. La vue Buider apparait
  3. Seelctinoner les marqueurs associés au mobile dans la vue 3D
  4. Le type à créer est Rigid Body que l'on nomme par exemple Lego1 pour le robot Lego N° 1
  5. Valider la création.
	

    Une fois la ressource de corps rigide créée, les marqueurs seront colorés (étiquetés) et interconnectés les uns aux autres. Le corps rigide nouvellement créé sera répertorié sous le volet Actifs .

Info2.png

	

Si les corps rigides, ou des squelettes, sont créés dans le mode d'édition, correspondant Prenez doit être étiqueté automatiquement . Ce n'est qu'alors que les marqueurs de corps rigides seront étiquetés à l'aide de l'élément de corps rigide et les positions et orientations seront calculées pour chaque cadre.
Créer un corps rigide


Propriétés du corps rigide

Les propriétés de corps rigides se composent de diverses configurations d'actifs de corps rigides dans Motive et déterminent comment les corps rigides sont suivis et affichés dans Motive. Pour plus d'informations sur chaque propriété, lisez la page Propriétés: Corps rigide .
Propriétés par défaut

    Lors de la création initiale d'un corps rigide, les propriétés de corps rigide par défaut sont appliquées aux éléments nouvellement créés. Les propriétés de création par défaut sont configurées sous l' onglet Corps rigides Paramètres d'application .

Modifier les propriétés

    Les propriétés des éléments de corps rigides existants peuvent être modifiées à partir du volet Propriétés .

Propriétés d'un corps rigide sélectionné sous le volet Propriétés .
Ajouter ou supprimer des marqueurs

Un corps rigide existant peut être modifié en ajoutant ou en supprimant des marqueurs à l'aide du menu contextuel.

    Sélectionnez d'abord un corps rigide dans le volet Actifs ou en sélectionnant le point de pivot dans la vue en perspective .
    Ctrl + clic gauche sur les marqueurs que vous souhaitez ajouter / supprimer.
    Cliquez avec le bouton gauche sur le volet Vue en perspective pour ouvrir le menu contextuel du corps rigide.
    Sous Corps rigide, choisissez Ajouter / Supprimer les marqueurs sélectionnés dans / du corps rigide.
    Si nécessaire, cliquez avec le bouton droit sur le corps rigide et sélectionnez Réinitialiser le pivot pour déplacer le point de pivot vers le nouveau centre.

Info2.png

	

Plusieurs corps rigides

Lorsque plusieurs corps rigides sont sélectionnés, le menu contextuel s'applique uniquement à la sélection de corps rigide principal uniquement. Le corps rigide principal est le dernier corps rigide que vous avez sélectionné et son nom apparaîtra dans le coin inférieur droit de la fenêtre 3D .
Ajout d'un marqueur supplémentaire à un élément de corps rigide existant.
Modification / affinage d'un corps rigide

Les définitions de corps rigides créées peuvent être modifiées à l'aide des outils d'édition du volet Générateur ou en suivant les étapes décrites dans les sections suivantes. 

### Configuration du Multicast

  1. Choisir dans les View, l'écran (pane) "Data Streaming Pane".
  2. valide le "Broadcast frame data", 
  3. choisir l'interface (ici 100.64.212.150). 
  4. On ne suit que les "Rigid Bodies". 
  5. L'axe vers le haut (Up Axis) est l'axe Z, pas de remote Trigger. 
  6. La transmission est de type Multicast. 
  7. On peux choisir par défaut les streaming Engine parmis les plugins preinstallés : VRPN ou/et Trackd.

https://v22.wiki.optitrack.com/index.php?title=Data_Streaming_Pane

Sur le PC de réception, il faut ouvrir un socket UDP lié à l'optitrack (10.10.0.3) vers celui de l'optitrack 10.10.0.254 

### Suivi d'un corps rigide

La page sur le [streaming des données](https://v22.wiki.optitrack.com/index.php?title=Data_Streaming) permet de découvrir que pour faire du suivi de mobile rigide, il faut installer un plugin dont la liste est en base de page. Nous pouvons utiliser les plugins suivants :

  * [NatNet SDK](http://optitrack.com/products/natnet-sdk/)
  * [Autodesk MotionBuilder Plugin](http://optitrack.com/downloads/#mobu-plugin)
  * [Unreal Engine 4 Plugin](http://optitrack.com/downloads/)
  * [Unity Plugin](http://optitrack.com/downloads/)
  * 3ds Max Plugin : plus maintenu.
  * [VRPN Sample]() : proget [open source sur git Hub](https://github.com/vrpn/vrpn)
  * [trackd](https://optitrack.com/downloads/plugins.html#trackd)
  * Motive API n'offre pas de multicast sur le réseau
  * [VCS:Maya](http://optitrack.com/downloads/insight-vcs.html) : nécessite une licence à part.


