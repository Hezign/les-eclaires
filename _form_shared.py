#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Briques communes aux formulaires de demande (copropriété, entreprise).
Vrai <form>, erreurs visibles sous chaque champ, téléphone + code postal obligatoires,
champ anti-spam, message d'échec dans la page, événement GA4 lead_submit, source du lead."""
import json

CSS = '''<style>
.copro-form .ferr{display:block;font-size:12.5px;line-height:1.4;color:#C0392B;margin-top:6px}
.copro-form .ferr:empty{display:none}
.copro-form [aria-invalid="true"]{border-color:#C0392B;box-shadow:0 0 0 3px rgba(192,57,43,.12)}
.copro-fail{margin:0 0 16px;padding:10px 14px;border-radius:10px;background:rgba(192,57,43,.08);color:#C0392B;font-size:13.5px;line-height:1.5}
html[data-theme="dark"] .copro-form .ferr,html[data-theme="dark"] .copro-fail{color:#FF8A80}
.copro-form .hp{position:absolute;left:-9999px;opacity:0}
</style>'''


def field(fid, label, kind='text', placeholder='', autocomplete='', inputmode='', options=None, extra=''):
    """Un champ avec libellé et emplacement d'erreur. options = liste pour un <select>."""
    ac = f' autocomplete="{autocomplete}"' if autocomplete else ''
    im = f' inputmode="{inputmode}"' if inputmode else ''
    ph = f' placeholder="{placeholder}"' if placeholder else ''
    if options is not None:
        opts = '<option value="" disabled selected>Sélectionnez…</option>' + ''.join(f'<option>{o}</option>' for o in options)
        ctrl = f'<select id="{fid}" aria-describedby="{fid}-err">{opts}</select>'
    elif kind == 'textarea':
        ctrl = f'<textarea id="{fid}"{ph}></textarea>'
    else:
        ctrl = f'<input type="{kind}" id="{fid}"{ph}{ac}{im}{extra} aria-describedby="{fid}-err">'
    return f'<div><label for="{fid}">{label}</label>{ctrl}<span class="ferr" id="{fid}-err" role="alert"></span></div>'


def form_html(rows, legal, arrow):
    """rows = liste de listes de champs (1 ou 2 par ligne)."""
    out = '<div class="copro-form">\n    <form id="cBox" novalidate onsubmit="return false">\n'
    for r in rows:
        inner = ''.join(r) if len(r) > 1 else r[0].replace('<div>', '<div class="full">', 1)
        out += f'      <div class="row">{inner}</div>\n'
    out += ('      <input type="checkbox" class="hp" id="cBot" name="botcheck" tabindex="-1" autocomplete="off" aria-hidden="true">\n'
            '      <p class="copro-fail" id="cFail" role="alert" hidden></p>\n'
            f'      <p class="copro-legal">{legal}</p><button class="btn-vert" id="cSubmit" type="submit">Envoyer ma demande {arrow}</button>\n'
            '    </form>\n'
            '    <div class="copro-ok" id="cOk"><h4>Demande bien reçue !</h4><p>On revient vers vous sous 24 à 48 heures ouvrées.</p></div>\n  </div>')
    return out


def form_js(*, title, subject, from_name, segment, lines, key='1109c206-cadd-4010-a0c1-cf832975b2fa'):
    """lines = [(libellé, id)] repris dans le message, dans l'ordre. Champs contrôlés : cNom, cEmail, cTel, cCP."""
    kind = {'Copropriété': 'copropriete', 'Entreprise': 'entreprise'}[segment]
    cfg = json.dumps({'title': title, 'subject': subject, 'from': from_name, 'segment': segment, 'type': kind,
                      'lines': lines, 'key': key}, ensure_ascii=False)
    return '''<script>
(function(){
  var CFG=''' + cfg + ''';
  function g(id){return document.getElementById(id);}
  function v(id){var e=g(id);return e?(e.value||'').trim():'';}
  /* Envoi principal : n8n (mails en français à la DA). Secours : Web3Forms si n8n ne répond pas. */
  async function leN8n(payload){
    try{
      var c=new AbortController(), to=setTimeout(function(){c.abort();},9000);
      var r=await fetch('https://n8n.srv1212149.hstgr.cloud/webhook/leseclaires-demande',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload),signal:c.signal});
      clearTimeout(to); if(!r.ok) return false;
      var j=await r.json(); return !!(j&&j.success);
    }catch(e){ return false; }
  }
  var RULES={
    cNom:function(x){return x?'':'Indiquez votre nom.';},
    cEmail:function(x){return /^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$/.test(x)?'':'Indiquez une adresse email valide (exemple : nom@domaine.fr).';},
    cTel:function(x){return /^(?:\\+33|0033|0)[1-9]\\d{8}$/.test(x.replace(/[\\s.\\-]/g,''))?'':'Indiquez un numéro de téléphone français valide (10 chiffres).';},
    cCP:function(x){return /^\\d{5}$/.test(x)?'':'Indiquez le code postal du site (5 chiffres).';}
  };
  function check(id){
    var el=g(id), err=g(id+'-err'); if(!el) return true;
    var msg=RULES[id](v(id));
    if(msg){ el.setAttribute('aria-invalid','true'); if(err) err.textContent=msg; return false; }
    el.removeAttribute('aria-invalid'); if(err) err.textContent=''; return true;
  }
  var form=g('cBox'), b=g('cSubmit'); if(!form) return; var sent=false;
  Object.keys(RULES).forEach(function(id){
    var el=g(id); if(!el) return;
    el.addEventListener('input',function(){ if(el.getAttribute('aria-invalid')) check(id); });
  });
  form.addEventListener('submit', async function(ev){
    ev.preventDefault();
    var fail=g('cFail'); if(fail){ fail.hidden=true; fail.textContent=''; }
    var firstBad=null;
    Object.keys(RULES).forEach(function(id){ if(g(id) && !check(id) && !firstBad) firstBad=g(id); });
    if(firstBad){ firstBad.focus(); return; }
    var bot=g('cBot'); if(bot && bot.checked){ form.style.display='none'; g('cOk').classList.add('show'); return; }
    if(sent) return; sent=true; var label=b.innerHTML; b.textContent='Envoi…'; b.disabled=true;
    var nom=v('cNom'), email=v('cEmail');
    var src=(document.referrer||'accès direct')+' | '+location.pathname+location.search;
    var msg=CFG.title+'\\n\\n'+CFG.lines.map(function(l){return l[0]+' : '+(v(l[1])||'(non précisé)');}).join('\\n')+
      '\\nSource : '+src+
      '\\n\\nConsentement : accepte la transmission à un installateur partenaire ('+new Date().toLocaleString('fr-FR')+')';
    try{
      var d={success:await leN8n({type:CFG.type,nom:nom,email:email,tel:v('cTel'),cp:v('cCP'),source:src,
        champs:CFG.lines.map(function(l){return [l[0],v(l[1])];}),
        consentement:'Transmission à un installateur partenaire acceptée ('+new Date().toLocaleString('fr-FR')+', page '+location.pathname+')'})};
      if(!d.success){
      var r=await fetch('https://api.web3forms.com/submit',{method:'POST',
        headers:{'Content-Type':'application/json',Accept:'application/json'},
        body:JSON.stringify({access_key:CFG.key,subject:CFG.subject+' - '+nom+' ('+v('cCP')+')',from_name:CFG.from,
          name:nom,email:email,replyto:email,'Téléphone':v('cTel'),'Code postal':v('cCP'),'Source':src,botcheck:'',message:msg})});
      d=await r.json();
      }
      if(d&&d.success){
        if(window.gtag)gtag('event','lead_submit',{profil:CFG.segment,segment:CFG.segment});
        form.style.display='none'; g('cOk').classList.add('show');
      } else throw new Error('w3f');
    }catch(e){ sent=false; b.disabled=false; b.innerHTML=label;
      if(fail){ fail.textContent="L'envoi n'a pas abouti. Vérifiez votre connexion et réessayez, ou écrivez-nous à contact@leseclaires.fr."; fail.hidden=false; fail.scrollIntoView({block:'center'}); }
    }
  });
})();
</script>'''
