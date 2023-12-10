import streamlit as st

from funzioni.clienti import clienti


def pagina_nuovo_cliente(S):
    C = clienti("dati/clienti.csv")
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
                if C.nuovo_cliente(cognome, nome, numero):
                    st.session_state["nc_bottone"] = True
                    st.rerun()
                else:
                    st.error("Utente già presente database")
    with col2:
        if st.button("**:red[ANNULLA]**", use_container_width=True):
            S["nc_bottone"] = True
            st.rerun()
    st.markdown("---")
