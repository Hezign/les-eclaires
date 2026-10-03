/* Nœud Code « Partenaires par département ».
   Liste des installateurs partenaires SIGNÉS. Une ligne par partenaire.
     depts : départements couverts, entre guillemets ('69', '42', '2A', '974'...)
     types : types de demandes acceptés parmi 'simulateur' (particuliers), 'copropriete', 'entreprise'
   Exemple :
     { nom: 'Élec Dupont', contact: 'Jean Dupont', email: 'jean@elec-dupont.fr', depts: ['69', '42'], types: ['simulateur', 'copropriete', 'entreprise'] },
*/
var PARTENAIRES = [
];

var d = $input.first().json;
d.partenaires = [];
if (d.type !== 'partenaire' && d.dept) {
  d.partenaires = PARTENAIRES.filter(function (p) {
    return (p.depts || []).map(String).indexOf(d.dept) !== -1 && (!p.types || !p.types.length || p.types.indexOf(d.type) !== -1);
  });
}
return [{ json: d }];
