/* Nœud Code « Partenaires par département ».
   Liste COMPLÉMENTAIRE d'installateurs partenaires signés (une ligne par partenaire).
   La source principale est Kalend : une fiche « Installateur IRVE » au statut Client = partenaire signé.
     depts : départements couverts, entre guillemets ('69', '42', '2A', '974'...)
     types : types de demandes acceptés parmi 'simulateur' (particuliers), 'copropriete', 'entreprise'
   Exemple :
     { nom: 'Élec Dupont', contact: 'Jean Dupont', email: 'jean@elec-dupont.fr', depts: ['69', '42'], types: ['simulateur', 'copropriete', 'entreprise'] },
*/
var PARTENAIRES = [
];

/* La demande vient du nœud Normaliser ; l'entrée de ce nœud est la réponse de Kalend (ou une erreur si Kalend est injoignable). */
var d = $('Normaliser').first().json;
var k = ($input.first() && $input.first().json) || {};
var kalend = Array.isArray(k.installateurs) ? k.installateurs : [];
d.partenaires = [];
d.prospects = [];
d.kalendOk = Array.isArray(k.installateurs);
d.kalendTotal = k.total || kalend.length;
if (d.type !== 'partenaire' && d.dept) {
  d.partenaires = PARTENAIRES.filter(function (p) {
    return (p.depts || []).map(String).indexOf(d.dept) !== -1 && (!p.types || !p.types.length || p.types.indexOf(d.type) !== -1);
  });
  kalend.forEach(function (i) {
    if (i.partenaire) d.partenaires.push({ nom: i.nom, contact: i.ville, email: i.email, telephone: i.telephone });
    else d.prospects.push(i);
  });
}
return [{ json: d }];
