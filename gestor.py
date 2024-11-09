from sqlalchemy import text, desc, func, case, Float, cast
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import db
import bcrypt
import re
from models import Jugador, Usuario, UsuarioJugador
from datetime import date


class Gestor:
    archivo = "noticias.txt"


    def crearUsuario(self, nombre, contrasena, nombre_equipo, nombre_estadio):
        try:
            # Buscar si el usuario ya existe
            usuario_existente = db.session.query(Usuario).filter_by(nombre=nombre).first()
            if usuario_existente:
                print("EL NOMBRE DEL USUARIO YA EXISTE")
                return None

            # Verificar si la contraseña ya existe (si es necesario)
            contrasena_existente = db.session.query(Usuario).filter_by(contrasena=contrasena).first()
            if contrasena_existente:
                print("LA CONTRASEÑA YA ESTÁ EN USO")
                return None

            # Si no existe, crear el nuevo usuario
            contrasena_encode = contrasena.encode()
            salt = bcrypt.gensalt(15)
            hashed_contrasena = bcrypt.hashpw(contrasena_encode, salt)

            patron = re.compile(r'^\w{4,9}$')
            if patron.match(contrasena):
                print("COMTRASEÑA VALIDA")
                nuevo_usuario = Usuario(nombre=nombre, contrasena=hashed_contrasena, nombre_equipo=nombre_equipo,
                                        nombre_estadio=nombre_estadio,
                                        presupuesto=6000000)
                db.session.add(nuevo_usuario)
                db.session.commit()
                print("USUARIO CREADO")
                return nuevo_usuario
            else:
                print("CONTRASEÑA NO VALIDA")
                return None

        except IntegrityError:
            db.session.rollback()
            print("Error de integridad al crear el usuario.")
            return None

        except Exception as e:
            db.session.rollback()
            print(f"Error al crear el usuario: {str(e)}")
            return None
    def comprobarUsuario(self, nombre, contrasena):
        try:
            usuario = db.session.query(Usuario).filter(Usuario.nombre == nombre).first()
            if not usuario:
                print("Usuario no encontrado")
                return False

            # Asegurarse de que usuario.contrasena sea una cadena de texto
            contrasena_almacenada = usuario.contrasena
            if isinstance(contrasena_almacenada, bytes):
                contrasena_almacenada = contrasena_almacenada.decode('utf-8')

            # Verificar si la contraseña está hasheada con bcrypt
            if contrasena_almacenada.startswith('$2b$') or contrasena_almacenada.startswith('$2a$') or contrasena_almacenada.startswith('$2y$'):
                # La contraseña está hasheada con bcrypt
                print("ESTA HASEADA")
                isLogin = bcrypt.checkpw(contrasena.encode('utf-8'), usuario.contrasena)
                return isLogin
            else:
                # La contraseña está en texto plano (no recomendado)
                return contrasena_almacenada == contrasena

        except Exception as e:
            print(f"Error al comprobar usuario: {str(e)}")
            return False



    def verTodosLosUsuarios(self):
        print(" > VER TODOS LOS USUARIOS: ")
        """jugadores = db.session.query(Usuario).from_statement(text("SELECT * FROM usuarios;")).all()"""
        usuarios = db.session.query(Usuario).all()
        for x in usuarios:
            print("*" * 20)
            print(f">ID: {x.id} "
                  f"\n>NOMBRE: {x.nombre} ")
            print("*" * 20)
        return usuarios
    def anadirJugador(self, web_nombre, web_equipo, web_posicion, web_nacionalidad , web_lesion, web_valoracion, web_val_mercado, web_clausula):
        print(" > AÑADIR JUGADOR: ")
        try:
            # Primero, verificamos si el jugador ya existe
            jugador_existente = db.session.query(Jugador).filter_by(nombre=web_nombre).first()

            if jugador_existente:
                print(f"El jugador {web_nombre} ya existe en la base de datos.")
                return web_nombre, web_equipo, web_lesion, web_valoracion, web_val_mercado, web_clausula

            nombre = web_nombre
            equipo = web_equipo
            posicion = web_posicion
            nacionalidad = web_nacionalidad
            lesion = web_lesion
            valoracion = web_valoracion
            val_mercado = web_val_mercado
            clausula = web_clausula
            """formatear_clausula = f"{abs(clausula):,.0f}".replace(",", ".")"""

            jugador = Jugador(nombre, equipo, posicion, nacionalidad, lesion, valoracion, val_mercado, clausula)
            db.session.add(jugador)  # ==> INSERT INTO persona (nombre, edad, altura) VALUES ('Juan', 30, 175)
            db.session.commit()
            print("JUGADOR AÑADIDO")
            return nombre, equipo, lesion, valoracion, val_mercado, clausula

        except ValueError as e:
            print("ERROR: ENTRADA NO VÁLIDA. POR FAVOR, INTRODUCE EL TIPO DE DATO CORRECTO.")
            print(f"DETALLES DEL ERROR: {e}")
            db.session.rollback()
            return None

        except IntegrityError as e:
            print("ERROR DE INTEGRIDAD EN LA BASE DE DATOS.")
            print(f"DETALLES DEL ERROR: {e}")
            db.session.rollback()
            return None

        except SQLAlchemyError as e:
            print("ERROR AL EJECUTAR EL COMANDO SQL.")
            print(f"DETALLES DEL ERROR: {e}")
            db.session.rollback()
            return None

        except Exception as e:
            print("ERROR INESPERADO.")
            print(f"DETALLES DEL ERROR: {e}")
            db.session.rollback()
            return None

    def editarJugador(self):
        print(" > EDITAR JUGADOR: ")
        jugador_id = int(input("ID DEL JUGADOR: "))
        exist_player = db.session.query(Jugador).filter(Jugador.id == jugador_id).first()
        if exist_player is None:
            print("ERROR: EL JUGADOR INDICADO NO EXISTE")
        else:
            print(exist_player)
            try:
                editar_nombre = input("INTRODUCE EN NOMBRE DEL JUGADOR: ")
                editar_equipo = input("INTRODUCE EN NOMBRE DEL EQUIPO: ")
                editar_edad = int(input("INTRODUCE LA EDAD DEL JUGADOR: "))
                editar_partidos = int(input("INTRODUCE LOS PARTIDOS QUE HA JUGADO: "))
                editar_puntos = float(input("INTRODUCE LOS PUNTOS POR PARTIDO DEL JUGADOR: "))
                editar_tiros_2 = float(input("INTRODUCE LOS TIROS DE 2 DEL JUGADOR: "))
                editar_porcentaje_2 = float(input("INTRODUCE EL PORCENTAJE DE 2 DEL JUGADOR: "))
                editar_tiros_3 = float(input("INTRODUCE LOS TIROS DE 3 DEL JUGADOR: "))
                editar_porcentaje_3 = float(input("INTRODUCE EL PORCENTAJE DE 3 DEL JUGADOR: "))
                editar_rebotes = float(input("INTRODUCE LOS REBOTES DEL JUGADOR: "))
                editar_asistencias = float(input("INTRODUCE LAS ASISTENCIAS DEL JUGADOR: "))
                editar_b_recuperados = float(input("INTRODUCE LOS ROBOS DEL JUGADOR: "))
                editar_b_perdidos = float(input("INTRODUCE LAS PERDIDAS DEL JUGADOR: "))
                editar_t_favor = float(input("INTRODUCE LOS TAPONES A FAVOR DEL JUGADOR: "))
                editar_t_contra = float(input("INTRODUCE LOS TAPONES EN CONTRA DEL JUGADOR: "))
                editar_f_cometidas = float(input("INTRODUCE LAS FALTAS COMETIDAS DEL JUGADOR: "))
                editar_f_recibidas = float(input("INTRODUCE LAS FALTAS RECIBIDAS DEL JUGADOR: "))

                editar_valoracion = (editar_puntos + editar_rebotes + editar_asistencias + editar_b_recuperados + editar_t_favor + editar_f_recibidas) - (editar_b_perdidos + editar_t_contra + editar_f_cometidas)
                editar_val_mercado = editar_valoracion * 50000

                exist_player.nombre = editar_nombre
                exist_player.equipo = editar_equipo
                exist_player.edad = editar_edad
                exist_player.partidos = editar_partidos
                exist_player.puntos = editar_puntos
                exist_player.tiros_2 = editar_tiros_2
                exist_player.porcentaje_2 = editar_porcentaje_2
                exist_player.tiros_3 = editar_tiros_3
                exist_player.porcentaje_3 = editar_porcentaje_3
                exist_player.rebotes = editar_rebotes
                exist_player.asistencias = editar_asistencias
                exist_player.b_recuperados = editar_b_recuperados
                exist_player.b_perdidos = editar_b_perdidos
                exist_player.t_favor = editar_t_favor
                exist_player.t_contra = editar_t_contra
                exist_player.f_cometidas = editar_f_cometidas
                exist_player.f_recibidas = editar_f_recibidas
                exist_player.valoracion = editar_valoracion
                exist_player.val_mercado = editar_val_mercado

                db.session.commit()
                print("PERSONA ACTUALIZADA")
                return editar_nombre, editar_equipo, editar_edad, editar_partidos, editar_puntos, editar_tiros_2, editar_porcentaje_2, editar_tiros_3, editar_porcentaje_3, editar_rebotes, editar_asistencias, editar_b_recuperados, editar_b_perdidos, editar_t_favor, editar_t_contra, editar_f_cometidas, editar_f_recibidas, editar_valoracion, editar_val_mercado

            except ValueError as c:
                print("ERROR: ENTRADA NO VALIDA. POR FAVOR, INTRODUCE EL TIPO DE DATO CORRECTO.")
                print(f"DETALLES DEL ERROR: {c}")

    def eliminarJugador(self):
        print(" > ELIMINAR JUGADOR: ")
        jugador_id = int(input("ID DEL JUGADOR: "))
        exist_player = db.session.query(Jugador).filter(Jugador.id == jugador_id).first()
        if exist_player is None:
            print("ERROR: EL JUGADOR INDICADO NO EXISTE")
        else:
            db.session.delete(exist_player)  # ==>DELETE FROM persona WHERE id = ?
            db.session.commit()
            print("JUGADOR ELIMINADO")
            return exist_player



    def verTodosLosJugadores(self):
        print(" > VER TODOS LOS JUGADORES: ")
        """jugadores = db.session.query(Jugador).from_statement(text("SELECT * FROM jugadores_tercera_FEB ORDER BY 
        valoracion DESC;")).all()"""

        """jugadores = db.session.query(Jugador).filter(Jugador.contratado_por == None).order_by(desc(Jugador.valoracion)).all()"""
        jugadores = db.session.query(
            Jugador,
            func.round(
                case(
                    (Jugador.p_jugados > 0, cast(Jugador.val_total, Float) / Jugador.p_jugados),
                    else_=0
                ),
                1
            ).label('media')
        ).order_by(desc('media')).all()
        for x, media in jugadores:
            print("*" * 20)
            print(f">ID: {x.id} "
                f"\n>NOMBRE: {x.nombre} "
                f"\n>EQUIPO: {x.equipo} "
                f"\n>LESION: {x.lesion} "
                f"\n>VALORACIÓN: {x.valoracion} "
                f"\n>VALOR DE MERCADO: {x.val_mercado}€\n"
                  f"\n>MEDIA: {media}")
            print("*" * 20)
        return jugadores

    def verTodosLosUsuarios(self):
        print(" > VER TODOS LOS USUARIOS: ")
        usuarios = db.session.query(Usuario).from_statement(text("SELECT * FROM usuarios;")).all()
        "usuarios = db.session.query(Usuario).all()"
        for x in usuarios:
            print("*" * 20)
            print(f">ID: {x.id} "
                f"\n>NOMBRE: {x.nombre} ")
            print("*" * 20)
        return usuarios

    def buscarJugador(self):
        global jugadores
        busqueda = int(input("BUSCAR JUGADOR POR NOMBRE(1) , EQUIPO(2) , ESPECIFICO(3): "))
        while True:
            if busqueda == 1:
                try:
                    nombre = input("INTRODUCEN EL NOMBRE QUE ESTAS BUSCANDO: ")
                    jugadores = db.session.query(Jugador).filter(Jugador.nombre.ilike(f"%{nombre}%")).all()

                except Exception as e:
                    print("HA OCURRIDO UN ERROR INESPERADO.")
                    print(f"DETALLES DEL ERROR: {e}")
            elif busqueda == 2:
                try:
                    nombre_equipo = input("INTRODUCEN EL NOMBRE DEL EQUIPO QUE ESTAS BUSCANDO: ")
                    jugadores = db.session.query(Jugador).filter(Jugador.equipo.ilike(f"%{nombre_equipo}%")).all()

                except Exception as e:
                    print("HA OCURRIDO UN ERROR INESPERADO.")
                    print(f"DETALLES DEL ERROR: {e}")
            elif busqueda == 3:
                try:
                    comando = input("ESCRIBE EL COMANDO SQL: ")
                    jugadores = db.session.query(Jugador).from_statement(text(comando)).all()

                except SQLAlchemyError as e:
                    print("ERROR AL EJECUTAR EL COMANDO SQL.")
                    print(f"DETALLES DEL ERROR: {e}")
                    db.session.rollback()

                except Exception as e:
                    print("HA OCURRIDO UN ERROR INESPERADO.")
                    print(f"DETALLES DEL ERROR: {e}")
            else:
                print("ERROR: SOLICITUD NO ENCONTRADA")
            break

        for x in jugadores:
            print(
                f"\t >ID: {x.id} >NOMBRE: {x.nombre} >EDAD: {x.edad} >EQUIPO: {x.equipo} >VALORACIÓN: {format(x.valoracion, '.2f')} >VALOR DE MERCADO: {format(x.val_mercado, ',.0f').replace(',', '.')}€\n")

        return jugadores

    def comprar_jugador(self, usuario, jugador):
        # EXTRAEMOS EL NOMBRE DEL USUARIO, NOMBRE DEL JUGADOR Y EL ID
        nombre_usuario = db.session.query(Usuario).filter(Usuario.nombre == usuario).all()
        nombre_jugador = db.session.query(Jugador).filter(Jugador.nombre == jugador).all()
        jugadores_id = db.session.query(Jugador.id).filter(Jugador.nombre == jugador).scalar()

        # COMPROBAMOS SI EL JUGADOR ESTA CONTRATADO POR ALGUIEN
        jugadores_en_propiedad = db.session.query(Jugador).filter(Jugador.contratado_por == usuario).all()

        # COMPROBAMOS SI EL JUGADOR YA ESTÁ CONTRATADO POR OTRO USUARIO
        jugador_contratado = db.session.query(Jugador).filter(Jugador.nombre == jugador,
                                                              Jugador.contratado_por != None).first()

        if jugador_contratado and jugador_contratado.contratado_por != usuario:
            print(f"El jugador {jugador} ya está contratado por {jugador_contratado.contratado_por}")
            return None

        # EL NUMERO MAXIMO DE CONTRATACIONES POR USUARIO SERA 9
        limite_jugadores = len(jugadores_en_propiedad)
        if limite_jugadores < 9:
            print("NO SUPERAS EL LIMITE")
            if jugadores_id in [j.id for j in jugadores_en_propiedad]:
                print("LO TIENES EN PROPIEDAD")
                return None
            else:
                print("NO LO TIENES EN PROPIEDAD")
                for player, user_name in zip(nombre_jugador, nombre_usuario):
                    try:
                        if '.' in player.val_mercado:
                            # Si contiene puntos, asumimos que son separadores de miles
                            precio = float(player.val_mercado.replace('.', '').replace(',', '.'))
                        else:
                            # Si no contiene puntos, intentamos convertir directamente
                            precio = float(player.val_mercado.replace(',', '.'))
                    except ValueError:
                        print(f"Error al convertir '{player.val_mercado}' a float.")
                        precio = 0  # O cualquier otro valor predeterminado
                    if user_name.presupuesto - precio > 0:
                        print("se puede comprar")
                        nuevo_presupuesto = user_name.presupuesto - precio
                        user_name.presupuesto = nuevo_presupuesto
                        actualizar_usuario = UsuarioJugador(user_name.id, player.id, usuario, jugador, date.today(),
                                                            None)
                        adquisicion = db.session.query(Jugador).filter(Jugador.id == player.id).first()
                        adquisicion.jugando_de = "BANQUILLO"
                        print(actualizar_usuario)
                        adquisicion.contratado_por = usuario
                        db.session.add(actualizar_usuario)
                        db.session.commit()

                        with open("noticias3F.txt", "a") as archivo:
                            archivo.write(f"{usuario} compró a {player.nombre} por {player.val_mercado}€\n")
                    else:
                        print("no se pudo comprar")
        else:
            print("LIMITE DE JUGADORES SUPERADO")

    def venderJugador(self, usuario, jugador):
        nombre_usuario = db.session.query(Usuario).filter(Usuario.nombre == usuario).first()
        nombre_jugador = db.session.query(Jugador).filter(Jugador.contratado_por == usuario,
                                                          Jugador.nombre == jugador).first()

        if nombre_usuario and nombre_jugador:
            presupuesto = db.session.query(Usuario.presupuesto).filter(Usuario.nombre == usuario).scalar()
            valor_jugador = db.session.query(Jugador.val_mercado).filter(Jugador.nombre == jugador).scalar()
            usuario_id = nombre_usuario.id
            jugador_id = nombre_jugador.id


            if presupuesto is not None and valor_jugador is not None:
                nuevo_presupuesto = float(presupuesto) + float(valor_jugador.replace('.', ''))
                print("PRESUPUESTO",nuevo_presupuesto)
                print(type(nuevo_presupuesto))
                # Actualizar el presupuesto del usuario
                nombre_usuario.presupuesto = nuevo_presupuesto

                # Liberar al jugador
                nombre_jugador.contratado_por = ""
                nombre_jugador.jugando_de = ""
                nombre_jugador.titular = False

                """# Verificar si ya existe un registro
                existing_record = db.session.query(UsuarioJugador).filter_by(
                    usuario_id=usuario_id, jugador_id=jugador_id
                ).first()

                if existing_record:
                    print(f"Ya existe un registro para usuario_id={usuario_id} y jugador_id={jugador_id}")
                    return False"""

                #Actualizamos el registro de USUARIJUGADORCOMO OBTENGO TAMBIEN EL ID DEL USUARIO Y DEL JUGADOR?
                try:
                    """nuevo_registro = UsuarioJugador(
                        usuario_id=int(usuario_id),
                        jugador_id=int(jugador_id),
                        nombre_usuario=usuario,
                        nombre_jugador=jugador,
                        fecha_adquisicion=None,
                        fecha_venta=date.today()
                    )"""
                    registro = UsuarioJugador(usuario_id, jugador_id, usuario, jugador, None, date.today())
                    venta = db.session.query(Jugador).filter(Jugador.id == jugador_id).first()
                    venta.contratado_por = None
                    with open("noticias3F.txt", "a") as archivo:
                        archivo.write(f"{usuario} vendió a {nombre_jugador.nombre} por {nombre_jugador.val_mercado}€\n")

                    db.session.add(registro)
                    # Guardar los cambios en la base de datos
                    db.session.commit()

                    print(f"Jugador {jugador} vendido. Nuevo presupuesto de {usuario}: {nuevo_presupuesto}")
                    return True

                except IntegrityError as e:
                    db.session.rollback()
                    print(f"Error al añadir el registro de venta: {str(e)}")
                    return False

            else:
                print("Error: No se pudo obtener el presupuesto o el valor del jugador.")
                return False
        else:
            print(
                f"No se pudo vender el jugador. Verifique que el usuario {usuario} exista y que sea dueño del jugador {jugador}.")
            return False


    def verPlantilla(self, nombre):
        # Primero, obtén el ID del usuario basado en el nombre
        jugadores = db.session.query(Jugador).filter(Jugador.contratado_por == nombre).all()
        usuario = db.session.query(UsuarioJugador).all()
        valor_equipo =[]
        print("Numero de jugadores:",len(jugadores))
        if len(jugadores) > 0:
            for user_name in usuario:
                print("ID DEL USUARIO: ", user_name.usuario_id)
                if user_name.nombre_usuario == nombre:
                    # Extraer los IDs de la lista de tuplas
                    ids = [jugador.id for jugador in jugadores]

                    # Obtener los detalles de los jugadores
                    plantilla = db.session.query(Jugador). \
                        filter(Jugador.id.in_(ids)). \
                        all()
                    lista_jugadores = {"NOMBRE": "",
                                       "POSICION": "",
                                       "VAL_MERCADO": 0,
                                       "VALORACION": 0}

                    if plantilla:
                        print(f"Plantilla de {nombre}:")
                        for jugador in plantilla:
                            print(f"Nombre: {jugador.nombre}")
                            print(f"Posición: {jugador.posicion}")
                            print(f"Equipo: {jugador.equipo}")
                            print("--------------------")
                            lista_jugadores[f"{jugador.nombre}"] = {"POSICION": jugador.posicion,
                                                                    "VAL_MERCADO": jugador.val_mercado,
                                                                    "VALORACION": jugador.val_semana}

                            if isinstance(jugador.val_mercado, str):
                                print(f"{jugador.val_mercado} es un string")
                                valor_formateado = float(jugador.val_mercado.replace('.', '').replace(',', '.'))
                                valor_equipo.append(valor_formateado)

                            elif isinstance(jugador.val_mercado, int):
                                print(f"{jugador.val_mercado} es un integer")
                                valor_equipo.append(jugador.val_mercado)

                            elif isinstance(jugador.val_mercado, float):
                                print(f"{jugador.val_mercado} es un float")
                                valor_equipo.append(jugador.val_mercado)

                    suma = sum(valor_equipo)

                    numero_formateado = "{:,.0f}".format(suma).replace(",", ".")
                    print("PRECIO: ", numero_formateado)
                    return lista_jugadores, numero_formateado
                else:
                    print(f"No se encontraron jugadores en la plantilla de {nombre}")
                    lista_jugadores = {"NOMBRE": "",
                                       "POSICION": "",
                                       "VAL_MERCADO": "",
                                       "VALORACION":""}
        else:
            print(f"No hay jugadores en la plantilla de {nombre}")
            lista_jugadores = {"NOMBRE": "",
                               "POSICION": "",
                               "VAL_MERCADO": "",
                               "VALORACION": ""}
            suma = sum(valor_equipo)
            numero_formateado = "{:,.0f}".format(suma).replace(",", ".")
            return lista_jugadores, numero_formateado

    def noticias(self):
        lista_noticias = []
        try:
            with open("noticias3F.txt", "r") as archivo:
                # Leer todas las líneas y guardarlas en una lista
                lineas = archivo.readlines()

                # Obtener las últimas líneas (hasta 5)
                ultimas_lineas = lineas[-5:] if len(lineas) > 5 else lineas

                for linea in reversed(ultimas_lineas):
                    # Eliminar espacios en blanco y saltos de línea extras
                    noticia = linea.strip()
                    lista_noticias.append(noticia)

        except FileNotFoundError:
            print("El archivo 'noticias3F.txt' no existe.")

        return lista_noticias

    def posiciones(self, usuario):
        bases = db.session.query(Jugador.nombre).filter(
            (Jugador.posicion == "BASE") & (Jugador.contratado_por == usuario) & (Jugador.titular == False)
        ).all()
        aleros = db.session.query(Jugador.nombre).filter(
            (Jugador.posicion == "ALERO") & (Jugador.contratado_por == usuario) & (Jugador.titular == False)
        ).all()
        pivots = db.session.query(Jugador.nombre).filter(
            (Jugador.posicion == "PIVOT") & (Jugador.contratado_por == usuario) & (Jugador.titular == False)
        ).all()

        # Extraer solo los nombres de las tuplas
        bases = [base[0] for base in bases]
        aleros = [alero[0] for alero in aleros]
        pivots = [pivot[0] for pivot in pivots]

        print("BASES: ", bases)
        print("ALEROS: ", aleros)
        print("PIVOTS: ", pivots)
        return bases, aleros, pivots

    def quintetoInicial(self, usuario, nuevo_base=None, nuevo_escolta=None, nuevo_alero=None, nuevo_ala_pivot=None,
                        nuevo_pivot=None):
        jugadores = db.session.query(Jugador).filter(
            (Jugador.contratado_por == usuario) &
            (Jugador.jugando_de.in_(
                ["BASE", "ESCOLTA", "ALERO", "ALA-PIVOT", "PIVOT", "BANQUILLO"]) | Jugador.jugando_de.is_(None))
        ).all()

        nombre_base = ""
        nombre_escolta = ""
        nombre_alero = ""
        nombre_ala_pivot = ""
        nombre_pivot = ""

        if nuevo_base is not None:
            base = db.session.query(Jugador).filter(Jugador.nombre == nuevo_base).first()
            if base and base.titular and base.jugando_de == "BASE":
                print("EL BASE QUE HAS SELECCIONADO YA ES TITULAR")
            else:
                for jugador in jugadores:
                    if jugador.jugando_de == "BASE" and jugador.titular:
                        jugador.titular = False
                        jugador.jugando_de = "BANQUILLO"
                if base:
                    base.titular = True
                    base.jugando_de = "BASE"
                    nombre_base = base.nombre

        if nuevo_escolta is not None:
            escolta = db.session.query(Jugador).filter(Jugador.nombre == nuevo_escolta).first()
            if escolta and escolta.titular and escolta.jugando_de == "ESCOLTA":
                print("EL ESCOLTA QUE HAS SELECCIONADO YA ES TITULAR")
            else:
                for jugador in jugadores:
                    if jugador.jugando_de == "ESCOLTA" and jugador.titular:
                        jugador.titular = False
                        jugador.jugando_de = "BANQUILLO"
                if escolta:
                    escolta.titular = True
                    escolta.jugando_de = "ESCOLTA"
                    nombre_escolta = escolta.nombre

        if nuevo_alero is not None:
            alero = db.session.query(Jugador).filter(Jugador.nombre == nuevo_alero).first()
            if alero and alero.titular and alero.jugando_de == "ALERO":
                print("EL ALERO QUE HAS SELECCIONADO YA ES TITULAR")
            else:
                for jugador in jugadores:
                    if jugador.jugando_de == "ALERO" and jugador.titular:
                        jugador.titular = False
                        jugador.jugando_de = "BANQUILLO"
                if alero:
                    alero.titular = True
                    alero.jugando_de = "ALERO"
                    nombre_alero = alero.nombre

        if nuevo_ala_pivot is not None:
            ala_pivot = db.session.query(Jugador).filter(Jugador.nombre == nuevo_ala_pivot).first()
            if ala_pivot and ala_pivot.titular and ala_pivot.jugando_de == "ALA-PIVOT":
                print("EL ALA-PIVOT QUE HAS SELECCIONADO YA ES TITULAR")
            else:
                for jugador in jugadores:
                    if jugador.jugando_de == "ALA-PIVOT" and jugador.titular:
                        jugador.titular = False
                        jugador.jugando_de = "BANQUILLO"
                if ala_pivot:
                    ala_pivot.titular = True
                    ala_pivot.jugando_de = "ALA-PIVOT"
                    nombre_ala_pivot = ala_pivot.nombre

        if nuevo_pivot is not None:
            pivot = db.session.query(Jugador).filter(Jugador.nombre == nuevo_pivot).first()
            if pivot and pivot.titular and pivot.jugando_de == "PIVOT":
                print("EL PIVOT QUE HAS SELECCIONADO YA ES TITULAR")
            else:
                for jugador in jugadores:
                    if jugador.jugando_de == "PIVOT" and jugador.titular:
                        jugador.titular = False
                        jugador.jugando_de = "BANQUILLO"
                if pivot:
                    pivot.titular = True
                    pivot.jugando_de = "PIVOT"
                    nombre_pivot = pivot.nombre

        db.session.commit()
        return nombre_base, nombre_escolta, nombre_alero, nombre_ala_pivot, nombre_pivot

    def verCompeticionClasificacion(self, nombre_liga):
        orden_liga = (
            db.session.query(
                Usuario.nombre,
                Usuario.victorias,
                Usuario.derrotas,
                func.row_number().over(order_by=desc(Usuario.victorias)).label('posicion')
            )
            .order_by(desc(Usuario.victorias))
            .all()
        )
        lista_liga = db.session.query(Usuario).filter( Usuario.liga == nombre_liga).all()
        if lista_liga:
            return lista_liga, orden_liga

