FROM base_proyectos:latest

RUN apt-get install python3 python3-pip -y

RUN pip install --no-cache-dir pandas numpy pyodbc streamlit pyautogui

RUN mkdir appStreamlit

COPY app.py /appStreamlit

COPY funciones.py /appStreamlit

EXPOSE 8501

# ENTRYPOINT ["streamlit", "run", "/appStreamlit/app.py", "--server.port=8501", "--server.address=0.0.0.0"]0
ENTRYPOINT ["streamlit", "run", "/appStreamlit/app.py", "--server.port=8501"]
