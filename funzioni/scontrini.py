import numpy as np
import pandas as pd


class scontrini:
    def __init__(self, path):
        self.path = path
        self.df = self.carica_tabella()

    def carica_tabella(self):
        df = pd.read_csv(
            self.path,
            dtype={
                "ID_scontrino": "int32",
                "ID_riga_scontrino": "int32",
                "ID_cliente": "int32",
                "ID_capo": "int32",
                "data": "str",
                "quantità": "str",
                "commento": "str",
            },
        )
        df["data"] = pd.to_datetime(df["data"])
        return df

    def salva(self):
        self.df.to_csv(self.path, index=0)

    def nuovo_scontrino(self, ID_cliente, ID_capo, data, quantità, commento):
        id_new = self.df["ID_scontrino"].max() + 1
        L = len(ID_capo)
        nuovo = pd.DataFrame(
            {
                "ID_scontrino": [id_new for i in range(L)],
                "ID_riga_scontrino": [i for i in range(L)],
                "ID_cliente": [ID_cliente for i in range(L)],
                "ID_capo": ID_capo,
                "data": [data for i in range(L)],
                "quantità": quantità,
                "commento": commento,
            }
        )
        nuovo["data"] = pd.to_datetime(nuovo["data"])
        self.df = pd.concat([self.df, nuovo], ignore_index=1)
        self.df["data"] = pd.to_datetime(self.df["data"])
        self.salva()
