# import pyautogui
from funciones import consultaTienda
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="random",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get help': 'mailto:mesaayudaago@agoconsultores.com.mx',
        'Report a bug': None,
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

@st.cache
def exportar_csv(df):
    return df.to_csv(index=None)

st.title('Consulta de productos auditados')

tienda = st.number_input('Escribe el no. de tienda', key='input_tienda', step=1)

if tienda == 0:
    pass

else:
    try:
        resumen, detalle = consultaTienda(tienda)
        if len(detalle) == 0:
            st.write('Esa tienda no existe, por favor consulta otra')
        else:
            st.write('A continuación se muestran los productos auditados en la última visita a la tienda:')
            st.subheader(f'{detalle.Tienda.head(1).values[0]} ({detalle.Formato.head(1).values[0]})')
            tab1, tab2 = st.tabs(['Resumen','Detalle'])
            with tab1:
                st.write(detalle[['Inicio Monitoreo','Fin Monitoreo','Cierre Tienda']])
                st.write(pd.DataFrame(data = {'UPCs auditados': [len(resumen)], 'Frentes leídos': [resumen.Frentes.sum()]}))
            with tab2:
                st.download_button(
                    'Exportar a CSV',
                    exportar_csv(resumen[['Categoria','SubCategoria','Segmento','SubSegmento','UPC','Descripcion','Frentes']]),
                    'Productos.csv',
                    'text/csv'
                )
                st.dataframe(resumen[['Categoria','SubCategoria','Segmento','SubSegmento','UPC','Descripcion','Frentes']])

    except Exception as e:
        st.write('Ha habido un error, por favor comunique el siguiente código a mesaayudaago@agoconsultores.com.mx', e)
        pass

    # btn_reiniciar = st.button('Reiniciar')
    # if btn_reiniciar:
    #     pyautogui.hotkey("ctrl","F5")