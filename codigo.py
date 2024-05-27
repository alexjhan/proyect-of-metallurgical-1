import sqlite3

# Conectar a la base de datos SQLite (crea el archivo si no existe)
conn = sqlite3.connect('minerales.db')
c = conn.cursor()

# Crear tabla de minerales
c.execute('''
CREATE TABLE IF NOT EXISTS minerales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL
)
''')

# Crear tabla de componentes
c.execute('''
CREATE TABLE IF NOT EXISTS componentes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mineral_id INTEGER NOT NULL,
    componente TEXT NOT NULL,
    porcentaje REAL NOT NULL,
    FOREIGN KEY (mineral_id) REFERENCES minerales(id)
)
''')

# Insertar minerales (solo si no existen ya en la base de datos)
minerales = ['azurita', 'malaquita', 'cuprita', 'tenorita']
for mineral in minerales:
    c.execute('INSERT OR IGNORE INTO minerales (nombre) VALUES (?)', (mineral,))

# Insertar componentes para cada mineral
componentes = [
    ('azurita', 'cobre', 0.5231),      # Ejemplo: azurita contiene 52.3% de cobre
    ('azurita', 'carbono', 0.0698),    # Ejemplo: azurita contiene 6.98% de carbono
    ('azurita', 'oxígeno', 0.3722),    # Ejemplo: azurita contiene 37.2% de oxígeno
    ('azurita', 'hidrogeno', 0.059),   # Ejemplo: azurita contiene 5.9% de hidrogeno
    ('malaquita', 'cobre', 0.5752),    # Ejemplo: malaquita contiene 57.52% de cobre
    ('malaquita', 'carbono', 0.0543),  # Ejemplo: malaquita contiene 5.43% de carbono
    ('malaquita', 'oxígeno', 0.3615),  # Ejemplo: malaquita contiene 3.62% de oxigeno
    ('malaquita', 'hidrogeno', 0.0091),# Ejemplo: malaquita contiene 0.91% de hidrogeno
    ('cuprita', 'cobre', 0.888),       # Ejemplo: cuprita contiene 88.8% de cobre
    ('cuprita', 'oxígeno', 0.112),     # Ejemplo: cuprita contiene 11.2% de oxígeno
    ('tenorita', 'cobre', 0.798),      # Ejemplo: tenorita contiene 79.8% de cobre
    ('tenorita', 'oxígeno', 0.202)     # Ejemplo: tenorita contiene 20.2% de oxígeno
]

for mineral, componente, porcentaje in componentes:
    mineral_id = c.execute('SELECT id FROM minerales WHERE nombre = ?', (mineral,)).fetchone()[0]
    c.execute('INSERT OR IGNORE INTO componentes (mineral_id, componente, porcentaje) VALUES (?, ?, ?)', 
              (mineral_id, componente, porcentaje))

# Guardar los cambios y cerrar la conexión a la base de datos
conn.commit()
conn.close()

print("Base de datos creada y poblada exitosamente.")

# Función para consultar componentes de un mineral dado su nombre y cantidad
def consultar_componentes(mineral, cantidad):
    conn = sqlite3.connect('minerales.db')
    c = conn.cursor()
    
    c.execute('''
    SELECT componentes.componente, componentes.porcentaje 
    FROM componentes 
    JOIN minerales ON componentes.mineral_id = minerales.id 
    WHERE minerales.nombre = ?
    ''', (mineral,))
    resultados = c.fetchall()
    
    if resultados:
        print(f"Componentes del mineral '{mineral}' en {cantidad} toneladas:")
        for componente, porcentaje in resultados:
            contenido_metal = porcentaje * cantidad
            print(f"- {componente}: {contenido_metal:.2f} toneladas ({porcentaje * 100}%)")
    else:
        print(f"No se encontraron componentes para el mineral '{mineral}'.")
    
    conn.close()

# Solicitar al usuario que ingrese el nombre del mineral y la cantidad
mineral = input("Ingrese el nombre del mineral: ").lower()
try:
    cantidad = float(input("Ingrese la cantidad del mineral (en toneladas): "))
except ValueError:
    print("Por favor, ingrese un número válido para la cantidad.")
    input("Presione Enter para salir.")
    exit()

# Consultar y mostrar los componentes del mineral
consultar_componentes(mineral, cantidad)

# Pausa para evitar que el programa se cierre inmediatamente
input("Presione Enter para salir.")
