"""
Ruta Óptima entre Ciudades de España
Matemática Discreta - Proyecto Final
Algoritmo: Dijkstra
Peso de aristas: Distancia en km (dato principal del grafo)
Información adicional: Costo estimado de bencina en CLP
"""

import tkinter as tk
from tkinter import ttk, messagebox
import heapq
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe

# ─────────────────────────────────────────────
# DATOS DEL GRAFO
# 15 ciudades de España con coordenadas (lon, lat) aproximadas
# ─────────────────────────────────────────────

CIUDADES = {
    "Madrid":       (3.70, 40.42),
    "Barcelona":    (8.15, 41.38),
    "Valencia":     (6.00, 39.47),
    "Sevilla":      (1.50, 37.38),
    "Zaragoza":     (6.88, 41.65),
    "Málaga":       (1.75, 36.72),
    "Bilbao":       (5.55, 43.26),
    "Murcia":       (5.00, 37.98),
    "Valladolid":   (2.85, 41.65),
    "Alicante":     (5.92, 38.35),
    "Córdoba":      (2.45, 37.88),
    "Granada":      (2.23, 37.18),
    "San Sebastián":(5.00, 43.32),
    "Santander":    (3.82, 43.46),
    "Toledo":       (3.00, 39.86),
}

# Aristas: (ciudad_a, ciudad_b, distancia_km)
# Fuente: distancias reales por carretera aproximadas
ARISTAS = [
    ("Madrid",      "Toledo",        71),
    ("Madrid",      "Valladolid",   193),
    ("Madrid",      "Zaragoza",     325),
    ("Madrid",      "Valencia",     357),
    ("Madrid",      "Córdoba",      398),
    ("Madrid",      "Sevilla",      531),
    ("Madrid",      "Bilbao",       395),
    ("Barcelona",   "Zaragoza",     296),
    ("Barcelona",   "Valencia",     349),
    ("Barcelona",   "San Sebastián",561),
    ("Zaragoza",    "Bilbao",       324),
    ("Zaragoza",    "Valencia",     309),
    ("Valencia",    "Alicante",     165),
    ("Valencia",    "Murcia",       241),
    ("Alicante",    "Murcia",        82),
    ("Murcia",      "Granada",      280),
    ("Granada",     "Málaga",       125),
    ("Granada",     "Córdoba",      166),
    ("Córdoba",     "Sevilla",      143),
    ("Sevilla",     "Málaga",       210),
    ("Bilbao",      "San Sebastián", 98),
    ("San Sebastián","Santander",   222),
    ("Santander",   "Valladolid",   236),
    ("Valladolid",  "Bilbao",       279),
    ("Toledo",      "Córdoba",      327),
    ("Madrid",      "Santander",    391),
]

# ─────────────────────────────────────────────
# COSTO DE BENCINA (dato informativo, no es el peso del grafo)
# Fuente: precio promedio bencina España 2024 ≈ 1.65 €/litro
# Consumo auto normal ≈ 8 litros / 100 km
# Tipo de cambio: 1 EUR ≈ 1.170 CLP (referencial)
# ─────────────────────────────────────────────
PRECIO_BENCINA_EUR_POR_LITRO = 1.65   # €/litro en España
CONSUMO_L_POR_100KM = 8.0             # litros cada 100 km (auto normal)
EUR_A_CLP = 1170                       # tipo de cambio referencial

def calcular_costo_bencina(km):
    """Retorna (costo_eur, costo_clp) para una distancia dada en km."""
    litros = (km * CONSUMO_L_POR_100KM) / 100
    eur = litros * PRECIO_BENCINA_EUR_POR_LITRO
    clp = eur * EUR_A_CLP
    return round(eur, 2), round(clp)


# ─────────────────────────────────────────────
# CONSTRUCCIÓN DEL GRAFO
# ─────────────────────────────────────────────

def construir_grafo():
    grafo = {ciudad: {} for ciudad in CIUDADES}
    for a, b, dist in ARISTAS:
        grafo[a][b] = dist
        grafo[b][a] = dist
    return grafo


# ─────────────────────────────────────────────
# ALGORITMO DE DIJKSTRA
# ─────────────────────────────────────────────

def dijkstra(grafo, origen, destino):
    """
    Implementación del algoritmo de Dijkstra.
    Retorna (distancia_total, camino)
    """
    distancias = {nodo: math.inf for nodo in grafo}
    distancias[origen] = 0
    previo = {nodo: None for nodo in grafo}
    visitados = set()
    cola = [(0, origen)]   # (costo_acumulado, nodo)

    while cola:
        costo_actual, nodo_actual = heapq.heappop(cola)

        if nodo_actual in visitados:
            continue
        visitados.add(nodo_actual)

        if nodo_actual == destino:
            break

        for vecino, peso in grafo[nodo_actual].items():
            if vecino not in visitados:
                nuevo_costo = costo_actual + peso
                if nuevo_costo < distancias[vecino]:
                    distancias[vecino] = nuevo_costo
                    previo[vecino] = nodo_actual
                    heapq.heappush(cola, (nuevo_costo, vecino))

    # Reconstruir camino
    camino = []
    nodo = destino
    while nodo is not None:
        camino.append(nodo)
        nodo = previo[nodo]
    camino.reverse()

    if camino[0] != origen:
        return math.inf, []

    return distancias[destino], camino


# ─────────────────────────────────────────────
# VISUALIZACIÓN DEL GRAFO
# ─────────────────────────────────────────────

def dibujar_grafo(ax, grafo, camino_optimo=None, origen=None, destino=None):
    ax.clear()
    ax.set_facecolor("#1a1a2e")

    # Coordenadas escaladas para visualización
    pos = {}
    lons = [v[0] for v in CIUDADES.values()]
    lats = [v[1] for v in CIUDADES.values()]
    lon_min, lon_max = min(lons), max(lons)
    lat_min, lat_max = min(lats), max(lats)

    for ciudad, (lon, lat) in CIUDADES.items():
        x = (lon - lon_min) / (lon_max - lon_min) * 9 + 0.5
        y = (lat - lat_min) / (lat_max - lat_min) * 6 + 0.5
        pos[ciudad] = (x, y)

    aristas_ruta = set()
    if camino_optimo and len(camino_optimo) > 1:
        for i in range(len(camino_optimo) - 1):
            aristas_ruta.add((camino_optimo[i], camino_optimo[i+1]))
            aristas_ruta.add((camino_optimo[i+1], camino_optimo[i]))

    # Dibujar aristas normales
    for a, b, dist in ARISTAS:
        if (a, b) not in aristas_ruta:
            x1, y1 = pos[a]
            x2, y2 = pos[b]
            ax.plot([x1, x2], [y1, y2], color="#4a4a6a", linewidth=1.2,
                    alpha=0.6, zorder=1)
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my, f"{dist}", fontsize=5.5, color="#7a7aaa",
                    ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.1', facecolor='#1a1a2e',
                              edgecolor='none', alpha=0.7))

    # Dibujar aristas de la ruta óptima
    if camino_optimo and len(camino_optimo) > 1:
        for i in range(len(camino_optimo) - 1):
            a, b = camino_optimo[i], camino_optimo[i+1]
            x1, y1 = pos[a]
            x2, y2 = pos[b]
            ax.plot([x1, x2], [y1, y2], color="#f0c040", linewidth=3.5,
                    alpha=0.95, zorder=3,
                    path_effects=[pe.Stroke(linewidth=5, foreground='#c07000',
                                            alpha=0.5), pe.Normal()])
            # Distancia sobre ruta
            dist_seg = grafo[a][b]
            mx, my = (x1+x2)/2, (y1+y2)/2
            ax.text(mx, my, f"{dist_seg} km", fontsize=6.5,
                    color="#fff8dc", ha='center', va='center', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.15', facecolor='#8b5e00',
                              edgecolor='#f0c040', linewidth=0.8, alpha=0.9),
                    zorder=5)

    # Dibujar nodos
    for ciudad, (x, y) in pos.items():
        if ciudad == origen:
            color_nodo = "#00e676"
            color_borde = "#00a152"
            radio = 0.22
        elif ciudad == destino:
            color_nodo = "#ff5252"
            color_borde = "#c50000"
            radio = 0.22
        elif camino_optimo and ciudad in camino_optimo:
            color_nodo = "#f0c040"
            color_borde = "#c07000"
            radio = 0.18
        else:
            color_nodo = "#5c6bc0"
            color_borde = "#3949ab"
            radio = 0.15

        circulo = plt.Circle((x, y), radio, color=color_nodo,
                             ec=color_borde, linewidth=1.5, zorder=4)
        ax.add_patch(circulo)

        offset_y = radio + 0.18
        ax.text(x, y + offset_y, ciudad, fontsize=6.5, color="white",
                ha='center', va='bottom', fontweight='bold', zorder=6,
                path_effects=[pe.withStroke(linewidth=2, foreground='#1a1a2e')])

    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 7.5)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("Red de Ciudades — España", color="white",
                 fontsize=11, fontweight='bold', pad=8)

    # Leyenda
    leyenda = [
        mpatches.Patch(color='#00e676', label='Origen'),
        mpatches.Patch(color='#ff5252', label='Destino'),
        mpatches.Patch(color='#f0c040', label='Ruta óptima'),
        mpatches.Patch(color='#5c6bc0', label='Otras ciudades'),
    ]
    ax.legend(handles=leyenda, loc='lower left', fontsize=7,
              facecolor='#2a2a4e', edgecolor='#5c6bc0',
              labelcolor='white', framealpha=0.9)


# ─────────────────────────────────────────────
# INTERFAZ GRÁFICA (TKINTER)
# ─────────────────────────────────────────────

class AplicacionRuta:
    def __init__(self, root):
        self.root = root
        self.root.title("Ruta Óptima — Ciudades de España")
        self.root.configure(bg="#1a1a2e")
        self.root.minsize(1050, 700)

        self.grafo = construir_grafo()
        self.ciudades_lista = sorted(CIUDADES.keys())

        self._construir_ui()

    # ── Layout ──────────────────────────────

    def _construir_ui(self):
        # Panel izquierdo (controles)
        panel_ctrl = tk.Frame(self.root, bg="#16213e", width=270, padx=14, pady=14)
        panel_ctrl.pack(side=tk.LEFT, fill=tk.Y)
        panel_ctrl.pack_propagate(False)

        # Panel derecho (grafo)
        panel_grafo = tk.Frame(self.root, bg="#1a1a2e")
        panel_grafo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self._panel_controles(panel_ctrl)
        self._panel_grafo(panel_grafo)

    def _panel_controles(self, parent):
        tk.Label(parent, text="🗺️ Ruta Óptima", bg="#16213e",
                 fg="#f0c040", font=("Helvetica", 15, "bold")).pack(pady=(0, 4))
        tk.Label(parent, text="España — Dijkstra", bg="#16213e",
                 fg="#7a8ab0", font=("Helvetica", 9)).pack(pady=(0, 16))

        # Separador
        tk.Frame(parent, bg="#3a3a6e", height=1).pack(fill=tk.X, pady=6)

        # Ciudad origen
        tk.Label(parent, text="Ciudad de Origen", bg="#16213e",
                 fg="#a0b0d0", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(8,2))
        self.combo_origen = ttk.Combobox(parent, values=self.ciudades_lista,
                                         state="readonly", font=("Helvetica", 10))
        self.combo_origen.pack(fill=tk.X, pady=(0,10))
        self.combo_origen.set("Madrid")

        # Ciudad destino
        tk.Label(parent, text="Ciudad de Destino", bg="#16213e",
                 fg="#a0b0d0", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(0,2))
        self.combo_destino = ttk.Combobox(parent, values=self.ciudades_lista,
                                          state="readonly", font=("Helvetica", 10))
        self.combo_destino.pack(fill=tk.X, pady=(0,16))
        self.combo_destino.set("Barcelona")

        # Botón calcular
        btn = tk.Button(parent, text="▶  Calcular Ruta Óptima",
                        command=self._calcular,
                        bg="#f0c040", fg="#1a1a2e",
                        font=("Helvetica", 10, "bold"),
                        relief=tk.FLAT, cursor="hand2",
                        activebackground="#c9a000", activeforeground="#1a1a2e",
                        padx=8, pady=7)
        btn.pack(fill=tk.X, pady=(0, 6))

        btn_reset = tk.Button(parent, text="↺  Limpiar",
                              command=self._limpiar,
                              bg="#3a3a6e", fg="#a0b0d0",
                              font=("Helvetica", 9),
                              relief=tk.FLAT, cursor="hand2",
                              activebackground="#5a5a9e", activeforeground="white",
                              padx=6, pady=5)
        btn_reset.pack(fill=tk.X, pady=(0, 14))

        tk.Frame(parent, bg="#3a3a6e", height=1).pack(fill=tk.X, pady=6)

        # Panel resultados
        tk.Label(parent, text="Resultados", bg="#16213e",
                 fg="#f0c040", font=("Helvetica", 10, "bold")).pack(anchor="w", pady=(8,4))

        self.lbl_distancia = tk.Label(parent, text="📏 Distancia total: —",
                                      bg="#16213e", fg="white",
                                      font=("Helvetica", 10, "bold"), anchor="w",
                                      justify="left", wraplength=240)
        self.lbl_distancia.pack(anchor="w", pady=2)

        self.lbl_costo_eur = tk.Label(parent, text="⛽ Bencina: —",
                                      bg="#16213e", fg="#f0c040",
                                      font=("Helvetica", 10), anchor="w",
                                      justify="left", wraplength=240)
        self.lbl_costo_eur.pack(anchor="w", pady=1)

        self.lbl_costo_clp = tk.Label(parent, text="💵 En pesos: —",
                                      bg="#16213e", fg="#00e676",
                                      font=("Helvetica", 10, "bold"), anchor="w",
                                      justify="left", wraplength=240)
        self.lbl_costo_clp.pack(anchor="w", pady=2)

        tk.Label(parent, text="Secuencia de ciudades:", bg="#16213e",
                 fg="#a0b0d0", font=("Helvetica", 9, "bold")).pack(anchor="w", pady=(10, 2))

        self.txt_camino = tk.Text(parent, height=10, bg="#0f1729",
                                  fg="#e0e8ff", font=("Courier", 9),
                                  relief=tk.FLAT, state=tk.DISABLED,
                                  wrap=tk.WORD, padx=6, pady=6)
        self.txt_camino.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        tk.Frame(parent, bg="#3a3a6e", height=1).pack(fill=tk.X, pady=4)
        tk.Label(parent,
                 text="⚙ Bencina España: 1,65 €/L · 8L/100km\n€1 ≈ $1.170 CLP (referencial)",
                 bg="#16213e", fg="#5a6a8a",
                 font=("Helvetica", 7), wraplength=240, justify="left").pack(anchor="w", pady=(4,0))

    def _panel_grafo(self, parent):
        self.fig, self.ax = plt.subplots(figsize=(8, 6), facecolor="#1a1a2e")
        self.fig.subplots_adjust(left=0.01, right=0.99, top=0.95, bottom=0.01)

        dibujar_grafo(self.ax, self.grafo)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

    # ── Acciones ────────────────────────────

    def _calcular(self):
        origen  = self.combo_origen.get()
        destino = self.combo_destino.get()

        if not origen or not destino:
            messagebox.showwarning("Datos incompletos",
                                   "Selecciona ciudad de origen y destino.")
            return
        if origen == destino:
            messagebox.showinfo("Sin ruta",
                                "El origen y el destino son la misma ciudad.")
            return

        distancia, camino = dijkstra(self.grafo, origen, destino)

        if distancia == math.inf or not camino:
            messagebox.showerror("Sin conexión",
                                 f"No existe ruta entre {origen} y {destino}.")
            return

        costo_eur, costo_clp = calcular_costo_bencina(distancia)

        # Actualizar etiquetas
        self.lbl_distancia.config(text=f"📏 Distancia total: {distancia} km")
        self.lbl_costo_eur.config(text=f"⛽ Bencina: {costo_eur:.2f} €")
        self.lbl_costo_clp.config(text=f"💵 En pesos: ${costo_clp:,.0f} CLP")

        # Actualizar texto secuencia
        self.txt_camino.config(state=tk.NORMAL)
        self.txt_camino.delete("1.0", tk.END)
        for i, ciudad in enumerate(camino):
            prefijo = "🟢 " if ciudad == origen else ("🔴 " if ciudad == destino else f"  {i}. ")
            self.txt_camino.insert(tk.END, f"{prefijo}{ciudad}\n")
            if i < len(camino) - 1:
                seg_dist = self.grafo[camino[i]][camino[i+1]]
                self.txt_camino.insert(tk.END, f"     ↓  {seg_dist} km\n")
        self.txt_camino.config(state=tk.DISABLED)

        # Redibujar grafo con ruta
        dibujar_grafo(self.ax, self.grafo, camino_optimo=camino,
                      origen=origen, destino=destino)
        self.canvas.draw()

    def _limpiar(self):
        self.combo_origen.set("Madrid")
        self.combo_destino.set("Barcelona")
        self.lbl_distancia.config(text="📏 Distancia total: —")
        self.lbl_costo_eur.config(text="⛽ Bencina: —")
        self.lbl_costo_clp.config(text="💵 En pesos: —")
        self.txt_camino.config(state=tk.NORMAL)
        self.txt_camino.delete("1.0", tk.END)
        self.txt_camino.config(state=tk.DISABLED)
        dibujar_grafo(self.ax, self.grafo)
        self.canvas.draw()


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()

    # Estilo ttk
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox",
                    fieldbackground="#0f1729",
                    background="#0f1729",
                    foreground="white",
                    selectbackground="#3a3a6e",
                    selectforeground="white",
                    arrowcolor="#f0c040")

    app = AplicacionRuta(root)
    root.mainloop()
