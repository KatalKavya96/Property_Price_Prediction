import streamlit as st

def inject_styles():
    """Injects the full CSS styling for the app."""
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
}

/* ✅ Add global page padding so nothing hugs edges */
div.block-container{
  padding-top: 1.4rem !important;
  padding-bottom: 2.0rem !important;
}

/* ✅ Simple reusable spacer */
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
  margin-bottom: 16px; /* ✅ space under navbar */
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
  margin-bottom: 14px; /* ✅ prevents “card-on-card” touching */
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

.table-wrap{
  border: 1px solid var(--border);
  background: var(--panel2);
  border-radius: 14px;
  overflow:hidden;
  margin-top: 10px;      /* ✅ spacing above table */
  margin-bottom: 14px;   /* ✅ spacing below table */
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

/* Streamlit widget polish */
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
</style>
""",
        unsafe_allow_html=True,
    )
