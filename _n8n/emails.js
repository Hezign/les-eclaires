/* Mails Les Éclairés (français, DA officielle). Source unique : ce fichier est recopié tel quel
   dans le nœud Code « Construire les mails » du workflow n8n « Les Éclairés - Demandes ».
   Compatible clients mail : tableaux, styles en ligne, polices avec repli, logo PNG hébergé. */
var SITE = 'https://leseclaires.fr';
var C = { vert: '#00F5A0', vertTxt: '#007A50', noir: '#000000', gris: '#5C6560', page: '#F4F6F5', menthe: '#E6FFF5', mentheBr: '#C2F5DF', ligne: '#E3E8E5' };
var FH = "'Schibsted Grotesk','Helvetica Neue',Helvetica,Arial,sans-serif";
var FB = "'Manrope','Helvetica Neue',Helvetica,Arial,sans-serif";
var FM = "'JetBrains Mono','SFMono-Regular',Consolas,monospace";

function esc(v) { return String(v == null ? '' : v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
function nl(v) { return esc(v).replace(/\n/g, '<br>'); }
function has(v) { return String(v == null ? '' : v).trim() !== ''; }

function layout(o) {
  /* o = {preheader, tag, title, intro, blocks (html), footer (html)} */
  return '<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
    + '<meta name="color-scheme" content="light only"><meta name="supported-color-schemes" content="light only">'
    + '<link href="https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@700;800&family=Manrope:wght@400;600&display=swap" rel="stylesheet">'
    + '<title>' + esc(o.title) + '</title></head>'
    + '<body style="margin:0;padding:0;background:' + C.page + ';">'
    + '<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:' + C.page + ';">' + esc(o.preheader || '') + '</div>'
    + '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:' + C.page + ';"><tr><td align="center" style="padding:28px 12px;">'
    + '<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background:#FFFFFF;border-radius:20px;overflow:hidden;border:1px solid ' + C.ligne + ';">'
    /* en-tête : logo officiel sur fond blanc */
    + '<tr><td style="padding:26px 32px 22px;border-bottom:3px solid ' + C.vert + ';">'
    + '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>'
    + '<td align="left"><a href="' + SITE + '" style="text-decoration:none;"><img src="' + SITE + '/logo-eclaires-horizontal.png" width="176" height="27" alt="Les Éclairés" style="display:block;border:0;width:176px;height:auto;"></a></td>'
    + (o.tag ? '<td align="right" style="font-family:' + FM + ';font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:' + C.vertTxt + ';">' + esc(o.tag) + '</td>' : '')
    + '</tr></table></td></tr>'
    /* corps */
    + '<tr><td style="padding:32px 32px 8px;">'
    + '<h1 style="margin:0 0 12px;font-family:' + FH + ';font-size:26px;line-height:1.2;font-weight:800;letter-spacing:-.02em;color:' + C.noir + ';">' + o.title + '</h1>'
    + (o.intro ? '<p style="margin:0 0 8px;font-family:' + FB + ';font-size:16px;line-height:1.65;color:' + C.gris + ';">' + o.intro + '</p>' : '')
    + '</td></tr>'
    + '<tr><td style="padding:8px 32px 30px;">' + o.blocks + '</td></tr>'
    + '<tr><td style="padding:20px 32px 26px;background:' + C.page + ';border-top:1px solid ' + C.ligne + ';font-family:' + FB + ';font-size:12.5px;line-height:1.6;color:' + C.gris + ';">' + o.footer + '</td></tr>'
    + '</table></td></tr></table></body></html>';
}

function card(title, rows) {
  var tr = rows.filter(function (r) { return has(r[1]); }).map(function (r) {
    return '<tr><td style="padding:7px 16px 7px 0;font-family:' + FB + ';font-size:14px;color:' + C.gris + ';vertical-align:top;white-space:nowrap;">' + esc(r[0]) + '</td>'
      + '<td style="padding:7px 0;font-family:' + FB + ';font-size:15px;font-weight:600;color:' + C.noir + ';vertical-align:top;">' + (r[2] ? r[1] : nl(r[1])) + '</td></tr>';
  }).join('');
  if (!tr) return '';
  return '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:16px 0 0;background:' + C.menthe + ';border:1px solid ' + C.mentheBr + ';border-radius:16px;"><tr><td style="padding:18px 20px;">'
    + '<div style="font-family:' + FM + ';font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:' + C.vertTxt + ';margin-bottom:6px;">' + esc(title) + '</div>'
    + '<table role="presentation" cellpadding="0" cellspacing="0" border="0">' + tr + '</table></td></tr></table>';
}

function steps(title, items) {
  var li = items.map(function (t, i) {
    return '<tr><td style="padding:8px 14px 8px 0;vertical-align:top;"><div style="width:26px;height:26px;border-radius:13px;background:' + C.noir + ';color:' + C.vert + ';font-family:' + FH + ';font-size:13px;font-weight:700;line-height:26px;text-align:center;">' + (i + 1) + '</div></td>'
      + '<td style="padding:8px 0;font-family:' + FB + ';font-size:15px;line-height:1.6;color:' + C.noir + ';vertical-align:top;">' + t + '</td></tr>';
  }).join('');
  return '<div style="margin:26px 0 0;font-family:' + FH + ';font-size:17px;font-weight:700;color:' + C.noir + ';">' + esc(title) + '</div>'
    + '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin-top:6px;">' + li + '</table>';
}

function button(label, href) {
  return '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:26px 0 0;"><tr><td style="border-radius:999px;background:' + C.vert + ';">'
    + '<a href="' + href + '" style="display:inline-block;padding:13px 26px;font-family:' + FH + ';font-size:15px;font-weight:700;color:' + C.noir + ';text-decoration:none;border-radius:999px;">' + esc(label) + '</a></td></tr></table>';
}

function para(html) { return '<p style="margin:18px 0 0;font-family:' + FB + ';font-size:15px;line-height:1.65;color:' + C.gris + ';">' + html + '</p>'; }
function pre(text) { return '<div style="margin:10px 0 0;padding:16px 18px;background:' + C.page + ';border:1px solid ' + C.ligne + ';border-radius:14px;font-family:' + FB + ';font-size:14px;line-height:1.6;color:' + C.noir + ';">' + nl(text) + '</div>'; }
function h2(t) { return '<div style="margin:26px 0 0;font-family:' + FH + ';font-size:17px;font-weight:700;color:' + C.noir + ';">' + esc(t) + '</div>'; }
function link(href, label) { return '<a href="' + href + '" style="color:' + C.vertTxt + ';text-decoration:underline;">' + esc(label) + '</a>'; }

var LIB = { simulateur: 'Simulateur', copropriete: 'Copropriété', entreprise: 'Entreprise', partenaire: 'Candidature installateur' };
var FOOT_CLIENT = 'Vous recevez ce message parce que vous avez fait une demande sur ' + link(SITE, 'leseclaires.fr') + '. Une question ? Répondez simplement à ce mail.<br>'
  + link(SITE + '/confidentialite.html', 'Confidentialité') + ' · ' + link(SITE + '/cgu.html', "Conditions d'utilisation") + ' · ' + link(SITE + '/mentions-legales.html', 'Mentions légales');

/* ---------- Confirmation envoyée au client ---------- */
function mailClient(d) {
  var prenom = has(d.prenom) ? d.prenom : (has(d.nom) ? String(d.nom).split(' ')[0] : '');
  var cible = d.type === 'copropriete' ? 'habitué aux copropriétés' : (d.type === 'entreprise' ? 'habitué aux sites professionnels' : 'proche de chez vous');
  var recap;
  if (d.type === 'simulateur') {
    recap = card('Votre simulation', [['Profil', d.profil], ['Puissance conseillée', d.puissance], ['Budget estimé', d.budget], ['Aide mobilisable', d.aide], ['Délai estimé', d.delai], ['Code postal', d.cp]])
      + para('Ces estimations sont indicatives. Le devis de l\'installateur, établi après examen de votre installation, fait foi.');
  } else {
    recap = card('Votre demande', (d.champs || []).filter(function (c) { return ['Email', 'Téléphone', 'Nom'].indexOf(c[0]) === -1; }));
  }
  var blocks = recap
    + steps('La suite', [
      'Nous sélectionnons un installateur <strong>certifié IRVE</strong> ' + cible + '.',
      'Il vous rappelle sous <strong>48 heures ouvrées</strong> pour préciser votre projet et établir un devis gratuit.',
      'Vous décidez librement. Aucun engagement de votre part.'
    ])
    + para('Le service est gratuit pour vous : Les Éclairés est rémunéré par l\'installateur. Vos coordonnées ne sont transmises qu\'à <strong style="color:' + C.noir + ';">un seul installateur</strong>.')
    + button('Lire nos guides', SITE + '/blog/')
    + para('À très vite,<br><strong style="color:' + C.noir + ';">L\'équipe Les Éclairés</strong>');
  return {
    subject: 'Votre demande est bien reçue - Les Éclairés',
    html: layout({
      preheader: 'Un installateur certifié IRVE vous rappelle sous 48 heures ouvrées.',
      tag: 'Demande reçue',
      title: (prenom ? esc(prenom) + ', votre ' : 'Votre ') + 'demande est bien reçue.',
      intro: 'Merci pour votre confiance. Voici le récapitulatif de votre demande et ce qui va se passer.',
      blocks: blocks, footer: FOOT_CLIENT
    })
  };
}

/* Bloc « à qui transmettre » : partenaire signé dans le département, ou à recruter */
function blocPartenaire(d) {
  var lieu = d.dept ? d.dept + (has(d.deptNom) ? ' (' + esc(d.deptNom) + ')' : '') : 'ce secteur';
  var liste = d.partenaires || [];
  if (liste.length) {
    var rows = liste.map(function (p) {
      return '<tr><td style="padding:6px 0;font-family:' + FB + ';font-size:15px;color:' + C.noir + ';"><strong>' + esc(p.nom) + '</strong>'
        + (has(p.contact) ? ' · ' + esc(p.contact) : '')
        + (has(p.email) ? ' · <a href="mailto:' + esc(p.email) + '" style="color:' + C.vertTxt + ';">' + esc(p.email) + '</a>' : '') + '</td></tr>';
    }).join('');
    return '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:16px 0 0;background:' + C.noir + ';border-radius:16px;"><tr><td style="padding:18px 20px;">'
      + '<div style="font-family:' + FM + ';font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:' + C.vert + ';margin-bottom:6px;">À transmettre · partenaire dans le ' + lieu + '</div>'
      + '<table role="presentation" cellpadding="0" cellspacing="0" border="0">' + rows.replace(new RegExp(C.noir, 'g'), '#FFFFFF').replace(new RegExp(C.vertTxt, 'g'), C.vert) + '</table></td></tr></table>';
  }
  return '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:16px 0 0;background:#FFFFFF;border:2px solid ' + C.noir + ';border-radius:16px;"><tr><td style="padding:16px 20px;">'
    + '<div style="font-family:' + FM + ';font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:' + C.noir + ';margin-bottom:6px;">À recruter · aucun partenaire dans le ' + lieu + '</div>'
    + '<div style="font-family:' + FB + ';font-size:15px;line-height:1.55;color:' + C.gris + ';">Contactez des installateurs certifiés IRVE du ' + lieu + ' avec cette demande concrète. Dans Kalend, filtrez les installateurs sur ce département.</div></td></tr></table>';
}

/* ---------- Notification interne (demande client) ---------- */
function mailInterne(d) {
  var qui = has(d.prenom) ? d.prenom : d.nom;
  var contact = card('Contact', [
    [d.type === 'simulateur' ? 'Prénom' : 'Nom', qui],
    ['Email', '<a href="mailto:' + esc(d.email) + '" style="color:' + C.vertTxt + ';">' + esc(d.email) + '</a>', true],
    ['Téléphone', '<a href="tel:' + esc(String(d.tel).replace(/[^\d+]/g, '')) + '" style="color:' + C.vertTxt + ';">' + esc(d.tel) + '</a>', true],
    ['Code postal', d.cp]
  ]);
  var corps = '';
  if (d.type === 'simulateur') {
    corps += card('Recommandation', [['Profil', d.profil], ['Puissance', d.puissance], ['Budget estimé', d.budget], ['Aide', d.aide], ['Délai', d.delai]]);
    if (has(d.synthese)) corps += para(esc(d.synthese));
    if (has(d.questionnaire)) corps += h2('Réponses au questionnaire') + pre(d.questionnaire);
  } else {
    corps += card('Projet', (d.champs || []).filter(function (c) { return ['Email', 'Téléphone', 'Nom', 'Code postal'].indexOf(c[0]) === -1; }));
  }
  var blocks = blocPartenaire(d) + contact + corps
    + button('Répondre à ' + (qui || 'ce contact'), 'mailto:' + esc(d.email) + '?subject=' + encodeURIComponent('Votre projet de borne de recharge - Les Éclairés'))
    + para('<span style="font-size:13px;">Origine : ' + esc(d.source || 'non précisée') + '<br>Consentement : ' + esc(d.consentement || 'transmission à un installateur partenaire acceptée') + '</span>');
  return {
    subject: 'Nouvelle demande ' + LIB[d.type].toLowerCase() + ' - ' + (qui || '') + (has(d.cp) ? ' (' + d.cp + ')' : '')
      + ((d.partenaires || []).length ? ' · partenaire : ' + d.partenaires[0].nom : ' · à recruter'),
    html: layout({
      preheader: (d.profil || LIB[d.type]) + (has(d.cp) ? ' · ' + d.cp : ''),
      tag: 'Nouvelle demande · ' + LIB[d.type],
      title: esc(qui || 'Nouvelle demande') + (has(d.cp) ? ' <span style="color:' + C.gris + ';font-weight:700;">· ' + esc(d.cp) + '</span>' : ''),
      intro: 'Reçue le ' + esc(d.date) + '. Un installateur doit rappeler ce contact sous 48 heures ouvrées.',
      blocks: blocks,
      footer: 'Demande reçue via ' + link(SITE, 'leseclaires.fr') + '. Mail interne, à ne pas transférer au client.'
    })
  };
}

/* ---------- Candidature installateur ---------- */
function mailPartenaire(d) {
  var blocks = card('Votre candidature', [['Entreprise', d.entreprise], ['Zone d\'intervention', d.zone], ['Types de projets', d.types], ['Qualification IRVE', d.qualification]])
    + steps('La suite', [
      'Nous étudions votre candidature : qualification IRVE, zone et types de projets.',
      'Nous vous recontactons sous <strong>48 heures ouvrées</strong> pour un premier échange et vous présenter le fonctionnement.',
      'Si nous avançons ensemble, vous recevez le contrat partenaire à signer.'
    ])
    + para('Le principe : chaque demande est transmise à <strong style="color:' + C.noir + ';">un seul installateur</strong>. Vous ne payez que les demandes reçues, sans abonnement.')
    + button('Revoir le fonctionnement', SITE + '/partenaires.html')
    + para('À très vite,<br><strong style="color:' + C.noir + ';">L\'équipe Les Éclairés</strong>');
  return {
    subject: 'Votre candidature est bien reçue - Les Éclairés',
    html: layout({
      preheader: 'Nous revenons vers vous sous 48 heures ouvrées.',
      tag: 'Candidature reçue',
      title: (has(d.prenom) ? esc(d.prenom) + ', votre ' : 'Votre ') + 'candidature est bien reçue.',
      intro: 'Merci de votre intérêt pour le réseau d\'installateurs Les Éclairés.',
      blocks: blocks,
      footer: 'Vous recevez ce message parce que vous avez candidaté sur ' + link(SITE + '/partenaires.html', 'leseclaires.fr') + '. Une question ? Répondez simplement à ce mail.<br>' + link(SITE + '/confidentialite.html', 'Confidentialité') + ' · ' + link(SITE + '/mentions-legales.html', 'Mentions légales')
    })
  };
}

function mailInternePartenaire(d) {
  var nom = [d.prenom, d.nom].filter(has).join(' ');
  var blocks = card('Contact', [
    ['Nom', nom], ['Entreprise', d.entreprise],
    ['Email', '<a href="mailto:' + esc(d.email) + '" style="color:' + C.vertTxt + ';">' + esc(d.email) + '</a>', true],
    ['Téléphone', '<a href="tel:' + esc(String(d.tel).replace(/[^\d+]/g, '')) + '" style="color:' + C.vertTxt + ';">' + esc(d.tel) + '</a>', true]
  ])
    + card('Activité', [['Zone d\'intervention', d.zone], ['Types de projets', d.types], ['Qualification IRVE', d.qualification]])
    + (has(d.message) ? h2('Message') + pre(d.message) : '')
    + button('Répondre à ' + (d.prenom || nom || 'ce contact'), 'mailto:' + esc(d.email) + '?subject=' + encodeURIComponent('Votre candidature au réseau Les Éclairés'))
    + para('<span style="font-size:13px;">Origine : ' + esc(d.source || 'non précisée') + '</span>');
  return {
    subject: 'Candidature installateur - ' + (d.entreprise || nom) + (has(d.zone) ? ' (' + d.zone + ')' : ''),
    html: layout({
      preheader: (d.entreprise || '') + ' · ' + (d.zone || ''),
      tag: 'Candidature installateur',
      title: esc(d.entreprise || nom || 'Nouvelle candidature'),
      intro: 'Reçue le ' + esc(d.date) + '. À recontacter sous 48 heures ouvrées.',
      blocks: blocks,
      footer: 'Candidature reçue via ' + link(SITE + '/partenaires.html', 'leseclaires.fr') + '. Mail interne.'
    })
  };
}

function construire(d) {
  if (d.type === 'partenaire') return { interne: mailInternePartenaire(d), client: mailPartenaire(d) };
  return { interne: mailInterne(d), client: mailClient(d) };
}
if (typeof module !== 'undefined') module.exports = { construire: construire };
