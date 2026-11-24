import pandas as pd

# =====================
# REGLA DE DISTRIBUCIÓN
# =====================
def calcular_distribucion(n_asesores, cvs, nombre=None, rol=None):

    cvs = str(cvs).upper()
    nombre = str(nombre).upper() if nombre else ""
           
    # ==================================================
    # ==================================================
    # 🔴 REGLA ESPECIAL FRONTINO
    # ==================================================
    if cvs in ["SEGOVIA"]:
        if rol == "LIDER":
            return 0.50
        else:
            return 0.50

    # ==================================================
    # ==================================================
    # TERMINAL NORTE
    # ==================================================

    if cvs == "TERMINAL NORTE":

        # Líder
        if rol == "LIDER":
            return 454 / 2200

        # Luz
        elif "LUZ" in nombre:
            return 125 / 2200

        # Diana
        elif "DIANA" in nombre:
            return 753 / 2200

        # Maria
        elif "MARIA" in nombre:
            return 868 / 2200

    # ==================================================
    # CALDAS
    # ==================================================

    if cvs == "CALDAS":

        # Líder
        if rol == "LIDER":
            return 724 / 3700

        # Yolima
        elif "YOLIMA" in nombre:
            return 201 / 3700

        # Johnson
        elif "JOHNSON" in nombre:
            return 1287 / 3700

        # Darinela
        elif "DARINELA" in nombre:
            return 1287 / 3700

    # ==================================================
    # GIRARDOTA
    # ==================================================

    if cvs == "GIRARDOTA":

        # Líder
        if rol == "LIDER":
            return 383 / 2000

        #  Narelig
        elif "NARELIG" in nombre:
            return 1617 / 2000

    # ==================================================
    # DABEIBA
    # ==================================================

    if cvs == "DABEIBA":

        # Líder
        if rol == "LIDER":
            return 1075 / 1200

        # Yeilisa Fernanda
        elif "YEILISA" in nombre:
            return 125 / 1200

    # ==================================================
    # FRONTINO
    # ==================================================

    if cvs == "FRONTINO":

        # Líder
        if rol == "LIDER":
            return 1211 / 2400

        # Yeilisa Fernanda
        elif "YEILISA" in nombre:
            return 1189 / 2400

    # ==================================================
    # LA ESTRELLA
    # ==================================================

    if cvs == "LA ESTRELLA":

        # Líder
        if rol == "LIDER":
            return 940 / 1200

        # Jhon
        elif "JHON" in nombre:
            return 104 / 1200

        # Yeilisa Fernanda
        elif "YEILISA" in nombre:
            return 156 / 1200

    # ==================================================
    # ENVIGADO
    # ==================================================

    if cvs == "ENVIGADO":

        # Líder
        if rol == "LIDER":
            return 944 / 3500

        # Luz
        elif "LUZ" in nombre:
            return 1415 / 3500

        # Diana
        elif "DIANA" in nombre:
            return 1141 / 3500  

    # ==================================================
    # BARBOSA
    # ==================================================

    if cvs == "BARBOSA":

        # Líder
        if rol == "LIDER":
            return 400 / 2400

        # Sara
        elif "SARA" in nombre:
            return 560 / 2400

        # Evelis
        elif "EVELIS" in nombre:
            return 1440 / 2400  


    # ==================================================
    # 🔴 REGLAS NORMALES
    # ==================================================

    # Si no hay asesores
    if n_asesores == 0:
        return 1.0

    if rol == "LIDER":

        if n_asesores == 1:
            return 0.40
        elif n_asesores == 2:
            return 0.25
        elif n_asesores >= 3:
            return 0.20

    else:

        if n_asesores == 1:
            return 0.60
        elif n_asesores == 2:
            return 0.375
        elif n_asesores >= 3:
            return 0.266

    return 1.0


# =================================================
# META GENERAL + EJECUCIÓN (RESUMEN POR CVS)
# =================================================
def resumen_meta_general_por_cvs(df):
    resultados = []

    for sucursal, grupo in df.groupby("Sucursal"):
        meta_total = grupo["Meta_General"].iloc[0]

        n_asesores = grupo[grupo["Rol"] == "ASESOR"]["Cedula_Vendedor"].nunique()
        pct_lider, pct_asesores = calcular_distribucion(n_asesores, sucursal)


        puntos_lider = grupo[grupo["Rol"] == "LIDER"]["Puntos"].sum()
        puntos_asesores = grupo[grupo["Rol"] == "ASESOR"]["Puntos"].sum()

        resultados.append({
            "Sucursal": sucursal,
            "Estructura": f"1 Líder + {n_asesores} Asesor(es)",

            "Meta CVS": meta_total,

            "Meta Líder": meta_total * pct_lider,
            "Ejecutado Líder": puntos_lider,
            "Cumplimiento Líder %": round(
                (puntos_lider / (meta_total * pct_lider)) * 100, 2
            ) if meta_total * pct_lider > 0 else 0,

            "Meta Asesores": meta_total * pct_asesores,
            "Ejecutado Asesores": puntos_asesores,
            "Cumplimiento Asesores %": round(
                (puntos_asesores / (meta_total * pct_asesores)) * 100, 2
            ) if meta_total * pct_asesores > 0 else 0,
        })

    return pd.DataFrame(resultados)


# =================================================
# KPI POR PRODUCTO + EJECUCIÓN (RESUMEN POR CVS)
# =================================================
def resumen_kpi_producto_por_cvs(df):
    resultados = []

    for (sucursal, producto), grupo in df.groupby(["Sucursal", "Producto"]):
        meta_producto = grupo["Meta_Producto"].iloc[0]

        n_asesores = grupo[grupo["Rol"] == "ASESOR"]["Cedula_Vendedor"].nunique()
        pct_lider, pct_asesores = calcular_distribucion(n_asesores, sucursal)


        puntos_lider = grupo[grupo["Rol"] == "LIDER"]["Puntos"].sum()
        puntos_asesores = grupo[grupo["Rol"] == "ASESOR"]["Puntos"].sum()

        resultados.append({
            "Sucursal": sucursal,
            "Producto": producto,

            "Meta Producto": meta_producto,

            "Meta Líder": meta_producto * pct_lider,
            "Ejecutado Líder": puntos_lider,
            "Cumplimiento Líder %": round(
                (puntos_lider / (meta_producto * pct_lider)) * 100, 2
            ) if meta_producto * pct_lider >= 0 else 0,

            "Meta Asesores": meta_producto * pct_asesores,
            "Ejecutado Asesores": puntos_asesores,
            "Cumplimiento Asesores %": round(
                (puntos_asesores / (meta_producto * pct_asesores)) * 100, 2
            ) if meta_producto * pct_asesores >= 0 else 0,
        })

    return pd.DataFrame(resultados)
