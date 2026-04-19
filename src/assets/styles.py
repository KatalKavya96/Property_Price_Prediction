import streamlit as st


def inject_styles():
    st.markdown(
        """
<style>
:root{
  --bg:#070a12;
  --panel:rgba(255,255,255,.03);
  --panel2:rgba(255,255,255,.02);
  --border:rgba(255,255,255,.08);
  --muted:rgba(255,255,255,.62);
  --text:rgba(255,255,255,.92);
  --pill:rgba(255,255,255,.06);
  --blue:#3b82f6;
  --green:#22c55e;
  --amber:#f59e0b;
}

div.block-container{
  padding-top: 1.4rem !important;
  padding-bottom: 2rem !important;
}

.vspace{ height: 14px; }

.stApp{
  background:
    radial-gradient(900px 500px at 15% 15%, rgba(59,130,246,.10), transparent 55%),
    radial-gradient(700px 450px at 85% 25%, rgba(34,197,94,.08), transparent 55%),
    linear-gradient(180deg, var(--bg) 0%, #05060c 100%);
  color: var(--text);
}

header, footer, #MainMenu { visibility:hidden; }

.container { max-width: 1400px; margin: 0 auto; }

.navbar{
  display:flex; align-items:center; justify-content:space-between;
  gap:16px;
  padding: 12px 14px;
  border: 1px solid var(--border);
  background: var(--panel);
  border-radius: 14px;
  box-shadow: 0 18px 55px rgba(0,0,0,.35);
  margin-bottom: 16px;
}

.brand{
  display:flex; align-items:center; gap:10px;
  font-weight:850; letter-spacing:-0.02em;
}

.brand-dot{
  width:10px; height:10px; border-radius:999px;
  background: linear-gradient(135deg, var(--blue), var(--green));
  box-shadow: 0 0 0 6px rgba(59,130,246,.08);
}

.card{
  border: 1px solid var(--border);
  background: var(--panel);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 18px 55px rgba(0,0,0,.32);
  margin-bottom: 14px;
}

.h1{
  font-size: 26px;
  font-weight: 900;
  letter-spacing: -0.03em;
  margin: 0;
}

.sub{
  color: var(--muted);
  font-size: 13px;
  margin-top: 6px;
}

.big-number{
  font-size: 54px;
  font-weight: 950;
  letter-spacing: -0.03em;
  margin: 10px 0 0 0;
}

.section-title{
  font-size: 18px;
  font-weight: 800;
  letter-spacing: -0.02em;
  margin-bottom: 10px;
}

.section-body{
  color: rgba(255,255,255,.86);
  font-size: 14px;
  line-height: 1.65;
}

.advisory-hero{
  background:
    radial-gradient(550px 220px at 10% 10%, rgba(59,130,246,.10), transparent 60%),
    radial-gradient(450px 180px at 90% 20%, rgba(34,197,94,.09), transparent 60%),
    var(--panel);
}

.advisory-card{
  min-height: 210px;
}

.evidence-card{
  background:
    linear-gradient(180deg, rgba(255,255,255,.04), rgba(255,255,255,.02));
}

.evidence-grid{
  display:grid;
  grid-template-columns: repeat(1, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 14px;
}

.evidence-pill{
  border:1px solid rgba(255,255,255,.08);
  background:rgba(255,255,255,.03);
  border-radius:14px;
  padding:12px 14px;
}

.evidence-label{
  font-size:12px;
  color:var(--muted);
  margin-bottom:4px;
}

.evidence-value{
  font-size:24px;
  font-weight:800;
  letter-spacing:-0.02em;
}

.evidence-subtitle{
  font-size:13px;
  color:var(--muted);
  margin: 10px 0 8px 0;
  font-weight:700;
  text-transform: uppercase;
  letter-spacing:.04em;
}

.evidence-list{
  margin: 0 0 0 18px;
  color: rgba(255,255,255,.86);
  line-height: 1.6;
}

.table-wrap{
  border: 1px solid var(--border);
  background: var(--panel2);
  border-radius: 14px;
  overflow:hidden;
  margin-top: 10px;
  margin-bottom: 14px;
}

.table-header{
  display:flex; align-items:center; justify-content:space-between;
  padding: 12px 14px;
  background: var(--panel);
  border-bottom: 1px solid var(--border);
}

.table-title{
  font-weight:900; letter-spacing:-0.02em;
}

hr.sep{
  border:0; height:1px; background: rgba(255,255,255,.08);
  margin: 14px 0;
}

div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input{
  background: rgba(255,255,255,.03) !important;
  border: 1px solid var(--border) !important;
  color: rgba(255,255,255,.85) !important;
  border-radius: 10px !important;
}

div[data-testid="stSlider"] > div{
  padding-top: 6px;
}

div.stButton > button{
  width:100%;
  border-radius: 12px !important;
  height: 44px;
  border: 1px solid rgba(255,255,255,.10) !important;
  background: rgba(255,255,255,.07) !important;
  color: rgba(255,255,255,.92) !important;
  font-weight: 900 !important;
}

div.stButton > button:hover{
  background: rgba(255,255,255,.10) !important;
  transform: translateY(-1px);
}

div[data-testid="stProgress"] > div > div{
  background: linear-gradient(90deg, var(--blue), var(--green)) !important;
}

@media (max-width: 900px){
  .big-number{
    font-size: 40px;
  }
  .advisory-card{
    min-height: auto;
  }
}
</style>
""",
        unsafe_allow_html=True,
    )