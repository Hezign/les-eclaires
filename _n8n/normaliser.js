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
var now = new Date();
var date = now.toLocaleDateString('fr-FR', { timeZone: 'Europe/Paris' }) + ' à ' + now.toLocaleTimeString('fr-FR', { timeZone: 'Europe/Paris', hour: '2-digit', minute: '2-digit' });
var champs = Array.isArray(b.champs) ? b.champs.filter(function (c) { return Array.isArray(c) && c.length >= 2; }).slice(0, 20).map(function (c) { return [t(c[0]).slice(0, 80), t(c[1])]; }) : [];
var d = {
  type: type, valide: !!type && emailOk && telOk && cpOk && !robot, robot: robot,
  prenom: t(b.prenom), nom: t(b.nom), email: email, tel: tel, cp: cp,
  source: t(b.source), consentement: t(b.consentement), date: date,
  profil: t(b.profil).replace(/^Profil\s*:\s*/i, '').replace(/^./, function (c) { return c.toUpperCase(); }),
  synthese: t(b.synthese), puissance: t(b.puissance), budget: t(b.budget), aide: t(b.aide), delai: t(b.delai),
  questionnaire: t(b.questionnaire), champs: champs,
  entreprise: t(b.entreprise), zone: t(b.zone), types: t(b.types), qualification: t(b.qualification), message: t(b.message)
};
return [{ json: d }];
