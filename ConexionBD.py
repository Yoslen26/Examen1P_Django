import pyodbc
import cx_Oracle

class ConexionBD:
    conexion = None

    @staticmethod
    def abrirconexion():
        ConexionBD.conexion = cx_Oracle.connect("system/area@localhost/xe")
        return ConexionBD.conexion

    @staticmethod
    def GetFutbolistas():
        cursor = ConexionBD.abrirconexion().cursor()
        cursor.execute("EXEC SP_GET_FUTBOLISTAS")
        rows = cursor.fetchall()
        return [row for row in rows]

    @staticmethod
    def GetFutbolista(cedula):
        cursor = ConexionBD.abrirconexion().cursor()
        cursor.execute("EXEC SP_GET_FUTBOLISTA @PI_CEDULA=?", cedula)
        row = cursor.fetchone()
        return row

    @staticmethod
    def PostFutbolista(objJugador):
        cursor = ConexionBD.abrirconexion().cursor()
        cursor.execute("EXEC SP_INS_FUTBOLISTA", (objJugador.cedula, objJugador.nombres, objJugador.apellidos, objJugador.fecha_nacimiento, objJugador.pais, objJugador.direccion, objJugador.descripcion))
        cursor.commit()

    @staticmethod
    def abrirconexion():
        ConexionBD.conexion = cx_Oracle.connect("usuario/password@localhost/XE")
        return ConexionBD.conexion

    @staticmethod
    def PutFutbolista(cedula, objJugador):
        cursor = ConexionBD.abrirconexion().cursor()
        cursor.callproc("SP_UPD_FUTBOLISTA", [objJugador.nombres, objJugador.apellidos, objJugador.fecha_nacimiento, objJugador.pais, objJugador.direccion, objJugador.descripcion])
        cursor.close()

    @staticmethod
    def DeleteFutbolista(cedula):
        cursor = ConexionBD.abrirconexion().cursor()
        cursor.callproc("SP_DEL_FUTBOLISTA", [cedula])
        cursor.close()

    @staticmethod
    def fillFutbolista(ds):
        jugador = []
        for row in ds:
            objJugador = Futbolista()
            objJugador.cedula = row[0]
            objJugador.nombres = row[1]
            objJugador.apellidos = row[2]
            objJugador.fecha_nacimiento = row[3]
            objJugador.pais = row[4]
            objJugador.direccion = row[5]
            objJugador.descripcion = row[6]
            jugador.append(objJugador)
        return jugador

    @staticmethod
    def GetHistoricoEquipos(cedula):
        cursor = ConexionBD.abrirconexion().cursor()
        data = cursor.callfunc("SP_GET_HISTORICO_EQUIPOS", cx_Oracle.CURSOR, [cedula])
        equipos = ConexionBD.fillHistorico(data)
        cursor.close()
        return equipos

    @staticmethod
    def fillHistorico(ds):
        historico = []
        for row in ds:
            objHistorico = HistoricoEquipos()
            objHistorico.nombres = row["NOMBRES"]
            objHistorico.nombre_equipo = row["NOMBRE_EQUIPO"]
            objHistorico.fecha_inicio = row["FECHA_INICIO"]
            objHistorico.fecha_fin = row["FECHA_FIN"]
            historico.append(objHistorico)
            return historico