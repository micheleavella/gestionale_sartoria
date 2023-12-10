import streamlit as st

from pagine.home import pagina_home
from pagine.nuovo_cliente import pagina_nuovo_cliente
from pagine.nuovo_scontrino import pagina_nuovo_scontrino


def inizializza(S):
    if "pagina" not in S:
        S["pagina"] = "home"
        S["pagina_nuovo_scontrino"] = pagina_nuovo_scontrino(S)
        S["nc_bottone"] = True


def tabs(S):
    col1, col2, col3 = st.columns(3)
    with col1:
        if S["pagina"] == "home":
            tipo = "primary"
        else:
            tipo = "secondary"
        if st.button(":house: HOME", type=tipo, use_container_width=True):
            S["pagina"] = "home"
            st.rerun()
    with col2:
        if S["pagina"] == "nuovo_scontrino":
            tipo = "primary"
        else:
            tipo = "secondary"
        if st.button(":moneybag: NUOVO SCONTRINO", type=tipo, use_container_width=True):
            S["pagina"] = "nuovo_scontrino"
            st.rerun()
    with col3:
        if S["pagina"] == "consegna":
            tipo = "primary"
        else:
            tipo = "secondary"
        if st.button(":spiral_note_pad: CONSEGNA", type=tipo, use_container_width=True):
            S["pagina"] = "consegna"
            st.rerun()


inizializza(st.session_state)
tabs(st.session_state)
st.divider()

if st.session_state["pagina"] == "home":
    pagina_home(st.session_state)

if st.session_state["pagina"] == "nuovo_scontrino":
    if st.session_state["nc_bottone"] == False:
        pagina_nuovo_cliente(st.session_state)
    else:
        if st.button("**:green[+ NUOVO CLIENTE]**", use_container_width=True):
            st.session_state["nc_bottone"] = False
            st.rerun()
        st.session_state["pagina_nuovo_scontrino"].mostra()
