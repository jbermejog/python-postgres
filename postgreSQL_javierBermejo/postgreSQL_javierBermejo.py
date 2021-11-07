# Aplicación básica para actividad SQL
# Importamos librerías
from decouple import config
import psycopg2
import sys
import os


class Actividad:

    def __init__(self):

        # Leemos los datos del fichero .env
        DB_HOST = config('DB_HOST')
        DB_DATABASE = config('DB_DATABASE')
        DB_USERNAME = config('DB_USERNAME')
        DB_PASSWORD = config('DB_PASSWORD')

        # Intentamos la conexión
        try:
            self.conn = psycopg2.connect(
                dbname=DB_DATABASE,
                user=DB_USERNAME,
                host=DB_HOST,
                password=DB_PASSWORD,
                connect_timeout=1
            )
            self.conn.autocommit = True
            self.cur = self.conn.cursor()
        except:
            print('Error al conectar con la DB')
            sys.exit(1)

    def ejecutar(self, comandos):
        # Método que permite ejecutar SQL

        try:
            for comando in comandos:
                self.cur.execute(comando)

        except psycopg2.Error as e:
            print('Se ha producido un error:', str(e))

    def consulta_notas(self, sql):
        # Función que permite hacer una consulta y mostrar las notas

        try:
            self.cur.execute(sql)
            registros = self.cur.fetchall()
            print('{}\t{:<20}\t{}\t{}\t{}\t'.format(
                'ID', 'NAME', 'EDAD', 'NOTAS', 'ID_EDIC'))
            for registro in registros:
                print('{}\t{:<20}\t{}\t{}\t{}\t'.format(
                    registro[0], registro[1], registro[2], registro[3], registro[4]))

        except psycopg2.Error as e:
            print('Se ha producido un error:', str(e))

    def crear_columnas(self):
        # Función para modificar la tabla existente y agregar columnas

        comandos = (
            """
            ALTER TABLE edicion
                ADD COLUMN id_edic SERIAL,
                ADD COLUMN numero VARCHAR(25),
                ADD PRIMARY KEY(id_edic)
            """,
            """
            ALTER TABLE notas
                ADD COLUMN id_notas SERIAL ,
                ADD COLUMN name VARCHAR(25),
                ADD COLUMN edad INT,
                ADD COLUMN notas NUMERIC,
                ADD COLUMN id_edic INT,
                ADD PRIMARY KEY(id_notas),
                ADD CONSTRAINT fk_edicion
                    FOREIGN KEY(id_edic)
                        REFERENCES edicion(id_edic)
                        ON DELETE CASCADE
            """,
        )

        self.ejecutar(comandos)

    def tarea_1_insertar_datos(self):
        # Función que realiza la tarea 1

        comandos = (
            """
            INSERT INTO "edicion" ("numero")
                VALUES
                    ('Uno'),
                    ('Dos'),
                    ('Tres')
            """,
            """
            INSERT INTO "notas" ("name", "edad", "notas", "id_edic")
                VALUES
                    ('Isabel Maniega', '30', '5.6', '1'),
                    ('José Manuel Peña', '30', '7.8', '1'),
                    ('Pedro López', '25', '5.2', '2'),
                    ('Julia García', '22', '7.3', '1'),
                    ('Amparo Mayora', '28', '8.4', '3'),
                    ('Juan Martínez', '30', '6.8', '3'),
                    ('Fernando López', '35', '6.1', '2'),
                    ('María Castro', '41', '5.9', '3')
            """,
        )

        self.ejecutar(comandos)
        print('Datos insertados')

    def tarea_2_actualizar_datos(self):
        # Función que realiza la tarea 2

        comandos = (
            """
            UPDATE "notas" SET
            "notas" = '6.4'
            WHERE "id_notas" = '3';
            """,
            """
            UPDATE "notas" SET
            "notas" = '5.2'
            WHERE "id_notas" = '8';
            """,
        )

        self.ejecutar(comandos)
        print('Datos actualizados')

    def tarea_3_mostrar_datos(self):
        # Función que realiza la tarea 3

        print("MOSTRAMOS TODAS LAS NOTAS")
        sql = """
              SELECT * FROM "notas";
            """
        self.consulta_notas(sql)

    def tarea_4_buscar_datos(self):
        # Función que realiza la tarea 4
        print("BUSCAMOS NOTAS ENTRE 5 Y 6.5")
        sql = """
            SELECT * FROM "notas"
            WHERE "notas" BETWEEN '5' AND '6.5'
            """
        self.consulta_notas(sql)

    def tarea_5_buscar_datos(self):
        # Función que realiza la tarea 5
        print("MOSTRAMOS NOTAS DE LA EDICION DOS")
        sql = """
            SELECT * FROM "notas"
            WHERE "id_edic" = '2'
            """
        self.consulta_notas(sql)

    def tarea_6_eliminar_datos(self):
        # Función que realiza la tarea 6
        print("ELIMINADOS DATOS DE PEDRO")

        comandos = (
            """
            DELETE FROM "notas" WHERE (("name" = 'Pedro López'))
            """,
        )

        self.ejecutar(comandos)
        print('Datos eliminados')

    def close(self):
        # Función de cierre de la conexión
        self.cur.close()
        self.conn.commit()
        self.conn.close()


def menu():
    # Función que muestra el menú al usuario
    while True:
        print("Selecciona una opción")
        print("\t0 - Crear columnas en las tablas notas y edicion")
        print("\t1 - Insertar datos de ediciones y notas")
        print("\t2 - Actualizar notas del id 3 y 8")
        print("\t3 - Mostrar todas las notas")
        print("\t4 - Mostrar notas entre 5 y 6.5")
        print("\t5 - Mostrar notas notas edicion 2")
        print("\t6 - Eliminar datos de Pedro")
        print("\t9 - salir")
        # solicitamos una opción al usuario
        opcionMenu = input("inserta un numero valor >> ")

        if opcionMenu == "0":
            os.system('cls')
            print("Has seleccionado crear columnas en tablas")
            db.crear_columnas()

        elif opcionMenu == "1":
            os.system('cls')
            print("Has seleccionado Insertar datos")
            db.tarea_1_insertar_datos()

        elif opcionMenu == "2":
            os.system('cls')
            print("Has seleccionado Actualiza los datos")
            db.tarea_2_actualizar_datos()

        elif opcionMenu == "3":
            os.system('cls')
            print("Has seleccionado Mostrar los datos")
            db.tarea_3_mostrar_datos()

        elif opcionMenu == "4":
            os.system('cls')
            print("Has seleccionado Mostrar los datos con filtro 1")
            db.tarea_4_buscar_datos()

        elif opcionMenu == "5":
            os.system('cls')
            print("Has seleccionado Mostrar los datos con filtro 2")
            db.tarea_5_buscar_datos()

        elif opcionMenu == "6":
            os.system('cls')
            print("Has seleccionado Eliminar datos")
            db.tarea_6_eliminar_datos()

        elif opcionMenu == "9":
            print("Hasta pronto!!")
            break

        else:
            print("")
            input(
                "No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")


if __name__ == '__main__':

    # Creamos el objeto con la conexión
    db = Actividad()

    # Mostramos el menú
    menu()

    # Cerramos la conexión
    db.close
