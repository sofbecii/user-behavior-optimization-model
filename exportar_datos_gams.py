"""
MA2001B - Optimización determinista
Generación de archivos GAMS para calcular los pesos de los 13 atributos
de juegos serios siguiendo la metodología de Pacheco-Velazquez et al. (2024)
"International Journal of Serious Games" 11(4), 41-54.

Lee la pestaña "Calificaciones" de los tres Excel producidos por
procesamiento_encuesta.py y genera tres modelos LP en formato GAMS:

  gams/pesos_hombres.gms   (segmento masculino)
  gams/pesos_mujeres.gms   (segmento femenino)
  gams/pesos_ambos.gms     (ambos géneros combinados)

Cada modelo:
  Min Z = sum_i (L_i + E_i)
  s.a.  sum_k F_k * X_{i,k} + L_i - E_i = GOE_i      i = 1..N
        sum_k F_k = 1
        0.03 <= F_k <= 0.50                          k = 1..13
        L_i, E_i >= 0
"""

from pathlib import Path
import pandas as pd

# ── Configuración ────────────────────────────────────────────────────────────
DIR_BASE = Path(__file__).parent
DIR_SALIDA = DIR_BASE / "gams"

ARCHIVOS = {
    "hombres": "resultados_encuesta_hombres.xlsx",
    "mujeres": "resultados_encuesta_mujeres.xlsx",
    "ambos":   "resultados_encuesta.xlsx",
}

ATRIBUTOS = [
    "Desafío",
    "Retroalimentación",
    "Inmersión",
    "Concentración",
    "Claridad de objetivos",
    "Autonomía",
    "Interacción social",
    "Mejora del conocimiento",
    "Involucramiento emocional",
    "Equilibrio entre habilidades y tareas",
    "Narrativa atractiva",
    "Estructura de progresión",
    "Animación y sonido",
]
COL_GLOBAL = "Calificación Global"

# Cotas del modelo 2 del artículo
F_MIN = 0.03
F_MAX = 0.50


# ── Construcción del archivo GAMS ────────────────────────────────────────────

def construir_gams(segmento: str, df: pd.DataFrame) -> str:
    """Devuelve el contenido completo de un archivo .gms para el segmento dado."""
    n = len(df)
    k = len(ATRIBUTOS)
    etiquetas_k = [f"F{j+1}" for j in range(k)]

    encabezado = (
        f"$TITLE Pesos de atributos de juegos serios - segmento {segmento}\n"
        f"$OFFLISTING\n"
        f"$OFFSYMXREF\n"
        f"$OFFSYMLIST\n\n"
        f"* Modelo de programacion lineal basado en:\n"
        f"*   Pacheco-Velazquez, E. et al. (2024). A Linear Programming\n"
        f"*   Methodology for Evaluating Game Attributes in Serious Games.\n"
        f"*   IJSG 11(4), pp. 41-54.\n"
        f"*\n"
        f"* Segmento: {segmento}    N encuestados: {n}    Atributos: {k}\n"
        f"* Atributos (orden de columnas):\n"
    )
    for j, nombre in enumerate(ATRIBUTOS):
        encabezado += f"*   F{j+1:<2} = {nombre}\n"
    encabezado += "\n"

    # SETS
    sets_block = (
        f"SETS\n"
        f"    i  encuestados   /1*{n}/\n"
        f"    k  atributos     /F1*F{k}/;\n\n"
    )

    # TABLE de calificaciones X(i,k)
    ancho = 6
    cabecera_tabla = " " * 8 + "".join(f"{lbl:>{ancho}}" for lbl in etiquetas_k)
    filas_tabla = []
    for idx, fila in enumerate(df[ATRIBUTOS].itertuples(index=False, name=None), start=1):
        valores = "".join(f"{int(v):>{ancho}}" for v in fila)
        filas_tabla.append(f"{idx:>7} {valores}")
    tabla = (
        "TABLE X(i,k) calificacion del atributo k por el encuestado i\n"
        + cabecera_tabla + "\n"
        + "\n".join(filas_tabla)
        + "\n;\n\n"
    )

    # PARAMETER GOE(i)
    goe_lineas = []
    for idx, val in enumerate(df[COL_GLOBAL].astype(int).tolist(), start=1):
        goe_lineas.append(f"    {idx:>5}  {val}")
    parametro_goe = (
        "PARAMETER GOE(i) calificacion global del juego /\n"
        + "\n".join(goe_lineas)
        + "\n/;\n\n"
    )

    # Modelo
    modelo = """\
VARIABLES
    F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13
    Z;

POSITIVE VARIABLES
    F1, F2, F3, F4, F5, F6, F7, F8, F9, F10, F11, F12, F13
    L(i), E(i);

EQUATIONS
    OBJ          funcion objetivo
    BAL(i)       balance lineal por encuestado
    SUMA         los pesos suman uno;

* Funcion objetivo: minimizar suma de holguras
OBJ.. Z =E= sum(i, L(i) + E(i));

* Balance lineal por encuestado (modelo del articulo, Ec. 5)
BAL(i)..  F1*X(i,'F1')  + F2*X(i,'F2')  + F3*X(i,'F3')
        + F4*X(i,'F4')  + F5*X(i,'F5')  + F6*X(i,'F6')
        + F7*X(i,'F7')  + F8*X(i,'F8')  + F9*X(i,'F9')
        + F10*X(i,'F10') + F11*X(i,'F11') + F12*X(i,'F12')
        + F13*X(i,'F13')
        + L(i) - E(i) =E= GOE(i);

* Los pesos suman 100 por ciento (Ec. 6)
SUMA.. F1 + F2 + F3 + F4 + F5 + F6 + F7
     + F8 + F9 + F10 + F11 + F12 + F13 =E= 1;

* Cotas del modelo 2 del articulo: 3 por ciento <= F_k <= 50 por ciento
F1.LO = 0.03;  F1.UP = 0.50;
F2.LO = 0.03;  F2.UP = 0.50;
F3.LO = 0.03;  F3.UP = 0.50;
F4.LO = 0.03;  F4.UP = 0.50;
F5.LO = 0.03;  F5.UP = 0.50;
F6.LO = 0.03;  F6.UP = 0.50;
F7.LO = 0.03;  F7.UP = 0.50;
F8.LO = 0.03;  F8.UP = 0.50;
F9.LO = 0.03;  F9.UP = 0.50;
F10.LO = 0.03; F10.UP = 0.50;
F11.LO = 0.03; F11.UP = 0.50;
F12.LO = 0.03; F12.UP = 0.50;
F13.LO = 0.03; F13.UP = 0.50;

MODEL PESOS /ALL/;
SOLVE PESOS USING LP MINIMIZING Z;

DISPLAY F1.L,  F2.L,  F3.L,  F4.L,  F5.L,  F6.L,  F7.L,
        F8.L,  F9.L,  F10.L, F11.L, F12.L, F13.L, Z.L;
"""

    return encabezado + sets_block + tabla + parametro_goe + modelo


# ── Carga de datos ───────────────────────────────────────────────────────────

def cargar_calificaciones(ruta_xlsx: Path) -> pd.DataFrame:
    """Lee la pestaña 'Calificaciones' y conserva solo filas con datos completos."""
    df = pd.read_excel(ruta_xlsx, sheet_name="Calificaciones")
    columnas = ATRIBUTOS + [COL_GLOBAL]
    df = df[columnas].dropna()
    df = df.astype(int)
    return df.reset_index(drop=True)


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    DIR_SALIDA.mkdir(exist_ok=True)
    print("=" * 60)
    print("  Generación de modelos GAMS para pesos de atributos")
    print("=" * 60)

    for segmento, archivo in ARCHIVOS.items():
        ruta_xlsx = DIR_BASE / archivo
        df = cargar_calificaciones(ruta_xlsx)
        contenido = construir_gams(segmento, df)
        ruta_salida = DIR_SALIDA / f"pesos_{segmento}.gms"
        ruta_salida.write_text(contenido, encoding="utf-8")
        print(f"  {segmento:8s} -> {ruta_salida.name}  ({len(df)} encuestados)")

    print(f"\nArchivos GAMS escritos en: {DIR_SALIDA}")


if __name__ == "__main__":
    main()
