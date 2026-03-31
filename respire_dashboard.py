"""Streamlit wrapper for the provided Respire pharmacy workflow mockup."""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Respire · Parcours pharmacie", layout="wide")
st.title("Respire · Parcours de commande officine")

HTML = r'''
<style>
*{box-sizing:border-box;margin:0;padding:0;}
body{font-family:var(--font-sans);color:var(--color-text-primary);font-size:13px;}
.app{padding:16px 0;}
.steps{display:flex;gap:0;margin-bottom:24px;border-bottom:1px solid var(--color-border-tertiary);}
.step-tab{padding:10px 16px;font-size:12px;font-weight:500;color:var(--color-text-secondary);cursor:pointer;border-bottom:2px solid transparent;transition:all .15s;white-space:nowrap;}
.step-tab.active{color:var(--color-text-primary);border-bottom:2px solid var(--color-text-primary);}
.step-tab:hover:not(.active){color:var(--color-text-primary);}
.panel{display:none;} .panel.active{display:block;}
.section-title{font-size:11px;font-weight:500;color:var(--color-text-secondary);text-transform:uppercase;letter-spacing:.05em;margin-bottom:12px;margin-top:20px;}
.section-title:first-child{margin-top:0;}
.grid2{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;}
.grid3{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;}
.grid4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;}
.card{background:var(--color-background-secondary);border-radius:var(--border-radius-lg);padding:14px;}
.card-white{background:var(--color-background-primary);border:0.5px solid var(--color-border-tertiary);border-radius:var(--border-radius-lg);padding:14px;}
.label{font-size:11px;color:var(--color-text-secondary);margin-bottom:4px;}
.value{font-size:15px;font-weight:500;}
.value-sm{font-size:13px;font-weight:500;}
.badge{display:inline-block;padding:2px 8px;border-radius:8px;font-size:10px;font-weight:500;}
.b-green{background:#EAF3DE;color:#27500A;} .b-blue{background:#E6F1FB;color:#0C447C;}
.b-amber{background:#FAEEDA;color:#633806;} .b-red{background:#FCEBEB;color:#791F1F;}
.b-teal{background:#E1F5EE;color:#085041;} .b-gray{background:#F1EFE8;color:#444441;}
@media(prefers-color-scheme:dark){
  .b-green{background:#27500A;color:#C0DD97;} .b-blue{background:#0C447C;color:#B5D4F4;}
  .b-amber{background:#633806;color:#FAC775;} .b-red{background:#791F1F;color:#F7C1C1;}
  .b-teal{background:#085041;color:#9FE1CB;} .b-gray{background:#444441;color:#D3D1C7;}
}
.form-row{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-bottom:10px;}
.form-group{display:flex;flex-direction:column;gap:4px;}
.form-group label{font-size:11px;color:var(--color-text-secondary);font-weight:500;}
select,input[type=text],input[type=number]{width:100%;padding:8px 10px;font-size:12px;border:0.5px solid var(--color-border-secondary);border-radius:var(--border-radius-md);background:var(--color-background-primary);color:var(--color-text-primary);}
.radio-group{display:flex;gap:6px;flex-wrap:wrap;}
.radio-opt{padding:5px 10px;border:0.5px solid var(--color-border-secondary);border-radius:var(--border-radius-md);font-size:11px;cursor:pointer;transition:all .1s;background:var(--color-background-primary);}
.radio-opt.selected{background:var(--color-text-primary);color:var(--color-background-primary);border-color:var(--color-text-primary);}
.btn{padding:8px 16px;border:0.5px solid var(--color-border-secondary);border-radius:var(--border-radius-md);background:var(--color-background-primary);color:var(--color-text-primary);font-size:12px;cursor:pointer;font-weight:500;}
.btn-primary{background:var(--color-text-primary);color:var(--color-background-primary);border-color:var(--color-text-primary);}
.btn:hover{background:var(--color-background-secondary);}
.btn-primary:hover{opacity:.85;}
.prod-card{background:var(--color-background-primary);border:0.5px solid var(--color-border-tertiary);border-radius:var(--border-radius-lg);padding:12px;}
.prod-card.featured{border:1.5px solid #1D9E75;}
.prod-name{font-weight:500;font-size:12px;margin-bottom:4px;}
.prod-desc{font-size:11px;color:var(--color-text-secondary);margin-bottom:6px;line-height:1.4;}
.prod-row{display:flex;justify-content:space-between;align-items:center;margin-top:6px;}
.prod-price{font-weight:500;font-size:12px;}
.qty-ctrl{display:flex;align-items:center;gap:6px;}
.qty-btn{width:22px;height:22px;border:0.5px solid var(--color-border-secondary);border-radius:4px;background:var(--color-background-secondary);cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center;color:var(--color-text-primary);line-height:1;}
.qty-val{font-size:12px;font-weight:500;min-width:16px;text-align:center;}
.divider{height:1px;background:var(--color-border-tertiary);margin:16px 0;}
.promo-card{border:0.5px solid var(--color-border-secondary);border-radius:var(--border-radius-lg);padding:12px;margin-bottom:8px;cursor:pointer;transition:border .1s;}
.promo-card.selected{border:1.5px solid #1D9E75;}
.promo-title{font-weight:500;font-size:12px;margin-bottom:2px;}
.promo-desc{font-size:11px;color:var(--color-text-secondary);}
.kpi-bar{display:flex;align-items:center;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--color-border-tertiary);}
.kpi-bar:last-child{border-bottom:none;}
.kpi-name{font-size:12px;}
.kpi-val{font-weight:500;font-size:12px;}
.progress-wrap{background:var(--color-background-secondary);border-radius:4px;height:6px;flex:1;margin:0 10px;}
.progress-fill{height:6px;border-radius:4px;background:#1D9E75;transition:width .3s;}
.cart-summary{background:var(--color-background-secondary);border-radius:var(--border-radius-lg);padding:14px;margin-top:16px;}
.cart-row{display:flex;justify-content:space-between;font-size:12px;margin-bottom:6px;}
.cart-row.total{font-weight:500;font-size:13px;padding-top:8px;border-top:1px solid var(--color-border-secondary);margin-top:4px;}
.tag-list{display:flex;flex-wrap:wrap;gap:5px;margin-top:6px;}
</style>

<div class="app"><div class="steps">
  <div class="step-tab active" onclick="showPanel(0)">1 · Inscription</div>
  <div class="step-tab" onclick="showPanel(1)">2 · Recommandation</div>
  <div class="step-tab" onclick="showPanel(2)">3 · Paiement & remises</div>
  <div class="step-tab" onclick="showPanel(3)">4 · Suivi & réassort</div>
</div>
<div class="panel active" id="p0"><p class="section-title">Profil établissement</p><div class="form-row"><div class="form-group"><label>N° FINESS officine</label><input type="text" placeholder="Ex : 750123456" id="finess"></div><div class="form-group"><label>N° RPPS titulaire</label><input type="text" placeholder="Ex : 10003456789"></div></div><div style="margin-top:16px;display:flex;justify-content:flex-end;"><button class="btn btn-primary" onclick="showPanel(1)">Obtenir ma recommandation →</button></div></div>
<div class="panel" id="p1"><div class="grid4" style="margin-bottom:20px;"><div class="card"><div class="label">Pack recommandé</div><div class="value-sm">Essentiel Départ</div></div><div class="card"><div class="label">Nb de références</div><div class="value">12</div></div><div class="card"><div class="label">Investissement initial</div><div class="value">540 €</div></div><div class="card"><div class="label">CA potentiel / an</div><div class="value" style="color:#3B6D11;">+2 100 €</div></div></div><div style="margin-top:12px;display:flex;justify-content:flex-end;"><button class="btn btn-primary" onclick="showPanel(2)">Choisir mon option de paiement →</button></div></div>
<div class="panel" id="p2"><p class="section-title">Fréquence de paiement</p><div class="grid3"><div class="promo-card" onclick="selectPromo(this,'freq')"><div class="promo-title">Paiement annuel</div></div><div class="promo-card selected" onclick="selectPromo(this,'freq')"><div class="promo-title">Paiement trimestriel</div></div><div class="promo-card" onclick="selectPromo(this,'freq')"><div class="promo-title">Paiement mensuel</div></div></div><div style="margin-top:12px;display:flex;justify-content:flex-end;"><button class="btn btn-primary" onclick="showPanel(3)">Valider & suivre ma commande →</button></div></div>
<div class="panel" id="p3"><div class="grid4" style="margin-bottom:20px;"><div class="card"><div class="label">CA généré (3 mois)</div><div class="value" style="color:#3B6D11;">+612 €</div></div><div class="card"><div class="label">Unités vendues</div><div class="value">38</div></div><div class="card"><div class="label">Taux de rotation stock</div><div class="value">68 %</div></div><div class="card"><div class="label">Score engagement</div><div class="value" style="color:#185FA5;">Bon</div></div></div></div></div>

<script>
function showPanel(i){document.querySelectorAll('.panel').forEach((p,idx)=>p.classList.toggle('active',idx===i));document.querySelectorAll('.step-tab').forEach((t,idx)=>t.classList.toggle('active',idx===i));}
function selectPromo(card,grp){card.classList.toggle('selected');}
</script>
'''

components.html(HTML, height=1200, scrolling=True)
