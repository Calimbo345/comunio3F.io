import db
from sqlalchemy import Column,Integer,String,Float, Boolean, Date
from sqlalchemy.orm import relationship
from datetime import date
from flask_login import UserMixin




class Usuario(UserMixin,db.Base):
    __tablename__ = "usuarios"
    __table_args__ = {"sqlite_autoincrement": True}

    # CON __SLOTS__ REDUCIMOS EL CONSUMO DE MEMORIA PERO PUEDE CAUSARPROBLEMAS
    #YA QUE SQLALCHEMY NO ESTA DISEÑADA PARA TRABAJAR ÓPTIMAMENTE
    """ __slots__ = (
        'id', 'nombre', 'contrasena', 'nombre_estadio', 'presupuesto',
        'liga', 'puesto', 'jugadores_asociacion',
        '_sa_instance_state'
    )"""

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False, unique=True)
    contrasena = Column(String, nullable=False)
    nombre_equipo = Column(String, nullable=False)
    nombre_estadio = Column(String, nullable=False)
    presupuesto = Column(Float, nullable=False, default=6000000)
    liga = Column(String,default='')
    puesto = Column(Integer,default=0)
    victorias = Column(Integer,default=0)
    derrotas = Column(Integer,default=0)

    def __init__(self, nombre, contrasena, nombre_equipo, nombre_estadio, presupuesto=6000000,liga='',puesto=0,victorias=0,derrotas=0):#LE HE QUITADO EL ATRIBUTO ID POSIBLEMENTE DE ERRORES
        self.nombre = nombre
        self.contrasena = contrasena
        self.nombre_equipo = nombre_equipo
        self.nombre_estadio = nombre_estadio
        self.presupuesto = presupuesto
        self.liga = liga
        self.puesto = puesto
        self.victorias = victorias
        self.derrotas = derrotas

    def get_id(self):
        return str(self.id)

    def __str__(self):
        return (f"__DATOS DEL USUSARIO__\n"
                f"NOMBRE: {self.nombre}\n"
                f"CONTRASEÑA: {self.contrasena}\n"
                f"NOMBRE DEL EQUIPO: {self.nombre_equipo}\n"
                f"NOMBRE DEL ESTADIO: {self.nombre_estadio}\n"
                f"PRESUPUESTO: {self.presupuesto}\n")

    def __repr__(self):
        return f'<Usuario {self.nombre}>'
class Jugador(db.Base):
#ORM(MAPEO DE OBJETOS RELACIONADOS)
    __tablename__ = "jugadores_tercera_FEB"
    __table_args__ = {"sqlite_autoincrement": True}#OPCIONAL: Es una forma para garantizar que el valor de la PK sea unica y no se reutilice
    id = Column(Integer,primary_key=True)#Automaticamente esta PK se convierte en autoincremental
    nombre = Column(String, nullable=False, default="¿¿??", unique=True)
    equipo = Column(String, nullable=False, default="¿¿??")
    posicion = Column(String, nullable=False, default="¿¿??")
    nacionalidad = Column(String, nullable=False, default="¿¿??")
    lesion = Column(String, nullable=False, default=False)
    valoracion = Column(Float, nullable=False, default=0)
    val_mercado = Column(String, nullable=False, default=0)
    clausula = Column(String, nullable=False, default=0)
    contratado_por = Column(String)
    titular = Column(Boolean, default=False)
    jugando_de = Column(String)
    val_semana = Column(Integer, default=0)
    val_total = Column(Integer, default=0)
    p_jugados = Column(Integer, default=0)

#PYTHON
    def __init__(self,nombre=None,equipo=None,posicion=None,nacionalidad=None,lesion=None,valoracion=None,val_mercado=None,clausula=None,contratado_por=None,titular=False,jugando_de="",val_semana=0,val_total=0,p_jugados=0):
        self.nombre = nombre
        self.equipo = equipo
        self.posicion = posicion
        self.nacionalidad = nacionalidad
        self.lesion = lesion
        self.valoracion = valoracion
        self.val_mercado = val_mercado
        self.clausula = clausula
        self.contratado_por = contratado_por
        self.titular = titular
        self.jugando_de = jugando_de
        self.val_semana = val_semana
        self.val_total = val_total + val_semana
        self.p_jugados = p_jugados

    def __str__(self):
        return (f"--DATOS DEL JUGADOR--\n"
            f"\t NOMBRE: {self.nombre}\n"
            f"\t EQUIPO: {self.equipo}\n"
            f"\t POSICIÓN: {self.posicion}\n"
            f"\t NACIONALIDAD: {self.nacionalidad}\n"
            f"\t LESION: {self.lesion}\n"
            f"\t VALORACION: {self.valoracion}\n"
            f"\t VALOR DE MERCADO: {self.val_mercado}€\n"
            f"\t CLAUSULA DEL JUGADOR: {self.clausula}€\n"
            f"\t CONTRATADOR POR: {self.contratado_por}\n"
            f"\t TITULAR: {self.titular}\n"
            f"\t JUGANDO DE: {self.jugando_de}"
            f"\t VALORACIÓN DE LA SEMANA: {self.val_semana}\n"
            f"\t VALORACIÓN TOTAL: {self.val_total}\n")


class UsuarioJugador(db.Base):
    __tablename__ = 'usuario_jugador'
    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, nullable=False)
    jugador_id = Column(Integer, nullable=False)
    nombre_usuario = Column(String)
    nombre_jugador = Column(String)
    fecha_adquisicion = Column(Date)  # Puedes añadir más campos si los necesitas
    fecha_venta = Column(Date)

    def __init__(self, usuario_id, jugador_id, nombre_usuario, nombre_jugador, fecha_adquisicion=None, fecha_venta=None):
        self.usuario_id = usuario_id
        self.jugador_id = jugador_id
        self.nombre_usuario = nombre_usuario
        self.nombre_jugador = nombre_jugador
        self.fecha_adquisicion = fecha_adquisicion
        self.fecha_venta = fecha_venta

    def __str__(self):
        return (f"JUGADORES EN PROPIEDAD\n"
                f"PRESIDENTE: {self.nombre_usuario}\n"
                f"NOMBRE DEL JUGADOR: {self.nombre_jugador}\n"
                f"FECHA DE ADQUISICIÓN: {self.fecha_adquisicion}\n"
                f"FECHA DE VENTA: {self.fecha_venta}")