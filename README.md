
TDLOG : Projet Shazam
=

L'objectif de ce projet est de réaliser une copie de l'algorithme de l'application Shazam, cette application permet d'identifier une musique enregistrée à partir du micro du téléphone. L'objectif n'est bien sûr pas de rencontrer les mêmes performances que celles de la vraie application mais de s'en approcher.   
On souhaite également créer une interface utilisateur, sous forme d'un site internet sur lequel il serait possible d'ajouter des sons dans une base de données, et d'ensuite identifier le son correspondant à un extrait sonore donné dans la base de données.
De ce fait notre projet se découpe en deux parties ayant chacunes leurs propres objectifs croissants :  




Partie Algorithme de Shazam
-
Ce que nous avons compris pour le moment de l'algorithme de Shazam :      
Pour ce qui est du fonctionnement de l'algorithme de Shazam notre
principale source d'information est un article du site internet "Les
Numériques" traitant du sujet :  <https://www.lesnumeriques.com/audio/magie-shazam-dans-entrailles-algorithme-a2375.html>   
L'algorithme comprend en réalité 2 phases :   
1. Analyse sonore et dégagement d'une empreinte :   
Pour être en mesure d'identifier des musiques et ce de la façon la plus rapide possible, Shazam associe à chaque musique une empreinte qui lui est propre, un peu comme une empreinte digitale. Pour créer cette empreinte Shazam procède par analyse sonore, il fait tout d'abord une transformation de Fourier qui lui donne un
spectromètre du son, duquel il ne retient que les fréquences de plus grande intensité à un instant t. On a alors ce qu'on appelle un spectromètre en constellation. De ce dernier on va pouvoir obtenir l’empreinte attendue, pour ce faire pour chaque point de la constellation, nommé alors “point d'ancrage", on définit une zone cible. Tous les points se trouvants dans la zone cible donnent lieu à la création d’un marqueur temporel : [(Fréquence du point d'ancrage, Fréquence du point dans la zone cible, Intervalle de temps entre les deux points), instant t du point d'ancrage].
L’ajout de l’ensemble des marqueurs temporels d’un extrait sonore dans une liste constitue alors notre empreinte du morceau. 


2. Matching entre un extrait et une base de données :    
Une fois la base de données alimentée avec des morceaux et leur empreinte associées, il faut maintenant être en mesure d’associer l’empreinte d’un extrait sonore à celle d’un morceau. Pour ce faire, Shazam utilise les marqueurs temporels des empreintes, dès que les 3 premiers arguments d’un marqueur temporel sont les mêmes dans l’empreinte de l’extrait et celle d’un morceau, il fait la différence du 4ème argument et la retient dans une liste propre au morceau. Puis il réalise un histogramme de ces différences, si un intervalle detaT de temps se dégage très largement statistiquement c’est qu’il est très probable qu’il s'agisse bien du bon morceau mais pour lequel l'extrait sonore est joué à partir de l’instant deltaT. On a donc dans ce cas là un match donné avec une incertitude liée à la statistique de l’histogramme.  



Objectifs croissants de la partie : 
* Partir d'un extrait sonore et en dégager une empreinte.
* Faire un algorithme capable de réaliser le matching d'un
extrait d'un son (partie du son non-détériorée) avec ce son présent en base de donnée.
* Essayer l'algorithme sur une base de données plus vaste et des extraits sonores de moins grande qualité.




Partie création de l'interface utilisateur
-
Objectifs croissants de la partie : 
* Faire une interface web avec une base de données sur laquelle on peut interagir.(ajouter un son ou en retirer un)
* Faire en sorte de pouvoir lancer l’analyse sonore des morceaux dans la base donnée pour leur associer une empreinte. 
* Faire en sorte de pouvoir ajouter un extrait sonore sur lequel on effectue la création d’empreinte et la recherche de matching, pour enfin donner un résultat avec possiblement un intervalle de confiance.


