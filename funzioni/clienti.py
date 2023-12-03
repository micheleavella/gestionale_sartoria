import pandas as pd


class clienti:
    def __init__(self, path):
        self.path = path
        self.df = self.carica_tabella()

    def carica_tabella(self):
        df = pd.read_csv(
            self.path,
            dtype={
                "ID_cliente": "int32",
                "cognome": "str",
                "nome": "str",
                "cellulare": "str",
            },
        )
        return df

    def salva(self):
        self.df.to_csv(self.path, index=0)

    def nuovo_cliente(self, cognome, nome, cellulare):
        id_new = self.df["ID_cliente"].max() + 1
        nuovo = pd.DataFrame(
            [
                {
                    "ID_cliente": id_new,
                    "cognome": cognome,
                    "nome": nome,
                    "cellulare": cellulare,
                }
            ]
        )
        self.df = pd.concat([self.df, nuovo], ignore_index=1)
        self.salva()

    def da_nome_a_ID(self, cognomenome):
        df = self.df.copy()
        df["cognomenome"] = df["cognome"] + " " + df["nome"]
        return df[df["cognomenome"] == cognomenome].ID_cliente.values[0]
