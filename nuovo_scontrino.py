from datetime import date, timedelta

import pandas as pd
import streamlit as st

from funzioni.clienti import clienti
from funzioni.scontrini import scontrini


def nuova_riga(i):
    col1, col2, col3, col4 = st.columns([2, 2, 3, 1])

    if i == min(st.session_state["lista_righe"]):
        with col1:
            st.write("Quantità")

        with col2:
            st.write("Capo")

        with col3:
            st.write("Commento")

        with col4:
            st.write("Elimina")

    with col1:
        quantità = st.number_input(
            "Quantità",
            min_value=1,
            step=1,
            key="ns_quantità_" + str(i),
            label_visibility="collapsed",
        )

    with col2:
        capo = st.selectbox(
            "Seleziona il capo",
            Capi["capo"].values,
            index=None,
            placeholder="nome capo",
            key="ns_capo_" + str(i),
            label_visibility="collapsed",
        )

    with col3:
        commento = st.text_input(
            "Commento", key="ns_commento_" + str(i), label_visibility="collapsed"
        )

    with col4:
        if st.button(":red[X]", key="ns_cancella_" + str(i), help="cancella la riga"):
            if len(st.session_state["lista_righe"]) > 1:
                cancella_riga(i)

    if max(st.session_state["lista_righe"]) == i:
        if st.button("**:green[+ NUOVA RIGA]**", use_container_width=True):
            if capo and commento:
                st.session_state["lista_righe"].append(i + 1)
                st.rerun()

        col1, col2 = st.columns(2)
        with col1:
            if st.button("**:red[CANCELLA TUTTO]**", use_container_width=True):
                resetta_pagina()
        with col2:
            if st.button("**:orange[SALVA E STAMPA]**", use_container_width=True):
                salva_stampa_scontrino()


def cancella_riga(i):
    del st.session_state["ns_cancella_" + str(i)]
    del st.session_state["ns_commento_" + str(i)]
    del st.session_state["ns_capo_" + str(i)]
    del st.session_state["ns_quantità_" + str(i)]
    st.session_state["lista_righe"].remove(i)
    st.rerun()


def da_capo_a_ID(capo):
    return Capi[Capi["capo"] == capo].ID_capo.values[0]


def salva_stampa_scontrino():
    corretto = True
    cliente = st.session_state["ns_cliente"]
    ID_cliente = C.da_nome_a_ID(cliente)
    data = st.session_state["ns_data"]

    capo = []
    quantità = []
    commento = []

    for k, v in st.session_state.items():
        if v == None:
            corretto = False
            break
        if "capo" in k:
            capo.append(da_capo_a_ID(v))
        if "quantità" in k:
            quantità.append(v)
        if "commento" in k:
            commento.append(v)

    if corretto:
        S.nuovo_scontrino(ID_cliente, capo, data, quantità, commento)
    else:
        st.error("Hai dimenticato di compilare qualche campo")


def nuovo_cliente(C):
    st.markdown("---")
    st.write(" ### Nuovo cliente")
    col1, col2, col3 = st.columns(3)
    cognome = col1.text_input(label="cognome")
    nome = col2.text_input(label="nome")
    numero = col3.text_input(label="numero di telefono")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("**:green[+ AGGIUNGI]**", use_container_width=True):
            if cognome and nome:
                if numero == "":
                    numero = "nessuno"
                C.nuovo_cliente(cognome, nome, numero)
                st.session_state["bottone_nc"] = True
                st.rerun()
    with col2:
        if st.button("**:red[ANNULLA]**", use_container_width=True):
            st.session_state["bottone_nc"] = True
            resetta_pagina()
    st.markdown("---")


def resetta_pagina():
    st.session_state["nuovo_scontrino"] = False
    st.session_state["lista_righe"] = [0]
    st.session_state["bottone_nc"] = True
    st.rerun()


if st.session_state.get("nuovo_scontrino", True):
    st.session_state["nuovo_scontrino"] = False
    st.session_state["lista_righe"] = [0]
    st.session_state["bottone_nc"] = True

C = clienti("dati/clienti.csv")
S = scontrini("dati/scontrini.csv")
Capi = pd.read_csv("dati/capi.csv")

st.write(" # NUOVO SCONTRINO")
if st.session_state["bottone_nc"]:
    if st.button("**:green[+ NUOVO CLIENTE]**", use_container_width=True):
        st.session_state["bottone_nc"] = False
        st.rerun()
else:
    nuovo_cliente(C)


if st.session_state["bottone_nc"]:
    st.write(" ### Cliente e data di consegna")
    col1, col2 = st.columns([3, 2])
    with col1:
        app = C.df.copy().sort_values(by="cognome")
        lista_clienti = app["cognome"] + " " + app["nome"]
        cliente = st.selectbox(
            "Seleziona il cliente",
            lista_clienti,
            index=None,
            placeholder="cognome nome",
            key="ns_cliente",
        )
    with col2:
        data = st.date_input(
            "Data di consegna",
            value=date.today() + timedelta(7),
            format="DD/MM/YYYY",
            key="ns_data",
        )

    if cliente:
        st.write(" ### Riga scontrino")
        for i in st.session_state["lista_righe"]:
            nuova_riga(i)
