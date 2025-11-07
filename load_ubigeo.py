import csv
import os
from app import create_app
from app.extensions import db
from app.models import Ubigeo

# Obtenemos la ruta absoluta del directorio donde está este script
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# El nombre de tu archivo CSV
CSV_FILENAME = 'UBIGEOS_2022_1891_distritos.csv'
CSV_PATH = os.path.join(BASE_DIR, CSV_FILENAME)

def load_data():
    """Lee el CSV y lo carga en la base de datos."""
    
    # Creamos e inicializamos la app de Flask para tener el contexto
    app = create_app()
    
    with app.app_context():
        print("Iniciando carga de Ubigeos...")
        
        # Primero, borramos los datos existentes para evitar duplicados
        try:
            num_rows_deleted = db.session.query(Ubigeo).delete()
            db.session.commit()
            print(f"Se eliminaron {num_rows_deleted} registros antiguos de ubigeo.")
        except Exception as e:
            db.session.rollback()
            print(f"Error al limpiar la tabla ubigeo: {e}")
            return

        # Abrimos el archivo CSV
        try:
            with open(CSV_PATH, mode='r', encoding='latin-1') as f:
                # Usamos DictReader para leer por nombre de columna
                # OJO: El delimitador es ';'
                reader = csv.DictReader(f, delimiter=';')
                
                count = 0
                batch_count = 0
                ubigeos_to_add = []

                for row in reader:
                    # Obtenemos el IDDIST
                    iddist = row.get('IDDIST')
                    
                    # Omitimos filas vacías o de pie de página
                    if not iddist or not iddist.strip():
                        continue

                    # Mapeamos las columnas del CSV a las columnas del Modelo
                    # Usamos .get() para evitar errores si una columna opcional no existe
                    nuevo_ubigeo = Ubigeo(
                        iddist=iddist.strip(),
                        nombdep=row.get('NOMBDEP'),
                        nombprov=row.get('NOMBPROV'),
                        nombdist=row.get('NOMBDIST'),
                        # El CSV tiene cabeceras con espacios o caracteres especiales
                        nom_capital=row.get('NOM_CAPITAL (LEGAL)'),
                        cod_reg_nat=row.get('COD_ REG_NAT'),
                        region_natural=row.get('REGION NATURAL')
                    )
                    ubigeos_to_add.append(nuevo_ubigeo)
                    count += 1
                    batch_count += 1

                    # Hacemos commit en lotes de 100 para no saturar la memoria
                    if batch_count >= 100:
                        db.session.add_all(ubigeos_to_add)
                        db.session.commit()
                        print(f"Cargados {count} registros...")
                        ubigeos_to_add = [] # Limpiamos el lote
                        batch_count = 0

                # Hacemos commit del último lote restante
                if ubigeos_to_add:
                    db.session.add_all(ubigeos_to_add)
                    db.session.commit()
                    print(f"Cargados {count} registros...")

                print(f"\n¡Carga completada! Se insertaron {count} registros de Ubigeo.")

        except FileNotFoundError:
            print(f"Error: No se encontró el archivo '{CSV_FILENAME}' en la carpeta raíz.")
            print(f"Ruta buscada: {CSV_PATH}")
        except Exception as e:
            db.session.rollback()
            print(f"Ocurrió un error durante la carga: {e}")

# Esto permite que el script se ejecute directamente
if __name__ == '__main__':
    load_data()