import math
import threading
import time
import tkinter as tk
import webbrowser
from tkinter import colorchooser, ttk
import pygame

class StatoSimulazione:
    def __init__(self):
        self.lock = threading.Lock()
        self.in_pausa = False
        self.direzione = 1
        self.orientamento = "Orizzontale"
        self.ampiezza = 160
        self.colore_cerchio = (220, 40, 40)
        self.colore_traccia = (30, 90, 220)
        self.colore_sfondo = (245, 245, 245)
        self.richiesta_reset = False
        
        self.angolo = 0.0
        self.punti_traccia = []
        self.ultimo_aggiornamento = time.time()

class MotoreLogico:
    def __init__(self, stato, stop_event):
        self.stato = stato
        self.stop_event = stop_event
        self.velocita_angolare = 1.4
        self.velocita_scorrimento = 180.0
        self.larghezza = 1200
        self.altezza = 650

    def esegui(self):
        while not self.stop_event.is_set():
            ora = time.time()
            dt = ora - self.stato.ultimo_aggiornamento
            self.stato.ultimo_aggiornamento = ora

            if dt > 0.1:
                dt = 0.016

            with self.stato.lock:
                if self.stato.richiesta_reset:
                    self.stato.angolo = 0.0
                    self.stato.punti_traccia = []
                    self.stato.richiesta_reset = False
                    continue

                if not self.stato.in_pausa:
                    self.stato.angolo += self.velocita_angolare * dt
                    
                    spostamento = self.velocita_scorrimento * dt * self.stato.direzione
                    nuovi_punti = []
                    
                    for x, y in self.stato.punti_traccia:
                        if self.stato.orientamento == "Orizzontale":
                            nx = x + spostamento
                            if 0 <= nx <= self.larghezza:
                                nuovi_punti.append((nx, y))
                        else:
                            ny = y + spostamento
                            if 0 <= ny <= self.altezza:
                                nuovi_punti.append((x, ny))
                    
                    raggio = self.stato.ampiezza
                    cx, cy = self.larghezza // 2, self.altezza // 2
                    
                    if self.stato.orientamento == "Orizzontale":
                        wx = 230 if self.stato.direzione == 1 else self.larghezza - 230
                        wy = cy
                        px = wx + raggio + 50 if self.stato.direzione == 1 else wx - raggio - 50
                        py = wy - raggio * math.sin(self.stato.angolo)
                    else:
                        wx = cx
                        wy = 180 if self.stato.direzione == 1 else self.altezza - 180
                        px = wx + raggio * math.cos(self.stato.angolo)
                        py = wy + raggio + 50 if self.stato.direzione == 1 else wy - raggio - 50
                    
                    nuovi_punti.append((px, py))
                    self.stato.punti_traccia = nuovi_punti

            time.sleep(0.01)

class InterfacciaGrafica:
    def __init__(self, stato, stop_event):
        self.stato = stato
        self.stop_event = stop_event
        self.larghezza = 1200
        self.altezza = 650

    def avvia(self):
        pygame.init()
        schermo = pygame.display.set_mode((self.larghezza, self.altezza))
        pygame.display.set_caption("Simulazione Sinusoide - Telecomunicazioni")
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("Segoe UI", 24)

        while not self.stop_event.is_set():
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.stop_event.set()

            with self.stato.lock:
                sfondo = self.stato.colore_sfondo
                cerchio_colore = self.stato.colore_cerchio
                traccia_colore = self.stato.colore_traccia
                angolo = self.stato.angolo
                raggio = self.stato.ampiezza
                punti = list(self.stato.punti_traccia)
                orientamento = self.stato.orientamento
                direzione = self.stato.direzione
                pausa = self.stato.in_pausa

            schermo.fill(sfondo)
            cx, cy = self.larghezza // 2, self.altezza // 2

            if orientamento == "Orizzontale":
                wx = 230 if direzione == 1 else self.larghezza - 230
                wy = cy
                px = wx + raggio + 50 if direzione == 1 else wx - raggio - 50
                py = wy - raggio * math.sin(angolo)
                ox, oy = wx + raggio * math.cos(angolo), wy - raggio * math.sin(angolo)
                pygame.draw.line(schermo, (180, 180, 180), (0, wy), (self.larghezza, wy), 2)
            else:
                wx = cx
                wy = 180 if direzione == 1 else self.altezza - 180
                px = wx + raggio * math.cos(angolo)
                py = wy + raggio + 50 if direzione == 1 else wy - raggio - 50
                ox, oy = wx + raggio * math.cos(angolo), wy - raggio * math.sin(angolo)
                pygame.draw.line(schermo, (180, 180, 180), (wx, 0), (wx, self.altezza), 2)

            pygame.draw.circle(schermo, (100, 100, 100), (wx, wy), int(raggio), 2)
            pygame.draw.line(schermo, (150, 150, 150), (wx, wy), (ox, oy), 2)
            pygame.draw.circle(schermo, cerchio_colore, (int(ox), int(oy)), 10)
            pygame.draw.line(schermo, (200, 200, 200), (ox, oy), (px, py), 1)

            if len(punti) > 1:
                pygame.draw.lines(schermo, traccia_colore, False, punti, 3)
            
            if punti:
                pygame.draw.circle(schermo, traccia_colore, (int(punti[-1][0]), int(punti[-1][1])), 6)

            testo = "PAUSA" if pausa else "IN CORSO"
            colore_testo = (200, 50, 50) if pausa else (50, 150, 50)
            img_testo = font.render(testo, True, colore_testo)
            schermo.blit(img_testo, (20, 20))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

class PannelloControllo:
    def __init__(self, root, stato, stop_event):
        self.root = root
        self.stato = stato
        self.stop_event = stop_event
        self.root.title("Controlli Simulazione")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        
        self.colori = {
            "Rosso": (220, 40, 40),
            "Verde": (40, 160, 70),
            "Blu": (30, 90, 220),
            "Giallo": (240, 200, 40),
            "Nero": (30, 30, 30),
            "Bianco": (245, 245, 245),
            "Magenta": (200, 70, 200),
            "Ciano": (40, 190, 200),
        }
        
        self.var_cerchio = tk.StringVar(value="Rosso")
        self.var_traccia = tk.StringVar(value="Blu")
        self.var_sfondo = tk.StringVar(value="Bianco")
        self.var_direzione = tk.StringVar(value="Destra")
        self.var_orientamento = tk.StringVar(value="Orizzontale")
        self.var_ampiezza = tk.DoubleVar(value=160)
        self.var_pulsante_pausa = tk.StringVar(value="Pausa")
        
        self._crea_interfaccia()
        self.root.protocol("WM_DELETE_WINDOW", self._chiudi)
        self.root.after(200, self._controlla_stop)

    def _crea_interfaccia(self):
        stile = ttk.Style()
        stile.configure("TLabel", font=("Segoe UI", 10))
        stile.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))

        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)

        ttk.Label(main, text="CONFIGURAZIONE", style="Header.TLabel").pack(pady=(0, 15))

        f_colori = ttk.LabelFrame(main, text=" Colori ", padding=10)
        f_colori.pack(fill="x", pady=5)

        for i, (testo, var) in enumerate([("Cerchio", self.var_cerchio), ("Traccia", self.var_traccia), ("Sfondo", self.var_sfondo)]):
            ttk.Label(f_colori, text=testo).grid(row=i, column=0, sticky="w", pady=2)
            cb = ttk.Combobox(f_colori, textvariable=var, values=list(self.colori.keys()) + ["Custom"], state="readonly", width=15)
            cb.grid(row=i, column=1, padx=10, pady=2)
            cb.bind("<<ComboboxSelected>>", lambda e, t=testo.lower(): self._cambia_colore(t))

        f_impostazioni = ttk.LabelFrame(main, text=" Parametri ", padding=10)
        f_impostazioni.pack(fill="x", pady=5)

        ttk.Label(f_impostazioni, text="Direzione:").grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(f_impostazioni, text="Destra/Basso", value="Destra", variable=self.var_direzione, command=self._aggiorna_stato).grid(row=0, column=1)
        ttk.Radiobutton(f_impostazioni, text="Sinistra/Alto", value="Sinistra", variable=self.var_direzione, command=self._aggiorna_stato).grid(row=0, column=2)

        ttk.Label(f_impostazioni, text="Orientamento:").grid(row=1, column=0, sticky="w", pady=(10, 0))
        ttk.Radiobutton(f_impostazioni, text="Orizzontale", value="Orizzontale", variable=self.var_orientamento, command=self._aggiorna_stato).grid(row=1, column=1, pady=(10, 0))
        ttk.Radiobutton(f_impostazioni, text="Verticale", value="Verticale", variable=self.var_orientamento, command=self._aggiorna_stato).grid(row=1, column=2, pady=(10, 0))

        ttk.Label(f_impostazioni, text="Ampiezza:").grid(row=2, column=0, sticky="w", pady=(10, 0))
        ttk.Scale(f_impostazioni, from_=40, to=240, variable=self.var_ampiezza, command=lambda v: self._aggiorna_ampiezza()).grid(row=2, column=1, columnspan=2, sticky="ew", pady=(10, 0))

        f_azioni = ttk.Frame(main, padding=(0, 20))
        f_azioni.pack(fill="x")
        
        ttk.Button(f_azioni, textvariable=self.var_pulsante_pausa, command=self._toggle_pausa).pack(fill="x", pady=2)
        ttk.Button(f_azioni, text="Reset Simulazione", command=self._reset).pack(fill="x", pady=2)

        info = ttk.Label(main, text="Sviluppato da HighMark [Marco N.]\nClicca per GitHub", justify="center", cursor="hand2", foreground="blue")
        info.pack(side="bottom", pady=10)
        info.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/MarcoNasi"))

    def _cambia_colore(self, tipo):
        var = {"cerchio": self.var_cerchio, "traccia": self.var_traccia, "sfondo": self.var_sfondo}[tipo]
        scelta = var.get()
        
        if scelta == "Custom":
            colore = colorchooser.askcolor(title="Seleziona Colore")
            if colore[0]:
                rgb = tuple(int(c) for c in colore[0])
            else: return
        else:
            rgb = self.colori[scelta]

        with self.stato.lock:
            if tipo == "cerchio": self.stato.colore_cerchio = rgb
            elif tipo == "traccia": self.stato.colore_traccia = rgb
            else: self.stato.colore_sfondo = rgb

    def _aggiorna_stato(self):
        dir_val = 1 if self.var_direzione.get() == "Destra" else -1
        orient = self.var_orientamento.get()
        with self.stato.lock:
            self.stato.direzione = dir_val
            self.stato.orientamento = orient
            self.stato.richiesta_reset = True

    def _aggiorna_ampiezza(self):
        with self.stato.lock:
            self.stato.ampiezza = self.var_ampiezza.get()

    def _toggle_pausa(self):
        with self.stato.lock:
            self.stato.in_pausa = not self.stato.in_pausa
            pausa = self.stato.in_pausa
        self.var_pulsante_pausa.set("Avvia" if pausa else "Pausa")

    def _reset(self):
        with self.stato.lock:
            self.stato.richiesta_reset = True

    def _chiudi(self):
        self.stop_event.set()
        self.root.destroy()

    def _controlla_stop(self):
        if self.stop_event.is_set():
            if self.root.winfo_exists():
                self.root.destroy()
            return
        self.root.after(200, self._controlla_stop)

def avvia_applicazione():
    stato = StatoSimulazione()
    stop_event = threading.Event()
    
    motore = MotoreLogico(stato, stop_event)
    grafica = InterfacciaGrafica(stato, stop_event)
    
    t_logica = threading.Thread(target=motore.esegui, daemon=True)
    t_grafica = threading.Thread(target=grafica.avvia, daemon=True)
    
    t_logica.start()
    t_grafica.start()
    
    root = tk.Tk()
    PannelloControllo(root, stato, stop_event)
    root.mainloop()
    
    stop_event.set()
    t_logica.join(timeout=1)
    t_grafica.join(timeout=1)

if __name__ == "__main__":
    avvia_applicazione()
