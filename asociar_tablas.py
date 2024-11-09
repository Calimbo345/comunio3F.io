"""from sqlalchemy import Table, Column, Integer, ForeignKey
import db
#CREA UNA CLASE EN MODELS Y AGREGA ESTA PARTE DEL CODIGO
usuario_jugador = Table('usuario_jugador', db.Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id')),
    Column('jugador_id', Integer, ForeignKey('jugadores_tercera_FEB.id'))
)"""