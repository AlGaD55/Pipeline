Le Pipeline2, a permis d'automatiser les différentes étapes de la création des tables dans Dbeaver. Le Pipeline, est un script python qui prend en compte la connexion à la base sous Dbeaver, et la création des différentes tables en passant par le contrôle de ces différentes etapes.


Le script du Pipeline comprend plusieurs étapes 

**Connexion à la base de données Dbeaver 

Cette étape permet de se connecter à la base de données Dbeaver. Les différents paramètres de connexion sont renseignés, sauf le mot de passe, qui sera saisi manuellement. 

** Execution de la première partie des scripts Sql, depuis la réinitialisation de la base, nettoyage et création des premières tables. Cette étape, passe par la création d'une boucle for, qui exécute les différents requêtes sql, et écrit les informations d'exécution dans un journal.

**Etapes Python : ces étapes ne traitent pas des fichiers Sql, mais des fichiers json et csv. Le but ici, est de traiter les fichiers json et csv, qui viendront alimenter les tables précédemment créée en sql. Ces étapes ont recours à des boucles en python . La première boucle crée un dataframe qui pourra être lue via des requêtes sql, et un second script, permettra de copier les données issue du fichier json et convertie, dans la table meteo_assurrisk
Par la suite, un autre script, permettra de copier les données du fichier csv ville_coordonnees_meteo, dans la table ville coordonnee_meteo.

** Etape d'exécution des 3 derniers scripts SQL : à ce niveau, recours sera fait de nouveau à une boucle for qui lira la liste contenant les 3 fichiers afin de les traiter après les avoirs ouverts. On précise que ces trois fichiers Sql, ont été ajouté dans la liste au moyen de la méthode append
Dans la boucle for, on aura ajouter une commande permettant de connaitre la durée d'exécution des différentes étapes.

** Etape de création du fichier journal du Pipeline
A cette étape, un journal sera créer en csv, permettant de suivre la bonne exécution du Pipeline

**Etape des différents contrôles
Cette étape permet de contrôler le volume des différentes tables de la base de données, puis une dernière étape, sauvegarde ces information dans un fichier controle.csv


