import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Sondaggio Priorità", layout="centered")

opzioni = ["Ghiaccio", "Alta montagna", "Sci", "Arrampicata"]
csv_file = "risposte.csv"

if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    df = pd.DataFrame(columns=["Nome", "1_scelta", "2_scelta", "3_scelta", "4_scelta", "Timestamp"])

st.title("Sondaggio preferenze")

nome = st.text_input("Nome")

st.write("Compila solo le scelte che vuoi. Le altre possono rimanere vuote.")

col1, col2, col3, col4 = st.columns(4)

prima = col1.selectbox("1ª scelta (obbligatoria)", [""] + opzioni, key="s1")

seconda = col2.selectbox(
    "2ª scelta (facoltativa)",
    [""] + [o for o in opzioni if o != prima],
    key="s2"
)

terza = col3.selectbox(
    "3ª scelta (facoltativa)",
    [""] + [o for o in opzioni if o not in [prima, seconda]],
    key="s3"
)

quarta = col4.selectbox(
    "4ª scelta (facoltativa)",
    [""] + [o for o in opzioni if o not in [prima, seconda, terza]],
    key="s4"
)

if st.button("Invia"):
    if nome.strip() == "":
        st.error("Inserisci il nome.")
        st.stop()

    if prima == "":
        st.error("La prima scelta non può essere vuota.")
        st.stop()

    nuova_riga = {
        "Nome": nome.strip(),
        "1_scelta": prima if prima else "",
        "2_scelta": seconda if seconda else "",
        "3_scelta": terza if terza else "",
        "4_scelta": quarta if quarta else "",
        "Timestamp": datetime.now().isoformat()
    }

    df = pd.concat([df, pd.DataFrame([nuova_riga])], ignore_index=True)
    df.to_csv(csv_file, index=False)
    st.success("Risposta registrata.")

st.subheader("Risposte")
st.dataframe(df)

pesi = {"1_scelta": 4, "2_scelta": 3, "3_scelta": 2, "4_scelta": 1}

punteggi = {o: 0 for o in opzioni}

for _, r in df.iterrows():
    for col, peso in pesi.items():
        scelta = r[col]
        if scelta in punteggi and scelta != "":
            punteggi[scelta] += peso

st.subheader("Punteggi")
st.write(
    pd.DataFrame.from_dict(punteggi, orient="index", columns=["Punti"])
    .sort_values("Punti", ascending=False)
)
