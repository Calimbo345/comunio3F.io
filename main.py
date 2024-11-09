# Importaciones de la biblioteca estándar
import os
import threading
from datetime import datetime

# Importaciones de Flask
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, LoginManager, login_user, logout_user
# Importaciones de SQLArchemy
from sqlalchemy import func, desc, case
from sqlalchemy.exc import SQLAlchemyError, NoResultFound, MultipleResultsFound, IntegrityError
# Importaciones de Pyngrok
from pyngrok import ngrok
from pyngrok.exception import PyngrokNgrokError
import schedule

# Importaciones locales
import actualizar
import db
import calendario
from gestor import Gestor
from models import Usuario, Jugador
nombre_archivo = "noticias3F.txt"
# Configura el token de autenticación de ngrok
ngrok.set_auth_token("2mlXrgLmEcF2pI1rKH7fI71LY4N_5WoBcBBDCKW6ECwWZX71c")

app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'comprobar_Usuario'  # Reemplaza 'login' con el nombre de tu función de vista para el login


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Usuario).get(int(user_id))


@app.route("/login", methods=["POST"])
def login():
    gestor = Gestor()
    nombre = request.form.get('nombre')
    contrasena = request.form.get('contrasena')
    usuario = db.session.query(Usuario).filter_by(nombre=nombre).first()
    if usuario and gestor.comprobarUsuario(nombre, contrasena):
        login_user(usuario)
        return redirect(url_for('oficina'))
    else:
        flash('Credenciales inválidas')
        return redirect(url_for('pagina_principal'))


@app.route('/')
def pagina_principal():
    return render_template("index.html")


@app.route('/registro', methods=["GET", "POST"])
def crear_Usuario():
    if request.method == "POST":
        try:
            gestor = Gestor()
            nombre = request.form["nombre_nuevo"]
            contrasena = request.form["contrasena_nuevo"]
            nombre_equipo = request.form["nombre_equipo"]
            nombre_estadio = request.form["nombre_estadio_nuevo"]

            if not nombre or not contrasena or not nombre_estadio:
                flash("Todos los campos son obligatorios", "error")
                return redirect(url_for('pagina_principal'))

            hashed_password = contrasena
            nuevo_usuario = gestor.crearUsuario(nombre=nombre, contrasena=hashed_password, nombre_equipo=nombre_equipo,
                                                nombre_estadio=nombre_estadio)

            login_user(nuevo_usuario)
            flash("Usuario creado y sesión iniciada exitosamente", "success")
            return redirect(url_for('oficina', nombre_usuario=nombre))

        except Exception as e:
            flash(f"Error inesperado: {str(e)}", "error")
            return redirect(url_for('pagina_principal'))

    return render_template("index.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('pagina_principal'))


@app.route('/oficina', methods=["GET", "POST"])
@login_required
def oficina():
    gestor = Gestor()
    # Obtener el nombre del formulario y guardarlo en la sesión

    name = current_user.nombre
    # Manejar la selección del base
    if request.method == "POST":
        ahora = datetime.now()
        dia_actual = ahora.weekday()
        hora_actual = ahora.hour

        # Condición: se aplica de lunes a viernes antes de las 19:00
        if dia_actual < 4 or (dia_actual == 4 and hora_actual < 19):
            base_seleccionado = request.form.get('base_seleccionado')
            escolta_seleccionado = request.form.get('escolta_seleccionado')
            alero_seleccionado = request.form.get('alero_seleccionado')
            ala_pivot_seleccionado = request.form.get('ala_pivot_seleccionado')
            pivot_seleccionado = request.form.get('pivot_seleccionado')

            if base_seleccionado or escolta_seleccionado or alero_seleccionado or ala_pivot_seleccionado or pivot_seleccionado:
                quinteto = gestor.quintetoInicial(name, base_seleccionado, escolta_seleccionado,
                                                  alero_seleccionado, ala_pivot_seleccionado, pivot_seleccionado)
                print("\033[93mJUGADOR SELECCIONADO:\033[0m", quinteto)

    base_titular = db.session.query(Jugador.nombre).filter(
        (Jugador.contratado_por == name) & (Jugador.jugando_de == "BASE")).scalar()
    escolta_titular = db.session.query(Jugador.nombre).filter(
        (Jugador.contratado_por == name) & (Jugador.jugando_de == "ESCOLTA")).scalar()
    alero_titular = db.session.query(Jugador.nombre).filter(
        (Jugador.contratado_por == name) & (Jugador.jugando_de == "ALERO")).scalar()
    ala_pivot_titular = db.session.query(Jugador.nombre).filter(
        (Jugador.contratado_por == name) & (Jugador.jugando_de == "ALA-PIVOT")).scalar()
    pivot_titular = db.session.query(Jugador.nombre).filter(
        (Jugador.contratado_por == name) & (Jugador.jugando_de == "PIVOT")).scalar()
    banquillo = db.session.query(Jugador.nombre).filter(
        (Jugador.contratado_por == name) & (Jugador.jugando_de == "BANQUILLO")).all()

    print("\033[93mBASE:\033[0m", base_titular)
    print("\033[93mESCOLTA:\033[0m", escolta_titular)
    print("\033[93mALERO:\033[0m", alero_titular)
    print("\033[93mALA-PIVOT:\033[0m", ala_pivot_titular)
    print("\033[93mPIVOT:\033[0m", pivot_titular)
    print("\033[93mSUPLENTES:\033[0m", banquillo)
    datos_usuario = gestor.verTodosLosUsuarios()
    jugadores_usuario = gestor.verPlantilla(name)
    cantidad_jugadores = db.session.query(Jugador).filter(Jugador.contratado_por == name).all()
    subquery = (
        db.session.query(
            Usuario.nombre,
            Usuario.victorias,
            Usuario.derrotas,
            func.row_number().over(order_by=desc(Usuario.victorias)).label('posicion')
        )
        .order_by(desc(Usuario.victorias))
        .subquery()
    )

    posicion_liga = (
        db.session.query(subquery)
        .filter(subquery.c.nombre == name)
        .first()
    )
    print(posicion_liga)
    notificaciones = gestor.noticias()
    posicion = gestor.posiciones(name)
    if len(jugadores_usuario[0]) > 0:
        for usuario in datos_usuario:
            if name == usuario.nombre:
                presupuesto_formateado = f"{usuario.presupuesto:,.0f}".replace(",", ".")
                print(presupuesto_formateado)
                return render_template("oficina.html", nombre_usuario=usuario.nombre,
                                       nombre_estadio=usuario.nombre_estadio,
                                       nombre_equipo=usuario.nombre_equipo, presupuesto=presupuesto_formateado,
                                       jugadores_usuario=jugadores_usuario[0],
                                       valor_equipo=jugadores_usuario[1], noticias=notificaciones, bases=posicion[0],
                                       aleros=posicion[1], pivots=posicion[2],
                                       nombre_b=str(base_titular), nombre_e=escolta_titular, nombre_a=alero_titular,
                                       nombre_al=ala_pivot_titular, nombre_p=pivot_titular,
                                       banquillo=banquillo, nombre_liga=usuario.liga, cantidad=len(cantidad_jugadores),
                                       posicion=posicion_liga[3])
    else:
        for usuario in datos_usuario:
            if name == usuario.nombre:
                presupuesto_formateado = f"{usuario.presupuesto:,.0f}".replace(",", ".")
                return render_template("oficina.html", nombre_usuario=usuario.nombre,
                                       nombre_estadio=usuario.nombre_estadio,
                                       nombre_equipo=usuario.nombre_equipo, presupuesto=presupuesto_formateado)


@app.route('/mercado')
@login_required
def mercado():
    try:
        gestor = Gestor()
        datos = gestor.verTodosLosJugadores()
        jugadores = []
        for jugador, media in datos:
            jugadores.append({
                'nombre': jugador.nombre,
                'equipo': jugador.equipo,
                'lesion': jugador.lesion,
                'posicion': jugador.posicion,
                'valoracion': jugador.valoracion,
                'val_mercado': jugador.val_mercado,
                'media': media
            })
        return render_template("mercado.html", jugadores=jugadores)
    except Exception as e:
        app.logger.error(f"Error en la ruta /mercado: {str(e)}")
        return f"Error al cargar el mercado: CODIGO DE ERROR ==> 500\n {str(e)}", 500


@app.route('/compraventa', methods=["POST"])
@login_required
def comprar_jugador():
    if request.method == "POST":
        gestor = Gestor()
        user_name = current_user.nombre
        name_player = request.form.get("jugador_nombre")

        if not name_player:
            flash("Nombre de jugador no proporcionado", "error")
            return redirect(url_for('mercado'))

        try:
            ahora = datetime.now()
            dia_actual = ahora.weekday()
            hora_actual = ahora.hour

            # Condición: se aplica de lunes a viernes antes de las 19:00
            if dia_actual < 4 or (dia_actual == 4 and hora_actual < 19):

                compra_exitosa, mensaje = gestor.comprar_jugador(user_name, name_player)

                if compra_exitosa:
                    # Actualizar el usuario en la sesión
                    db.session.refresh(current_user)

                    flash(mensaje or "Jugador comprado con éxito", "success")
                    return redirect(url_for('oficina'))
                else:
                    flash(mensaje or "No se pudo completar la compra", "warning")
                    return redirect(url_for('mercado'))

        except SQLAlchemyError as e:
            db.session.rollback()
            app.logger.error(f"Error de base de datos en la compra: {str(e)}")
            flash("Error en la base de datos. Por favor, inténtelo de nuevo.", "error")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error inesperado en la compra: {str(e)}")
            flash(f"Error en la compra: {str(e)}", "error")

    return redirect(url_for('mercado'))


@app.route('/venta', methods=["POST", "GET"])
@login_required
def vender_jugador():
    try:
        gestor = Gestor()
        user_name = current_user.nombre
        name_player = request.form["jugador_nombre"]

        if not name_player:
            print("Nombre de jugador no proporcionado")
            flash("Nombre de jugador no proporcionado", "error")
            return redirect(url_for('oficina'))

        jugador = db.session.query(Jugador).filter(Jugador.nombre == name_player).first()

        if not jugador:
            print(f"No se encontró el jugador: {name_player}")
            flash(f"No se encontró el jugador: {name_player}", "error")
            return redirect(url_for('oficina'))
        ahora = datetime.now()
        dia_actual = ahora.weekday()
        hora_actual = ahora.hour

        # Condición: se aplica de lunes a viernes antes de las 19:00
        if dia_actual < 4 or (dia_actual == 4 and hora_actual < 19):
            venta_exitosa = gestor.venderJugador(str(user_name), name_player)

            if venta_exitosa:
                print("Jugador vendido con éxito")
                flash("Jugador vendido con éxito", "success")
            else:
                print("No se pudo completar la venta del jugador")
                flash("No se pudo completar la venta del jugador", "error")

        return redirect(url_for('oficina'))

    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error de base de datos: {str(e)}", "error")
        return redirect(url_for('oficina'))

    except Exception as e:
        db.session.rollback()
        flash(f"Error inesperado: {str(e)}", "error")
        return redirect(url_for('oficina'))


@app.route('/competicion', methods=["POST", "GET"])
@login_required
def competicion():
    gestor = Gestor()
    name = current_user.nombre
    if request.method == "POST":
        """nombre_liga = request.form["nombre_liga"]
        if nombre_liga:
            calendario.crear_liga(nombre_liga)
"""
        dia_actual = datetime.now().weekday()
        # Verificar si es un día entre lunes y viernes (0-4)
        if 0 <= dia_actual <= 4:
            unirse_liga = request.form["unirse_liga"]
            archivo = f"{unirse_liga}.xlsx"
            if os.path.exists(archivo) and unirse_liga:
                usuario = db.session.query(Usuario).filter(Usuario.nombre == name).first()
                if usuario:
                    calendario.unirse_a_liga(usuario.nombre_equipo, unirse_liga)
                    usuario.liga = unirse_liga
                    db.session.commit()

    nombre_liga = db.session.query(Usuario.liga).filter(Usuario.nombre == name).all()
    nombre = ""

    for liga_n in nombre_liga:
        if liga_n.liga:
            nombre = liga_n.liga
            lista_liga, orden_liga = gestor.verCompeticionClasificacion(nombre)
            enfrentamientos = calendario.mostrar_enfrentamientos(nombre, 1)

            # Crear un diccionario para mapear nombres de usuarios a sus posiciones
            posiciones = {usuario.nombre: usuario.posicion for usuario in orden_liga}

            if datetime.now().weekday() == 6:  # 6 representa el domingo (0 es lunes, 6 es domingo)
                for local, visitante in enfrentamientos:
                    try:
                        pts_l = db.session.query(
                            func.sum(
                                case(
                                    (Jugador.jugando_de == 'BANQUILLO', Jugador.valoracion * 0.8),
                                    else_=Jugador.valoracion)).label('val_total')).filter(
                            Jugador.contratado_por == local)
                        pts_v = db.session.query(
                            func.sum(
                                case(
                                    (Jugador.jugando_de == 'BANQUILLO', Jugador.valoracion * 0.8),
                                    else_=Jugador.valoracion)).label('val_total')).filter(
                            Jugador.contratado_por == visitante)

                    except SQLAlchemyError as e:
                        print(f"Error de base de datos: {e}")
                    except NoResultFound:
                        print("No se encontró ningún partido o usuario")
                    except MultipleResultsFound:
                        print("Se encontraron múltiples resultados donde se esperaba uno solo")
                    except IntegrityError:
                        print("Error de integridad en la base de datos")
                    except AttributeError as e:
                        print(f"Error de atributo: {e}")
                    except TypeError as e:
                        print(f"Error de tipo: {e}")
                    except Exception as e:
                        print(f"Error inesperado: {e}")
                    return schedule.CancelJob  # Cancela el trabajo después de ejecutarlo

            return render_template('competicion.html', lista_liga=lista_liga, posiciones=posiciones,
                                   calendario=enfrentamientos)


def actualizar_resultados_domingo():
    if datetime.now().weekday() == 6:  # Domingo
        schedule.logger.info("Iniciando actualización de resultados del domingo")
        try:
            # Obtener todas las ligas
            ligas = db.session.query(Usuario.liga).distinct().all()
            for liga in ligas:
                nombre_liga = liga.liga
                if nombre_liga:
                    jornada_fecha = actualizar.extraerJornadas()
                    enfrentamientos = calendario.mostrar_enfrentamientos(nombre_liga, jornada_fecha[1])

                    print(f"Enfrentamientos en {nombre_liga}: {enfrentamientos}")  # Imprimir enfrentamientos

                    for local, visitante in enfrentamientos:
                        try:
                            print("ENFRENTAMIENTO: ", local, visitante)
                            # Verificar si alguno es "Descanso"
                            if local == "Descanso" or visitante == "Descanso":
                                print("EL RESULTADO SERÁ: 0-0")
                                resultado_final = "0-0"
                                print(f"{local.upper()} 0-0 {visitante.upper()}")

                                # Guardar el resultado en el archivo Excel como 0-0
                                exito, ganador, perdedor = calendario.actualizar_resultado(nombre_liga, local,
                                                                                           visitante, "0", "0",
                                                                                           2)

                                if exito:
                                    print(
                                        f"Resultado actualizado exitosamente para {local} vs {visitante}: {resultado_final}")
                                else:
                                    print(f"No se pudo actualizar el resultado para {local} vs {visitante}.")
                                continue  # Saltar a la siguiente iteración del bucle

                            # Calcular puntos solo si ambos equipos no son "Descanso"
                            pts_l = db.session.query(func.sum(
                                case((Jugador.jugando_de == 'BANQUILLO', Jugador.valoracion * 0.8),
                                     else_=Jugador.valoracion)).label('val_total')).filter(
                                Jugador.contratado_por == local).scalar()

                            pts_v = db.session.query(func.sum(
                                case((Jugador.jugando_de == 'BANQUILLO', Jugador.valoracion * 0.8),
                                     else_=Jugador.valoracion)).label('val_total')).filter(
                                Jugador.contratado_por == visitante).scalar()

                            # Verificar si pts_l o pts_v son None
                            if pts_l is None or pts_v is None:
                                schedule.logger.warning(f"No se encontraron puntos para {local} o {visitante}")
                                pts_l = 0
                                pts_v = 0

                            # Redondear los valores
                            pts_l_rounded = round(pts_l) if pts_l is not None else 0
                            pts_v_rounded = round(pts_v) if pts_v is not None else 0

                            print(f"{local.upper()} {pts_l_rounded}-{pts_v_rounded} {visitante.upper()}")

                            # Actualizar el resultado en el calendario
                            exito, ganador, perdedor = calendario.actualizar_resultado(nombre_liga, local, visitante,
                                                                                       pts_l_rounded, pts_v_rounded, 2)
                            print("DATOS:", exito, ganador, perdedor)

                            if exito:
                                nombre_ganador = db.session.query(Usuario).filter(Usuario.nombre == ganador).first()
                                nombre_perdedor = db.session.query(Usuario).filter(Usuario.nombre == perdedor).first()

                                if nombre_ganador and nombre_perdedor:
                                    nombre_ganador.victorias += 1
                                    nombre_perdedor.derrotas += 1
                                else:
                                    schedule.logger.warning(f"No se encontró usuario para {ganador} o {perdedor}")
                        except SQLAlchemyError as e:
                            schedule.logger.error(f"Error en partido {local} vs {visitante}: {e}")

            """db.session.commit()"""
            schedule.logger.info("Actualización de resultados completada")
        except Exception as e:
            schedule.logger.error(f"Error general en actualización: {e}")
            db.session.rollback()


if __name__ == "__main__":
    try:
        public_url = ngrok.connect("5000")
        print(f' * Tunnel URL: {public_url}')

        if not os.path.exists(nombre_archivo):
            with open(nombre_archivo, "w") as archivo:
                print(f"Se ha creado el archivo '{nombre_archivo}'.")
        else:
            print(f"El archivo '{nombre_archivo}' ya existe.")

    except PyngrokNgrokError as e:
        print(f"Error al iniciar ngrok: {e}")
        print("La aplicación se ejecutará solo localmente.")

    # En la sigueinte linea estamos indicando a SQLAlchemy que cree, si no existen, las tablas
    # de todos los modulos que encuentre. Es importante que cuando se llegue a esta linea,
    # los modelos esten accesibles en este fichero main.py, esto se consigue con los imports
    # from models import Persona
    db.Base.metadata.create_all(bind=db.engine)

    # Inicia un hilo demonio para actualizar resultados periódicamente en segundo plano
    threading.Thread(target=actualizar_resultados_domingo, daemon=True).start()

    # Ejecuta la aplicación Flask
    app.run(host='0.0.0.0', port=5000, debug=True)

    " app.run(debug=True)"


