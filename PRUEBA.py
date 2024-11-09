from gestor import Gestor
import calendario
from datetime import datetime
import main



gestor = Gestor()
"""gestor.verPlantilla("admin2")"""
"""print(gestor.comprar_jugador("admin", "LORENZO MEDINA, JEREMY DUKESY"))"""
"""print(gestor.verTodosLosJugadores())"""
"""print(gestor.crearUsuario("admin","1234","Torreon"))"""
"""gestor.comprobarUsuario("admin1","admin")"""
"""gestor.venderJugador("admin", "SOLE MOURATAY, MAXIMILLIANO AGKOUSTIN")"""
"""gestor.verTodosLosJugadores()"""
"""a = gestor.noticias()
print(a)"""
"""a = gestor.posiciones("admin")
print(a[1])"""
"""print(gestor.quintetoInicial("admin",nuevo_escolta="RUEDA ALVAREZ, DIEGO"))"""
"""a = gestor.verCompeticionClasificacion("MOSTOLETA-LIEGUE")
for usuario in a[1]:
    print(usuario[3])"""
"""calendario.crear_liga("MOSTOLETA-LIEGUE")
a = calendario.generar_calendario("MOSTOLETA-LIEGUE")
print(a)
"""
"""a = calendario.unirse_a_liga("admin","MOSTOLETA-LIEGUE")
print(a)

a = calendario.mostrar_enfrentamientos("MOSTOLETA-LIEGUE",1)
for local, visitante, pts_local, pts_visitante in a:
    print(f"{local} {pts_local}-{pts_visitante} {visitante}")"""
"""a = 0.1 + 0.2
print(round(a,2))"""
"print(datetime.now())"
"""print(calendario.actualizar_resultado("MOSTOLETA-LIEGUE","admin","Descanso",68,0,1))"""
"print(main.actualizar_resultados_domingo())"
"""anadir = gestor.anadirJugador("RIGA, LOUIS NEA FRANCOIS",
                              "FUNDACIÓN CB CANARIAS",
                              "ALERO",
                              "FRANCIA",
                              None,
                              6.6,
                              "462.000",
                              "660.000")"""
print(gestor.verTodosLosJugadores())
