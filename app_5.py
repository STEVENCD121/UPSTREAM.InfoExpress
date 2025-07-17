
import pandas as pd
import streamlit as st

def cargar_datos(ruta_csv):
    try:
        df = pd.read_csv(ruta_csv, dtype=str)
        df["Lote"] = df["Lote"].str.strip()
        df["Tipo de Hidrocarburo"] = df["Tipo de Hidrocarburo"].str.strip()
        df["Año"] = df["Año"].str.extract(r'(\d{4})')[0].astype(int)
        columnas_numericas = [
            'Reservas Probadas (P1)', 'Reservas Probables (P2)', 'Reservas Posibles (P3)',
            'Reservas Totales (3P)', 'Recursos Contingentes (2C)', 'Recursos Prospectivos (2U)',
            'Producción', 'Inversion', 'Regalia', 'Canon'
        ]
        for col in columnas_numericas:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        return df
    except FileNotFoundError:
        st.error(f"Error: No se encontró el archivo {ruta_csv}.")
    except Exception as e:
        st.error(f"Error al cargar datos: {e}")
    return None

def format_df(df):
    return df.applymap(lambda x: f"{x:,.2f}" if isinstance(x, float) else x)

def mostrar_reservas_recursos(df, lote, hidrocarburo):
    año = 2023
    columnas = {
        'Reservas Probadas (P1)': 'P1',
        'Reservas Probables (P2)': 'P2',
        'Reservas Posibles (P3)': 'P3',
        'Reservas Totales (3P)': 'Reservas Totales (3P)',
        'Recursos Contingentes (2C)': '2C',
        'Recursos Prospectivos (2U)': '2U'
    }
    unidades = {
        "Petróleo": "Petróleo (MMBBL)",
        "Gas": "Gas (TCF)",
        "LGN": "LGN (MMBBL)"
    }

    df_f = df[(df["Año"] == año) &
              (df["Tipo de Hidrocarburo"] == hidrocarburo) &
              (df["Lote"] == lote)]
    filas, vol_lote, vol_pais = [], [], []

    for col, etiqueta in columnas.items():
        vl = df_f[col].sum() / 1000
        vp = df[(df["Año"] == año) & (df["Tipo de Hidrocarburo"] == hidrocarburo)][col].sum() / 1000
        filas.append(etiqueta)
        vol_lote.append(round(vl, 2))
        vol_pais.append(round(vp, 2))

    if all(v == 0 for v in vol_lote):
        st.warning(f"No hay reservas ni recursos para el lote '{lote}' - {hidrocarburo}.")
        return

    df_res = pd.DataFrame({
        "Clasificación": filas,
        "Volumen": vol_lote,
        "País": vol_pais
    })
    df_res["%Participación"] = (df_res["Volumen"] / df_res["País"] * 100).round(2)

    st.markdown(f"<h3>{unidades[hidrocarburo]} - Lote: {lote}</h3>", unsafe_allow_html=True)
    st.table(format_df(df_res))

def mostrar_produccion(df, lote, hidrocarburo):
    unidades = {
        "Petróleo": "Petróleo (BPD)",
        "Gas": "Gas (MMPCD)",
        "LGN": "LGN (BPD)"
    }
    años = [2021, 2022, 2023, 2024, 2025]
    fila_l, fila_p, fila_pct = [], [], []

    for año in años:
        df_f = df[(df["Año"] == año) & (df["Tipo de Hidrocarburo"] == hidrocarburo)]
        vl = df_f[df_f["Lote"] == lote]["Producción"].sum()
        vp = df_f["Producción"].sum()
        fila_l.append(round(vl, 2))
        fila_p.append(round(vp, 2))
        fila_pct.append(round(vl / vp * 100, 2) if vp > 0 else 0)

    if all(v == 0 for v in fila_l):
        st.warning(f"No hay producción registrada para el lote '{lote}' - {hidrocarburo}.")
        return

    df_res = pd.DataFrame({"Clasificación": ["Lote", "País", "%Participación"]})
    for i, año in enumerate(años):
        df_res[str(año)] = [fila_l[i], fila_p[i], fila_pct[i]]

    st.markdown(f"<h3>{unidades[hidrocarburo]} - Lote: {lote}</h3>", unsafe_allow_html=True)
    st.table(format_df(df_res))

def mostrar_inversion(df, lote):
    años = [2021, 2022, 2023, 2024, 2025]
    fila_l, fila_p, fila_pct = [], [], []

    for año in años:
        df_f = df[df["Año"] == año]
        vl = df_f[df_f["Lote"] == lote]["Inversion"].sum()
        vp = df_f["Inversion"].sum()
        fila_l.append(round(vl, 2))
        fila_p.append(round(vp, 2))
        fila_pct.append(round(vl / vp * 100, 2) if vp > 0 else 0)

    if all(v == 0 for v in fila_l):
        st.warning(f"No hay inversión registrada para el lote '{lote}'.")
        return None

    df_res = pd.DataFrame({"Clasificación": ["Lote", "País", "%Participación"]})
    for i, año in enumerate(años):
        df_res[str(año)] = [fila_l[i], fila_p[i], fila_pct[i]]
    return format_df(df_res)

def mostrar_regalias(df, lote):
    años = [2021, 2022, 2023, 2024, 2025]
    fila_l, fila_p, fila_pct = [], [], []

    for año in años:
        df_f = df[df["Año"] == año]
        vl = df_f[df_f["Lote"] == lote]["Regalia"].sum()
        vp = df_f["Regalia"].sum()
        fila_l.append(round(vl, 2))
        fila_p.append(round(vp, 2))
        fila_pct.append(round(vl / vp * 100, 2) if vp > 0 else 0)

    if all(v == 0 for v in fila_l):
        st.warning(f"No hay regalías registradas para el lote '{lote}'.")
        return None

    df_res = pd.DataFrame({"Clasificación": ["Lote", "País", "%Participación"]})
    for i, año in enumerate(años):
        df_res[str(año)] = [fila_l[i], fila_p[i], fila_pct[i]]
    return format_df(df_res)

def mostrar_canon(df, lote):
    años = [2021, 2022, 2023, 2024, 2025]
    fila_l, fila_p, fila_pct = [], [], []

    for año in años:
        df_f = df[df["Año"] == año]
        vl = df_f[df_f["Lote"] == lote]["Canon"].sum()
        vp = df_f["Canon"].sum()
        fila_l.append(round(vl, 2))
        fila_p.append(round(vp, 2))
        fila_pct.append(round(vl / vp * 100, 2) if vp > 0 else 0)

    if all(v == 0 for v in fila_l):
        st.warning(f"No hay cánones registrados para el lote '{lote}'.")
        return None

    df_res = pd.DataFrame({"Clasificación": ["Lote", "País", "%Participación"]})
    for i, año in enumerate(años):
        df_res[str(año)] = [fila_l[i], fila_p[i], fila_pct[i]]
    return format_df(df_res)

def main():
    st.markdown('<p style="text-align: right; font-size: 12px;">by Ing. Steven Cipra</p>', unsafe_allow_html=True)
    st.title("Principales Cifras UPSTREAM por Lote - Perú")

    df = cargar_datos("Integrado.csv")
    if df is None:
        return

    lote = st.text_input("¿De qué Lote necesitas información?").strip()
    if not lote:
        st.info("Por favor, ingresa un lote para continuar.")
        return

    hidrocarburos = ["Petróleo", "Gas", "LGN"]

    # Subtítulos con viñetas y tamaño un poco menor que el título (aprox h3)
    subtitulos_con_viñeta = [
        "RESERVAS Y RECURSOS DE HIDROCARBUROS (Año 2023)",
        "PRODUCCIÓN FISCALIZADA DE HIDROCARBUROS",
        "INVERSIÓN (MMUSD)",
        "REGALÍA (MMUSD)",
        "CANON (MMUSD)"
    ]

    # Mostrar Reservas y Recursos
    st.markdown(f'<h3>• {subtitulos_con_viñeta[0]}</h3>', unsafe_allow_html=True)
    for h in hidrocarburos:
        mostrar_reservas_recursos(df, lote, h)

    # Mostrar Producción Fiscalizada
    st.markdown(f'<h3>• {subtitulos_con_viñeta[1]}</h3>', unsafe_allow_html=True)
    for h in hidrocarburos:
        mostrar_produccion(df, lote, h)

    # Mostrar Inversión
    df_inv = mostrar_inversion(df, lote)
    if df_inv is not None:
        st.markdown(f'<h3>• {subtitulos_con_viñeta[2]}</h3>', unsafe_allow_html=True)
        st.table(df_inv)

    # Mostrar Regalía
    df_reg = mostrar_regalias(df, lote)
    if df_reg is not None:
        st.markdown(f'<h3>• {subtitulos_con_viñeta[3]}</h3>', unsafe_allow_html=True)
        st.table(df_reg)

    # Mostrar Canon
    df_can = mostrar_canon(df, lote)
    if df_can is not None:
        st.markdown(f'<h3>• {subtitulos_con_viñeta[4]}</h3>', unsafe_allow_html=True)
        st.table(df_can)

if __name__ == "__main__":
    main()
