# Sujets imposés du blog (lu par n8n à chaque exécution)

Le workflow n8n « Les Éclairés — Blog 2x/semaine » prend **le premier sujet de la liste dont le slug n'existe pas encore** dans `blog/`.
Un sujet est donc « fait » dès que `blog/<slug>.html` existe : rien à cocher.

- Pour changer l'ordre : déplacer les lignes.
- Pour ajouter un sujet : ajouter une ligne au même format (slug unique, jamais de nom de ville).
- Liste épuisée : n8n repasse en mode automatique (rotation des cibles) et envoie un mail d'alerte dès qu'il reste 3 sujets ou moins.

Format d'une ligne (séparateur ` | `) :
`- cible | slug | titre indicatif | mot-clé principal | catégorie | page à mailler obligatoirement`

Cibles : particulier, copropriete, entreprise, collectivite.
Catégories du blog : Choisir & installer, Aides & prix, Copropriété, Entreprise, Recharge au quotidien.

## File d'attente

- entreprise | borne-recharge-flotte-vehicules-societe | Électrifier une flotte de véhicules de société : quelles bornes prévoir | borne de recharge flotte entreprise | Entreprise | /entreprise
- copropriete | vote-assemblee-generale-borne-recharge-copropriete | Faire voter un projet de bornes de recharge en assemblée générale | vote ag borne recharge copropriété | Copropriété | /copropriete
- particulier | devis-borne-de-recharge-points-a-verifier | Devis de borne de recharge : les lignes à vérifier avant de signer | devis borne de recharge | Choisir & installer | /simulateur
- entreprise | pilotage-de-charge-parking-entreprise | Parking d'entreprise : combien de bornes sur la puissance électrique existante | pilotage de charge entreprise | Entreprise | /entreprise
- copropriete | syndic-refuse-borne-recharge-que-faire | Le syndic refuse l'installation de ma borne : que faire | syndic refuse borne de recharge | Copropriété | /copropriete
- particulier | etapes-installation-borne-recharge-maison | Installer une borne à la maison : les étapes, du devis à la mise en service | installation borne de recharge maison | Choisir & installer | /simulateur
- entreprise | recharge-salaries-refacturation-entreprise | Recharge des salariés sur le parking : offrir ou refacturer l'électricité | refacturation recharge salariés | Entreprise | /entreprise
- collectivite | bornes-recharge-publiques-commune | Commune : comment déployer des bornes de recharge ouvertes au public | borne de recharge commune | Entreprise | /simulateur
- particulier | borne-recharge-maison-neuve-construction | Maison neuve : prévoir la borne de recharge dès la construction | borne de recharge maison neuve | Choisir & installer | /simulateur
- entreprise | borne-recharge-commerce-clients | Borne de recharge pour un commerce : un service qui attire des clients | borne de recharge commerce | Entreprise | /entreprise
- copropriete | cout-borne-recharge-copropriete-par-place | Bornes en copropriété : combien coûte l'équipement par place | prix borne de recharge copropriété | Copropriété | /copropriete
- particulier | borne-recharge-exterieur-precautions | Borne de recharge en extérieur : emplacement, protection et précautions | borne de recharge extérieur | Choisir & installer | /simulateur
