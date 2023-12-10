import pandas as pd
import streamlit as st

from funzioni.clienti import clienti
from funzioni.scontrini import scontrini


def nuova_consegna(CO, ID_scontrino, prezzo):
    d = pd.DataFrame([{"ID_scontrino": ID_scontrino, "prezzo": prezzo}])
    CO = pd.concat([CO, d], ignore_index=True)
    CO.to_csv("dati/consegne.csv", index=False)
    st.session_state["pagina"] = "home"
    st.rerun()


def pagina_consegna():
    C = clienti("dati/clienti.csv")
    S = scontrini("dati/scontrini.csv")
    CO = pd.read_csv("dati/consegne.csv")
    df_capi = pd.read_csv("dati/capi.csv")

    st.write("## CONSEGNA")
    app = C.df.copy().sort_values(by="cognome")
    clienti_con_scontino = (
        S.df.groupby("ID_cliente").first().reset_index()[["ID_cliente"]]
    )
    app = app.merge(clienti_con_scontino)
    lista_clienti = app["cognome"] + " " + app["nome"]
    cliente = st.selectbox(
        "Seleziona il cliente",
        lista_clienti,
        index=None,
        placeholder="cognome nome cliente",
        label_visibility="collapsed",
    )
    if cliente is not None:
        st.divider()
        ID_cliente = C.da_nome_a_ID(cliente)
        df = S.df.merge(df_capi).merge(CO, how="outer", indicator=True)
        df = df[df["_merge"] == "left_only"].reset_index(drop=1)
        df = df[df.ID_cliente == ID_cliente]
        if len(df) > 0:
            for id, d in df.groupby("ID_scontrino"):
                d["data"] = d["data"].dt.strftime("%d/%m/%Y")
                data = d.data.values[0]
                col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                with col1:
                    st.write("Scontrino del : ")
                    st.write("**:violet[" + data + "]**")

                with col3:
                    st.write("Prezzo finale [€]:")
                    prezzo = st.number_input(
                        value=0.0,
                        label="Prezzo",
                        min_value=0.0,
                        step=0.5,
                        label_visibility="collapsed",
                        key="prezzo_" + str(id),
                    )
                with col4:
                    st.write("Consegna:")
                    if st.button(
                        ":green[:white_check_mark:]",
                        use_container_width=True,
                        key="bottone_" + str(id),
                    ) and (prezzo != 0):
                        nuova_consegna(CO, id, prezzo)
                st.dataframe(
                    d[["quantità", "capo", "commento"]],
                    hide_index=True,
                    use_container_width=True,
                )
                st.divider()
        else:
            st.info("Il cliente selezionato non ha nessuno scontrino aperto")
