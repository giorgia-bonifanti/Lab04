class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome

    def __str__(self):
        return f"[{self.codice}] {self.nome} {self.cognome}"

    def __eq__(self, other):
        if isinstance(other, Espositore):     #controllare se l'oggetto confrontato è un espositore
            return self.codice == other.codice   #gli espositori sono uguali se hanno lo stesso codice
        return False


#classe genitore:
class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = float(superficie)
        self.padiglione = padiglione
        self.prezzo_base = float(prezzo_base)
        self.espositore_assegnato= None

    def calcola_prezzo(self):
        return self.prezzo_base

    def __str__(self):
        #controllo se l'espositore è disponibile o assegnato
        stato="Disponibile" if self.espositore_assegnato is None else (f"Assegnato a {self.espositore_assegnato.codice}")
        return f"{self.codice}: Standard | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - {stato}"

    def __lt__(self, other):  #simboleggia il minore di:
        return self.calcola_prezzo() < other.calcola_prezzo()



#classe figlia con gli stand con le prese:
class StandPreseExtra(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, numero_prese):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.numero_prese = int(numero_prese)

    def calcola_prezzo(self):    #polimorfismo
        return self.prezzo_base * (1 + 0.07 * self.numero_prese) #calcola il sovraprezzo

    def __str__(self):
        stato="Disponibile" if self.espositore_assegnato is None else f"Assegnato a {self.espositore_assegnato.codice}"
        return f"{self.codice}: Prese Extra | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - Prese aggiuntive: {self.numero_prese} - {stato}"



#classe figlia con gli stand premium:
class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base) #chiamo il genitore per far leggere i dati di Stand
        self.posizione = posizione

    def calcola_prezzo(self):
        return self.prezzo_base * 1.30  #applico il 30% di sovrappezzo fisso

    def __str__(self):
        stato="Disponibile" if self.espositore_assegnato is None else f"Assegnato a {self.espositore_assegnato.codice}"
        return f"{self.codice}: Premium | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - Posizione: {self.posizione} - {stato}"



class LingottoFiere:
    def __init__(self, nome):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome
        self.stand = {}   #creo un dizionario per salvare gli stand
        self.espositori = {}   #creo un dizionario per salvare gli espositori

    """Aggiungere setter e getter se necessari"""
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nuovo_nome):
        self._nome = nuovo_nome

    def carica_file_dati(self, file_path):
        """Carica i dati (stand ed espositori) dal file"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                for riga in f:
                    riga = riga.strip()
                    if not riga:
                        continue

                    parti = riga.split(",")
                    codice = parti[0].strip()

                    if codice.startswith("SI"):  #significa che è una riga di uno stand
                        superficie = parti[1].strip()
                        padiglione = parti[2].strip()
                        prezzo = parti[3].strip()

                        if len(parti) == 4:
                            nuovo_stand = Stand(codice, superficie, padiglione, prezzo)
                            self.stand[codice] = nuovo_stand

                        elif len(parti) == 5:
                            caratteristica_extra = parti[4].strip()
                            if caratteristica_extra.isdigit():
                                nuovo_stand = StandPreseExtra(codice, superficie, padiglione, prezzo, caratteristica_extra)

                            else:
                                nuovo_stand = StandPremium(codice, superficie, padiglione, prezzo, caratteristica_extra)
                            self.stand[codice] = nuovo_stand

                    elif codice.startswith("ES"):
                        if len(parti) >=3:
                            nome= parti[1].strip()
                            cognome= parti[2].strip()
                            nuovo_espositore=Espositore(codice, nome, cognome)
                            self.espositori[codice]=nuovo_espositore

        except FileNotFoundError:
            raise FileNotFoundError("Errore, il file dati_lingotto.csv non è stato trovato!")


    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        """Associa uno stand a un espositore"""
        if codice_stand not in self.stand:
            raise Exception("Lo stand non esiste nel sistema.")

        if codice_espositore not in self.espositori:
            raise Exception("L'espositore richiesto non esiste nel sistema.")

        stand_selezionato = self.stand[codice_stand]
        espositore_selezionato = self.espositori[codice_espositore]

        if stand_selezionato.espositore_assegnato is not None:
            raise Exception("Questo stand non è disponibile, è già stato assegnato.")

        for s in self.stand.values():
            if s.espositore_assegnato == espositore_selezionato:
                raise Exception("L'espositore ha già uno stand assegnato per questa fiera.")

        stand_selezionato.espositore_assegnato = espositore_selezionato



    def elenca_espositori(self):
        """Stampa l'elenco degli espositori mostrando, per ognuno, lo stand a cui è associato, quando applicabile """
        for esp in self.espositori.values():
            stand_trovato = None

            for s in self.stand.values():
                if s.espositore_assegnato == esp:
                    stand_trovato = s
                    break

            if stand_trovato is not None:
                print(f"{esp} -> Assegnato a Stand: {stand_trovato.codice}")    #Stampo espositore e codice stand
            else:
                print(f"{esp} -> Nessuno stand assegnato attualmente.")



    def stand_ordinati_per_prezzo(self):
        """Restituisce la lista ordinata degli stand in base al prezzo"""
        return sorted(self.stand.values())
