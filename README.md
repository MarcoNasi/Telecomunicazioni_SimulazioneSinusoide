# 📡 Simulatore della Formazione del Segnale Sinusoidale

Questo software è stato progettato per aiutare gli studenti di **Telecomunicazioni (4° anno)** a comprendere visivamente come nasce una sinusoide, partendo dai concetti fondamentali della trigonometria e dei segnali periodici.

---

> ### [Scarica l'Eseguibile per Windows (.exe)](https://github.com/MarcoNasi/Telecomunicazioni_SimulazioneSinusoide/releases/download/Release/Sinusoide.exe)

# Concetto Teorico

In telecomunicazioni, un segnale sinusoidale può essere visto come la proiezione nel tempo di un **punto che si muove di Moto Circolare Uniforme (MCU)** lungo una circonferenza di raggio $A$ (Ampiezza).

La formula che governa questo fenomeno è:
$$s(t) = A \cdot \sin(\omega t + \phi)$$

Dove:
- **$A$ (Ampiezza)**: Il raggio del cerchio rotante.
- **$\omega$ (Pulsazione)**: La velocità con cui il cerchio ruota (misurata in rad/s).
- **$t$ (Tempo)**: Rappresentato dallo scorrimento orizzontale (o verticale) della "carta".

Questo simulatore mostra visivamente come il "braccio" del cerchio proietti la sua altezza istantanea su un nastro di carta in movimento, creando la classica forma d'onda.

---

## Caratteristiche del Simulatore

- **Visualizzazione in Tempo Reale**: Osserva il legame diretto tra la rotazione e l'onda risultante.
- **Scorrimento Infinito**: La traccia prosegue senza interruzioni, simulando un oscilloscopio reale.
- **Doppio Orientamento**: Possibilità di proiettare la sinusoide sia in orizzontale che in verticale.

---

## Come Utilizzare lo Strumento

L'applicazione è divisa in due finestre: la **Visualizzazione Grafica** (grande e chiara) e il **Pannello di Controllo**.

### Parametri Regolabili:
1. **Ampiezza**: Trascina lo slider per ingrandire o rimpicciolire il segnale.
2. **Direzione**: Cambia il verso di scorrimento del segnale (Destra/Basso o Sinistra/Alto).
3. **Orientamento**: Scegli se visualizzare la propagazione lungo l'asse X o l'asse Y.
4. **Colori**: Personalizza l'aspetto grafico per distinguere meglio il cerchio generatore dalla traccia risultante.
5. **Comandi**: Usa i tasti **Pausa/Avvia** per analizzare un istante specifico o **Reset** per ricominciare la traccia.

---

## Note Tecniche 

Il software è scritto in **Python 3.12** utilizzando due librerie principali:
- **Pygame**: Per il rendering grafico ad alte prestazioni.
- **Tkinter**: Per l'interfaccia utente (GUI) nativa e leggera.

L'architettura utilizza un **thread logico separato** per i calcoli matematici, assicurando che la frequenza di campionamento virtuale rimanga costante indipendentemente dal carico sulla CPU o dallo spostamento delle finestre.

---

## Installazione e Distribuzione

Se sei uno studente e vuoi solo usare il programma:
1. Scarica il file `Sinusoide.exe`.
2. Avvialo con un doppio clic (non serve installare Python).

Se sei un aspirante sviluppatore:
1. Installa le dipendenze: `pip install pygame`
2. Avvia lo script principale: `python main.py`

---

**Sviluppato da:** HighMark [Marco N.]
*Creato appositamente per le lezioni di Telecomunicazioni Vallauri.*
