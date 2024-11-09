import requests
import db
import time
from bs4 import BeautifulSoup
from models import Jugador
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime


def actualizarJugador(urls_semana):
    for url in urls_semana:
        web_game = f"https://baloncestoenvivo.feb.es/partido/{url}"

        response = requests.get(web_game)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            nameplayers = soup.find_all("td", class_="nombre jugador")
            valplayer = soup.find_all("td", class_="valoracion")
            url_local = soup.find_all(id="_ctl0_MainContentPlaceHolderMaster_equipoLocalNombre")
            url_visitante = soup.find_all(id="_ctl0_MainContentPlaceHolderMaster_equipoVisitanteNombre")

            for local, visitante in zip(url_local, url_visitante):
                print(f"\033[93m{local.text.strip()}\033[0m - \033[93m{visitante.text.strip()}\033[0m")

            for nombre, valoracion in zip(nameplayers, valplayer):
                nombre_completo = nombre.text.strip()
                val = valoracion.text.strip()

                # Manejo de posibles errores en el formato del nombre
                try:
                    print(nombre_completo)
                    apellido, nombre = nombre_completo.split(',', 1)
                except ValueError:
                    print(f"Error en el formato del nombre: {nombre_completo}")
                    continue

                # Búsqueda del jugador en la base de datos
                jugador = db.session.query(Jugador).filter(
                    Jugador.nombre.ilike(f"%{apellido}%{nombre}%")
                ).first()

                if jugador:
                    jugador.val_semana = int(val)
                    jugador.val_total += jugador.val_semana

                    if jugador.val_semana > 0:
                        print(f"EL VALOR DE MERCADO SUBIRA UN {jugador.val_semana}% PARA: {jugador.nombre}")
                        precio = float(jugador.val_mercado.replace('.', '').replace(',', '.'))
                        incremento = (precio * jugador.val_semana) / 100
                        nuevo_precio = precio + incremento
                        formatear_precio = f"{abs(nuevo_precio):,.0f}".replace(",", ".")
                        formatear_incremento = f"{abs(incremento):,.0f}".replace(",", ".")
                        jugador.val_mercado = formatear_precio
                        partido_jugado = int(jugador.p_jugados) + 1
                        jugador.p_jugados = partido_jugado
                        db.session.commit()
                        print("*" * 10)
                        print("VALORACIÓN DE LA SEMANA: ", jugador.val_semana)
                        print("INCREMENTO: ", formatear_incremento, "€")
                        print(f"PRECIO ANTIGUO: {abs(precio):,.0f} €".replace(",", "."))
                        print("NUEVO PRECIO: ", formatear_precio, "€")
                        print("*" * 10)

                    elif jugador.val_semana < 0:
                        print(f"EL VALOR DE MERCADO BAJARÁ UN {jugador.val_semana}% PARA: {jugador.nombre}")
                        precio = float(jugador.val_mercado.replace('.', '').replace(',', '.'))
                        decremento = (precio * jugador.val_semana) / 100
                        nuevo_precio = precio - decremento
                        formatear_precio = f"{abs(nuevo_precio):,.0f}".replace(",", ".")
                        jugador.val_mercado = formatear_precio
                        partido_jugado = int(jugador.p_jugados) + 1
                        jugador.p_jugados = partido_jugado
                        db.session.commit()
                        print("*" * 10)
                        print("NOMBRE DEL JUGADOR: ", jugador.nombre)
                        print("VALORACIÓN DE LA SEMANA: ", jugador.val_semana)
                        print("DECREMENTO: ", decremento, "€")
                        print("PRECIO ANTIGUO: ", precio, "€")
                        print("NUEVO PRECIO: ", formatear_precio, "€")
                        print("*" * 10)

                else:
                    print(f"NO SE ENCONTRO A: {nombre_completo}")


def reajuste():
    global media_valoracion
    urls = [922176, 921919, 922177, 922212, 923507, 922825, 921852, 922865, 922861, 921475, 922866, 922174, 923002,
            922864,
            922484, 922868, 921853, 922824, 922867, 922698, 921476, 922862, 922826, 922823, 921672, 922822, 923001,
            921854]

    for url in urls:
        web = f"https://baloncestoenvivo.feb.es/estadisticasacumuladas/{url}"
        response = requests.get(web)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            nameplayers = soup.find_all("td", class_="nombre jugador")
            valplayer = soup.find_all("td", class_="valoracion")
            game_players = soup.find_all("td", class_="partidos")

            for nombre, valoracion, partidos in zip(nameplayers, valplayer, game_players):
                try:
                    print(nombre.text.strip(), type(int(valoracion.text.strip())), type(int(partidos.text.strip())))
                except:
                    print(f"ERROR: No se pudo castear al jugador{nombre.text.strip()}")
                try:
                    valoracion_p = int(valoracion.text.strip())
                except ValueError:
                    print(f"No se pudo convertir '{valoracion.text.strip()}' a un entero")
                    valoracion_p = 0  # O cualquier valor predeterminado
                try:
                    partidos = int(partidos.text.strip())
                except ValueError:
                    print(f"Error: No se pudo convertir 'game' a entero para {nombre.text.strip()}")
                    partidos = 0

                if partidos != 0:
                    media_valoracion = round(valoracion_p / partidos, 1)
                else:
                    print("ESTADISTICAS ACUMULADAS DEL EQUIPO")

                val_mercado = round(media_valoracion * 70000)
                clausula = round(media_valoracion * 100000)
                formate_val = f"{abs(val_mercado):,.0f}".replace(",", ".")
                formate_clausula = f"{abs(clausula):,.0f}".replace(",", ".")
                nombre_completo = nombre.text.strip()
                val = valoracion.text.strip()
                jugador = db.session.query(Jugador).filter(Jugador.nombre == nombre_completo).first()
                if jugador:
                    try:
                        jugador.valoracion = media_valoracion
                        jugador.val_mercado = formate_val
                        jugador.clausula = formate_clausula
                        db.session.commit()
                    except:
                        db.session.rollback()
                        break


def extraerJornadas():
    lista_partidos = []
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # Configurar el driver de Selenium (asegúrate de tener el driver correcto instalado)
    driver = webdriver.Chrome(options=chrome_options)  # O usa Firefox, Safari, etc.

    # Navegar a la página web
    web_jornada = "https://baloncestoenvivo.feb.es/resultados/ligaeba/57/2024"
    driver.get(web_jornada)
    response = requests.get(web_jornada)
    jornada_actual = 0

    try:
        soup_jornada = BeautifulSoup(response.text, "html.parser")
        select_element = soup_jornada.find('select', id='_ctl0_MainContentPlaceHolderMaster_jornadasDropDownList')

        # Encuentra todos los elementos option dentro del select
        options = select_element.find_all('option')


        for option in options:
            fecha = option.text.strip()
            jornada = fecha.split()[1].split('(')[0]
            value = option['value']
            fecha_jornada = fecha.split('(')[-1].strip(')')

            # Convertir fecha_jornada a objeto datetime
            fecha_comparar = datetime.strptime(fecha_jornada, '%d/%m/%Y')

            # Obtener la fecha de hoy
            fecha_hoy = datetime.now().date()
            # INDICA EL DIA DE HOY
            fecha_hoy_str = fecha_hoy.strftime('%d/%m/%Y')
            print(f"FECHA DE HOY: {fecha_hoy_str}")
            print(f"FECHA DE LA JORNADA: {fecha_jornada}")
            if fecha_jornada == fecha_hoy_str:
                print("ACTUALIZA LOS DATOS DE LOS PARTIDOS")
                jornada_actual = jornada
                # Esperar a que se cargue el select de jornadas
                wait = WebDriverWait(driver, 10)
                select_element = wait.until(
                    EC.presence_of_element_located((By.ID, "_ctl0_MainContentPlaceHolderMaster_jornadasDropDownList")))

                # Crear un objeto Select
                select = Select(select_element)
                # AÑADIR UN BUCLE FOR MAÑANA PARA INTRODUCIR LOS VALUES DE LAS JORNADAS
                # Seleccionar la opción específica por su valor
                select.select_by_value(value)  # Valor para Jornada 4(03/11/2024)

                # Esperar a que se actualice el contenido
                time.sleep(2)  # Ajusta este tiempo según sea necesario

                # Obtener el HTML actualizado
                html = driver.page_source

                # Usar BeautifulSoup para analizar el HTML
                soup = BeautifulSoup(html, "html.parser")
                for i in range(2, 9):
                    jornadas = soup.find_all(
                        id=f"_ctl0_MainContentPlaceHolderMaster_jornadaDataGrid__ctl{i}_resultadoHyperLink")
                    for x in jornadas:
                        print(x.text.strip() != "*-*")
                        if x.text.strip() != "*-*":
                            href = x.get('href')
                            if href:
                                url_str = str(href)
                                numero_partido = url_str.split("=")[-1]
                                lista_partidos.append(numero_partido)
                                print(f"JORNADA {jornada} ==> NUMERO DEL PARTIDO:{numero_partido}\n")
            else:
                print("La fecha no coincide con ninguna jornada")  # Este caso nunca ocurrirá

            print("--------------------")
    except:
        print("ERROR: AL INTRODUCIR LOS DATOS")
    print(lista_partidos)
    return lista_partidos, jornada_actual



urls = extraerJornadas()
actualizarJugador(urls[0])

