from datetime import date, timedelta

import pandas as pd
import streamlit as st

from funzioni.clienti import clienti
from funzioni.scontrini import scontrini
from funzioni.stampa import stampa


class pagina_nuovo_scontrino:
    def __init__(self, S):
        self.lista_righe = [0]
        self.df_capi = pd.read_csv("dati/capi.csv")
        self.S = S

        # mettere che li importa al momento

    @property
    def clienti(self):
        return clienti("dati/clienti.csv")

    @property
    def scontrini(self):
        return scontrini("dati/scontrini.csv")

    def mostra(self):
        st.write("## NUOVO SCONTRINO")
        self.mostra_cliente_data()

    def cancella_riga(self, i):
        del self.S["ns_cancella_" + str(i)]
        del self.S["ns_commento_" + str(i)]
        del self.S["ns_capo_" + str(i)]
        del self.S["ns_quantita_" + str(i)]
        self.lista_righe.remove(i)

    def resetta(self):
        for i in range(len(self.lista_righe)):
            i = self.lista_righe[0]
            self.cancella_riga(i)
        self.lista_righe = [0]

        del self.S["ns_cliente"]
        del self.S["ns_data"]
        st.rerun()

    def mostra_cliente_data(self):
        st.write(" ### Cliente e data di consegna")
        col1, col2 = st.columns([3, 2])
        with col1:
            app = self.clienti.df.copy().sort_values(by="cognome")
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
            self.mostra_righe()

    def salva_stampa_scontrino(self):
        C = clienti("dati/clienti.csv")
        corretto = True
        cliente = self.S["ns_cliente"]
        ID_cliente = C.da_nome_a_ID(cliente)
        data_consegna = self.S["ns_data"]
        data = date.today()

        capo = []
        ID_capo = []
        quantita = []
        commento = []

        for i in self.lista_righe:
            # CAPO
            v = self.S["ns_capo_" + str(i)]
            if v is None:
                corretto = False
                break
            else:
                capo.append(v)
                ID_capo.append(
                    self.df_capi[self.df_capi["capo"] == v].ID_capo.values[0]
                )
            # QUANTITA
            v = self.S["ns_quantita_" + str(i)]
            quantita.append(v)

            # COMMENTO
            v = self.S["ns_commento_" + str(i)]
            if (v is not None) and (v != ""):
                commento.append(v)
            else:
                corretto = False
                break

        if corretto:
            self.scontrini.nuovo_scontrino(
                ID_cliente, ID_capo, data, quantita, commento
            )
            stampa(cliente, data, quantita, capo, commento, data_consegna)
            self.S["pagina"] = "home"
            self.resetta()
        else:
            st.error("Hai dimenticato di compilare qualche campo")

    def mostra_righe(self):
        for i in self.lista_righe:
            col1, col2, col3, col4 = st.columns([2, 2, 3, 1])

            if i == min(self.lista_righe):
                with col1:
                    st.write("Quantità")

                with col2:
                    st.write("Capo")

                with col3:
                    st.write("Commento")

                with col4:
                    st.write("Elimina")

            with col1:
                quantita = st.number_input(
                    "Quantità",
                    min_value=1,
                    step=1,
                    key="ns_quantita_" + str(i),
                    label_visibility="collapsed",
                )

            with col2:
                capo = st.selectbox(
                    "Seleziona il capo",
                    self.df_capi["capo"].values,
                    index=None,
                    placeholder="nome capo",
                    key="ns_capo_" + str(i),
                    label_visibility="collapsed",
                )

            with col3:
                commento = st.text_input(
                    "Commento",
                    key="ns_commento_" + str(i),
                    label_visibility="collapsed",
                )

            with col4:
                if st.button(
                    ":red[X]", key="ns_cancella_" + str(i), help="cancella la riga"
                ):
                    if len(self.lista_righe) > 1:
                        self.cancella_riga(i)
                        st.rerun()

            if max(self.lista_righe) == i:
                if st.button("**:green[+ NUOVA RIGA]**", use_container_width=True):
                    if capo and commento:
                        self.lista_righe.append(i + 1)
                        st.rerun()

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("**:red[CANCELLA TUTTO]**", use_container_width=True):
                        self.resetta()
                with col2:
                    if st.button(
                        "**:orange[SALVA E STAMPA]**", use_container_width=True
                    ):
                        self.salva_stampa_scontrino()
