import pandas as pd
import numpy as np
import pyodbc

def consultaTienda(tienda):
    sql_con = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=148.245.208.249,1538;DATABASE=AgoSorianaHist;UID=usrBIVentas;PWD=@goXc8rW;')
    tsql = f'''
    SELECT
        E.Clasificacion Categoria,
        D.Clasificacion SubCategoria,
        C.Clasificacion Segmento,
        B.Clasificacion SubSegmento,
        A.UPC, A.Descripcion, A.Frentes
    FROM (
        SELECT
            A.*,
            B.PROD_NAME Descripcion, B.CATEGORY
        FROM (
            SELECT A.UPCERR UPC, COUNT(A.UPCERR) Frentes
            FROM tbl_PositionRealogramaMonitoreo A
                JOIN (
                    SELECT A.IdRealograma
                    FROM tbl_RealogramaMonitoreo A
                        JOIN (
                            SELECT TOP 1 Clave_Tienda IdTienda, Evento
                            FROM tbl_BitacoraTiendasProcesadas
                            WHERE Clave_Tienda = {tienda} AND Tienda_Cerrada = 1
                            ORDER BY Evento DESC
                        ) B ON A.IdTienda = B.IdTienda AND A.Evento = B.Evento
                ) B ON A.IdRealograma = B.IdRealograma
            GROUP BY A.UPCERR
        ) A
            LEFT JOIN cat_Productos B ON A.UPC = B.UPC
    ) A
        LEFT JOIN cat_Categorias B ON A.CATEGORY = B.ClaveClasificacion
        LEFT JOIN cat_Categorias C ON B.OrgNode.GetAncestor(1) = C.OrgNode
        LEFT JOIN cat_Categorias D ON B.OrgNode.GetAncestor(2) = D.OrgNode
        LEFT JOIN cat_Categorias E ON B.OrgNode.GetAncestor(3) = E.OrgNode
    WHERE B.Clasificacion != 'Raiz'
    ORDER BY Categoria, SubCategoria, Segmento, SubSegmento, Descripcion
    '''
    dfProductos = pd.read_sql(tsql, sql_con)

    tsql = f'''
    SELECT
        B.Tienda,
        C.Formato,
        A.Clave_Tienda IdTienda, Evento,
        CAST(A.Fecha_Inicio_Monitoreo AS DATE) [Inicio Monitoreo],
        CAST(A.Fecha_Fin_Monitoreo AS DATE) [Fin Monitoreo],
        CAST(A.Fecha_Tienda_Cerrada AS DATE) [Cierre Tienda]
    FROM (
        SELECT TOP 1 *
        FROM tbl_BitacoraTiendasProcesadas
        WHERE Clave_Tienda = {tienda} AND Tienda_Cerrada = 1
        ORDER BY Evento DESC
    ) A
        JOIN cat_Tiendas B ON A.Clave_Tienda = B.IdTienda
        JOIN cat_Formatos C ON B.IdFormato = C.IdFormato
    '''
    dfTienda = pd.read_sql(tsql, sql_con)

    return dfProductos, dfTienda