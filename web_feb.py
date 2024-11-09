import requests
from bs4 import BeautifulSoup
from gestor import Gestor

urls =[952151,952029,951349,950668,951084,952343,951794,952159,951278,951062,952228,951397]

for equipo in urls:
    web = f"https://baloncestoenvivo.feb.es/estadisticasacumuladas/{equipo}"
    response = requests.get(web)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        nameplayers = soup.find_all("td", class_="nombre jugador")
        team = soup.find("div", class_="wrapper-text")
        game_players = soup.find_all("td", class_="partidos")
        minut_game = soup.find_all("td", class_="minutos")
        point_game = soup.find_all("td", class_="puntos")
        t2 = soup.find_all("td", class_="tiros dos")
        porcentaje_t2 = soup.find_all("td", class_="tiros dos")
        t3 = soup.find_all("td", class_="tiros tres")
        porcentaje_t3 = soup.find_all("td", class_="tiros tres")
        tiros_campo = soup.find_all("td", class_="tiros campo")
        porcentaje_tc = soup.find_all("td", class_="tiros campo")
        tiros_libres = soup.find_all("td", class_="tiros libres")
        porcentaje_tl = soup.find_all("td", class_="tiros libres")
        rebotes_o = soup.find_all("td", class_="rebotes ofensivos")
        rebotes_d = soup.find_all("td", class_="rebotes defensivos")
        rebotes_t = soup.find_all("td", class_="rebotes total")
        asistencias = soup.find_all("td", class_="asistencias")
        b_robados = soup.find_all("td", class_="recuperaciones")
        b_perdidos = soup.find_all("td", class_="recuperaciones")
        t_favor = soup.find_all("td", class_="tapones favor")
        t_contra = soup.find_all("td", class_="tapones contra")
        mates = soup.find_all("td", class_="mates")
        f_cometida = soup.find_all("td", class_="faltas cometidas")
        f_recibida = soup.find_all("td", class_="faltas recibidas")
        valoracion = soup.find_all("td", class_="valoracion")

        #NO HACE FALTA METER EN EL BUCLE FOR LA VARIBALE EQUIPO YA QUE NO VARIA DE JUGADOR DEL MISMO EQUIPO
        equipo = team.find("span").text.strip()
        gestor = Gestor()
        for a, b, c, d, e, f, g, h, i, k, l, m, n, o, p, q, r, s, t, u, v, w, x in zip(nameplayers, game_players, minut_game, point_game, t2, porcentaje_t2, t3, porcentaje_t3, tiros_campo, tiros_libres, porcentaje_tl, rebotes_o, rebotes_d, rebotes_t,asistencias, b_robados, b_perdidos, t_favor, t_contra, mates,f_cometida,f_recibida, valoracion):
            name = a.text.strip()
            game = b.text.strip()
            minut = c.text.strip()
            point = d.text.strip()
            p_t2 = f.find("span").text.strip()
            p_t3 = h.find("span").text.strip()
            p_tc = i.find("span").text.strip()
            p_tl = l.find("span").text.strip()
            o_rebounds = m.text.strip()
            d_rebounds = n.text.strip()
            t_rebounds = o.text.strip()
            asist = p.text.strip()
            s_ball = q.text.strip()
            l_ball = r.text.strip()
            b_favor = s.text.strip()
            b_against = t.text.strip()
            dunk = u.text.strip()
            foul_c = v.text.strip()
            foul_r = w.text.strip()
            val = x.text.strip()



    #TRIOS DE 2P
            try:
                metidos_2p , resto_2p = e.text.strip().split("/")
                fallados_2p = resto_2p.split()[0]
            except ValueError:
                metidos_2p, fallados_2p = "0", "0"

    #TIROS DE 3P
            try:
                metidos_3p , resto_3p = g.text.strip().split("/")
                fallados_3p = resto_3p.split()[0]
            except ValueError:
                metidos_3p, fallados_3p = "0", "0"

    #TIROS DE CAMPO
            try:
                metidos_tc , resto_tc = i.text.strip().split("/")
                fallados_tc = resto_tc.split()[0]
            except ValueError:
                metidos_tc, fallados_tc = "0", "0"

    # TIROS LIBRES
            try:
                metidos_tl, resto_tl = k.text.strip().split("/")
                fallados_tl = resto_tl.split()[0]
            except ValueError:
                metidos_tl, fallados_tl = "0", "0"

    #CASTEAR EL VALOR DE PARTIDOS JUGADOS A INT
            try:
                partidos = int(game)
            except ValueError:
                print(f"Error: No se pudo convertir 'game' a entero para {name}")
                partidos = 0

    #CASTEAR EL VALOR DE PUNTOS POR PARTIDO A INT
            try:
                puntos = int(point)
            except ValueError:
                print(f"Error: No se pudo convertir 'point' a entero para {name}")
                puntos = 0

    # CASTEAR EL VALOR DE ASISTENCIAS POR PARTIDO A INT
            try:
                asis = int(asist)
            except ValueError:
                print(f"Error: No se pudo convertir 'point' a entero para {name}")
                asis = 0

    # CASTEAR EL VALOR DE (REBOTES) POR PARTIDO A INT
            try:
                rebT = int(t_rebounds)
            except ValueError:
                print(f"Error: No se pudo convertir 'point' a entero para {name}")
                rebT = 0

    # CASTEAR EL VALOR DE VALORACION A INT
            try:
                valoracion_p = int(val)
            except ValueError:
                print(f"Error: No se pudo convertir 'point' a entero para {name}")
                valoracion_p = 0

    #EN CASO DE QUE NO HAYA VALORES NO LO TENDRA EN CUENTA Y LO MOSTRARÁ POR PANTALLA CON DATOS VACIOS
            if partidos != 0:
               media_puntos = round(puntos / partidos, 1)
               media_valoracion = round(valoracion_p / partidos, 1)
            else:
               print("ESTADISTICAS ACUMULADAS DEL EQUIPO")


            val_mercado =round(media_valoracion * 70000)
            clausula = float(media_valoracion * 100000)
            formate_clausula = f"{abs(clausula):,.0f}".replace(",", ".")
            formate_val = f"{abs(val_mercado):,.0f}".replace(",", ".")
            datos_jugador = gestor.anadirJugador(name, equipo, "BASE", "ESPAÑOL", "",media_valoracion, str(formate_val),formate_clausula)

            print(f"NOMBRE: \033[32m{ name }\033[0m"
                  f"\nEQUIPO: \033[32m{ equipo }\033[0m"
                  f"\nPOSICIÓN: \033[32m{ "BASE" }\033[0m"
                  f"\nNACIONALIDAD: \033[32m{ "ESPAÑOL" }\033[0m"
                  f"\nLESIÓN: \033[32m{ "" }\033[0m"
                  f"\nVALORACIÓN: \033[32m{media_valoracion}\033[0m"
                  f"\nVALOR DE MERCADO: \033[32m{formate_val}€\033[0m"
                  f"\nCLAUSULA DE RESCISIÓN: \033[32m{formate_clausula}€\033[0m"
                  )
            print("-" * 50)

    else:
        print("ERROR AL CARGAR LA PAGINA WEB, CODIGO: ", response.status_code)






