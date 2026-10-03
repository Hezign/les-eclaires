/* Nœud Code « Normaliser » : reçoit le POST du site, contrôle, et produit un objet demande. */
var b = $input.first().json.body || $input.first().json;
var t = function (v) { return String(v == null ? '' : v).trim().slice(0, 4000); };
var type = t(b.type).toLowerCase();
if (['simulateur', 'copropriete', 'entreprise', 'partenaire'].indexOf(type) === -1) type = '';
var email = t(b.email), tel = t(b.tel), cp = t(b.cp);
var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email);
var telOk = /^(?:\+33|0033|0)[1-9]\d{8}$/.test(tel.replace(/[\s.\-]/g, ''));
var cpOk = type === 'partenaire' ? true : /^\d{5}$/.test(cp);
var robot = b.botcheck === true || b.botcheck === 'true' || b.botcheck === 'on';
/* Département à partir du code postal (Corse : 2A / 2B ; outre-mer : 3 chiffres) */
var DEPTS={"01":"Ain","02":"Aisne","03":"Allier","04":"Alpes-de-Haute-Provence","05":"Hautes-Alpes","06":"Alpes-Maritimes","07":"Ardèche","08":"Ardennes","09":"Ariège","10":"Aube","11":"Aude","12":"Aveyron","13":"Bouches-du-Rhône","14":"Calvados","15":"Cantal","16":"Charente","17":"Charente-Maritime","18":"Cher","19":"Corrèze","2A":"Corse-du-Sud","2B":"Haute-Corse","21":"Côte-d'Or","22":"Côtes-d'Armor","23":"Creuse","24":"Dordogne","25":"Doubs","26":"Drôme","27":"Eure","28":"Eure-et-Loir","29":"Finistère","30":"Gard","31":"Haute-Garonne","32":"Gers","33":"Gironde","34":"Hérault","35":"Ille-et-Vilaine","36":"Indre","37":"Indre-et-Loire","38":"Isère","39":"Jura","40":"Landes","41":"Loir-et-Cher","42":"Loire","43":"Haute-Loire","44":"Loire-Atlantique","45":"Loiret","46":"Lot","47":"Lot-et-Garonne","48":"Lozère","49":"Maine-et-Loire","50":"Manche","51":"Marne","52":"Haute-Marne","53":"Mayenne","54":"Meurthe-et-Moselle","55":"Meuse","56":"Morbihan","57":"Moselle","58":"Nièvre","59":"Nord","60":"Oise","61":"Orne","62":"Pas-de-Calais","63":"Puy-de-Dôme","64":"Pyrénées-Atlantiques","65":"Hautes-Pyrénées","66":"Pyrénées-Orientales","67":"Bas-Rhin","68":"Haut-Rhin","69":"Rhône","70":"Haute-Saône","71":"Saône-et-Loire","72":"Sarthe","73":"Savoie","74":"Haute-Savoie","75":"Paris","76":"Seine-Maritime","77":"Seine-et-Marne","78":"Yvelines","79":"Deux-Sèvres","80":"Somme","81":"Tarn","82":"Tarn-et-Garonne","83":"Var","84":"Vaucluse","85":"Vendée","86":"Vienne","87":"Haute-Vienne","88":"Vosges","89":"Yonne","90":"Territoire de Belfort","91":"Essonne","92":"Hauts-de-Seine","93":"Seine-Saint-Denis","94":"Val-de-Marne","95":"Val-d'Oise","971":"Guadeloupe","972":"Martinique","973":"Guyane","974":"La Réunion","976":"Mayotte"};
var dept='';
if(/^\d{5}$/.test(cp)){
  if(cp.slice(0,2)==='20'){ dept = (cp.slice(0,3)==='200'||cp.slice(0,3)==='201') ? '2A' : '2B'; }
  else if(cp.slice(0,2)==='97'||cp.slice(0,2)==='98'){ dept = cp.slice(0,3); }
  else dept = cp.slice(0,2);
}
var now = new Date();
var date = now.toLocaleDateString('fr-FR', { timeZone: 'Europe/Paris' }) + ' à ' + now.toLocaleTimeString('fr-FR', { timeZone: 'Europe/Paris', hour: '2-digit', minute: '2-digit' });
var champs = Array.isArray(b.champs) ? b.champs.filter(function (c) { return Array.isArray(c) && c.length >= 2; }).slice(0, 20).map(function (c) { return [t(c[0]).slice(0, 80), t(c[1])]; }) : [];
var d = {
  dept: dept, deptNom: DEPTS[dept] || '',
  type: type, valide: !!type && emailOk && telOk && cpOk && !robot, robot: robot,
  prenom: t(b.prenom), nom: t(b.nom), email: email, tel: tel, cp: cp,
  source: t(b.source), consentement: t(b.consentement), date: date,
  profil: t(b.profil).replace(/^Profil\s*:\s*/i, '').replace(/^./, function (c) { return c.toUpperCase(); }),
  synthese: t(b.synthese), puissance: t(b.puissance), budget: t(b.budget), aide: t(b.aide), delai: t(b.delai),
  questionnaire: t(b.questionnaire), champs: champs,
  entreprise: t(b.entreprise), zone: t(b.zone), types: t(b.types), qualification: t(b.qualification), message: t(b.message)
};
return [{ json: d }];
