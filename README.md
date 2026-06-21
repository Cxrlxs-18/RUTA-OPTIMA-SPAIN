# Ruta Óptima entre Ciudades de España
### Proyecto Final — Matemática Discreta

Aplicación en Python que modela una red de 15 ciudades de España mediante un **grafo ponderado** y calcula la **ruta óptima** entre dos ciudades usando el **algoritmo de Dijkstra**.

---

## Integrantes

| Nombres            | 
|--------------------|
| [Gonzalo Albornoz] |
| [Carlos Nahuelcoy] |
| [Rodrigo Sevilla ] |
| [Matías Salinas  ] |

---

## Descripción del Problema

Se construye un grafo ponderado **G = (V, E, w)** donde:
- **V** → 15 ciudades de España (vértices)
- **E** → 26 conexiones reales por carretera (aristas)
- **w(u,v)** → distancia en km entre ciudades (peso)

El objetivo es encontrar el camino de **menor distancia total** entre una ciudad de origen y una de destino.

---

## Ciudades Incluidas

Madrid · Barcelona · Valencia · Sevilla · Zaragoza · Málaga · Bilbao · Murcia · Valladolid · Alicante · Córdoba · Granada · San Sebastián · Santander · Toledo

---

## Algoritmo Utilizado

**Dijkstra** con cola de prioridad (min-heap).  
Complejidad: `O((V + E) log V)`  
Condición requerida: todos los pesos deben ser positivos ✅

---

## Requisitos

- Python 3.8 o superior
- matplotlib

---

## Instalación y Ejecución

```bash
# 1. Clonar el repositorio
git clone https://github.com/Cxrlxs-18/RUTA-OPTIMA-SPAIN.git

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la aplicación
python ruta_optima_españa.py
```

---

## Uso de la Interfaz

1. Seleccionar **ciudad de origen** en el menú desplegable
2. Seleccionar **ciudad de destino**
3. Presionar **▶ Calcular Ruta Óptima**
4. Ver en pantalla:
   - Secuencia de ciudades de la ruta
   - Distancia total en km
   - Costo estimado de bencina en € y en CLP
   - Ruta resaltada en el grafo

---

## Estructura del Repositorio

```
📦 proyecto-rutas-españa
 ┣ 📄 ruta_optima_españa.py     # Código fuente principal
 ┣ 📄 requirements.txt          # Librerías necesarias
 ┗ 📄 README.md                 # Este archivo
```

---

## Librerías Utilizadas

| Librería | Uso |
|----------|-----|
| `tkinter` | Interfaz gráfica |
| `matplotlib` | Visualización del grafo |
| `heapq` | Cola de prioridad para Dijkstra |
| `math` | Constante infinito para inicialización |

---

## Ejemplos de Rutas

| Origen | Destino                                   | Ruta                                                         | Distancia |
|--------|-------------------------------------------|--------------------------------------------------------------|-----------|
| Madrid | Barcelona                                 | Madrid → Zaragoza → Barcelona                                |  621 km   |
| Sevilla| Bilbao                                    | Sevilla → Madrid → Bilbao                                    |  926 km   |
| Málaga | San Sebastián                             | Málaga → Granada → Córdoba → Madrid → Bilbao → San Sebastián | 1.182 km  |
 
---

## Cálculo del Costo de Bencina

> Costo estimado para recorrer la ruta en auto particular.

- Consumo: **8 litros / 100 km**
- Precio bencina España: **1,65 €/litro**
- Tipo de cambio: **1 EUR ≈ 1.170 CLP**

**Fórmula:**
```
litros = (km × 8) / 100
costo_eur = litros × 1.65
costo_clp = costo_eur × 1170
```
