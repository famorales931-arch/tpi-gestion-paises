"""
TPI - Gestión de Datos de Países en Python
Programación 1 - Tecnicatura Universitaria en Programación - UTN
"""

import csv
import os

ARCHIVO_CSV = "paises.csv"


# ─────────────────────────────────────────
# CARGA Y GUARDADO DE DATOS
# ─────────────────────────────────────────

def cargar_paises(archivo):
    """Lee el archivo CSV y devuelve una lista de diccionarios con los datos de cada país."""
    paises = []
    try:
        with open(archivo, newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            for fila in lector:
                # Validar que no haya campos vacíos
                if not all(fila.values()):
                    print(f"  [!] Fila ignorada por campos vacíos: {fila}")
                    continue
                try:
                    pais = {
                        "nombre": fila["nombre"].strip(),
                        "poblacion": int(fila["poblacion"]),
                        "superficie": int(fila["superficie"]),
                        "continente": fila["continente"].strip()
                    }
                    paises.append(pais)
                except ValueError:
                    print(f"  [!] Fila ignorada por error de formato: {fila}")
    except FileNotFoundError:
        print(f"  [!] Archivo '{archivo}' no encontrado. Se iniciará con lista vacía.")
    return paises


def guardar_paises(paises, archivo):
    """Guarda la lista de países en el archivo CSV."""
    with open(archivo, "w", newline="", encoding="utf-8") as f:
        campos = ["nombre", "poblacion", "superficie", "continente"]
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(paises)
    print("  [OK] Datos guardados correctamente.")


# ─────────────────────────────────────────
# MOSTRAR PAÍSES
# ─────────────────────────────────────────

def mostrar_lista(paises):
    """Muestra una lista de países en formato de tabla."""
    if not paises:
        print("  No hay países para mostrar.")
        return
    print(f"\n  {'#':<4} {'Nombre':<22} {'Población':>14} {'Superficie (km²)':>17} {'Continente':<12}")
    print("  " + "-" * 72)
    for i, p in enumerate(paises, 1):
        print(f"  {i:<4} {p['nombre']:<22} {p['poblacion']:>14,} {p['superficie']:>17,} {p['continente']:<12}")
    print(f"\n  Total: {len(paises)} país/es.\n")


# ─────────────────────────────────────────
# AGREGAR PAÍS
# ─────────────────────────────────────────

def agregar_pais(paises):
    """Solicita los datos de un nuevo país y lo agrega a la lista."""
    print("\n  ── Agregar País ──")
    nombre = input("  Nombre del país: ").strip()
    if not nombre:
        print("  [!] El nombre no puede estar vacío.")
        return

    # Verificar duplicado
    if any(p["nombre"].lower() == nombre.lower() for p in paises):
        print(f"  [!] Ya existe un país con el nombre '{nombre}'.")
        return

    poblacion = pedir_entero("  Población: ")
    if poblacion is None:
        return
    superficie = pedir_entero("  Superficie en km²: ")
    if superficie is None:
        return
    continente = input("  Continente: ").strip()
    if not continente:
        print("  [!] El continente no puede estar vacío.")
        return

    pais = {"nombre": nombre, "poblacion": poblacion, "superficie": superficie, "continente": continente}
    paises.append(pais)
    guardar_paises(paises, ARCHIVO_CSV)
    print(f"  [OK] País '{nombre}' agregado exitosamente.")


# ─────────────────────────────────────────
# ACTUALIZAR PAÍS
# ─────────────────────────────────────────

def actualizar_pais(paises):
    """Actualiza la población y superficie de un país existente."""
    print("\n  ── Actualizar País ──")
    nombre = input("  Nombre del país a actualizar: ").strip()
    if not nombre:
        print("  [!] El nombre no puede estar vacío.")
        return

    pais = buscar_exacto(paises, nombre)
    if pais is None:
        print(f"  [!] No se encontró el país '{nombre}'.")
        return

    print(f"  País encontrado: {pais['nombre']} | Población: {pais['poblacion']:,} | Superficie: {pais['superficie']:,} km²")
    nueva_pob = pedir_entero("  Nueva Población (Enter para no cambiar): ", opcional=True)
    nueva_sup = pedir_entero("  Nueva Superficie en km² (Enter para no cambiar): ", opcional=True)

    if nueva_pob is not None:
        pais["poblacion"] = nueva_pob
    if nueva_sup is not None:
        pais["superficie"] = nueva_sup

    guardar_paises(paises, ARCHIVO_CSV)
    print(f"  [OK] Datos de '{pais['nombre']}' actualizados.")


# ─────────────────────────────────────────
# BUSCAR PAÍS
# ─────────────────────────────────────────

def buscar_pais(paises):
    """Busca países por nombre (coincidencia parcial o exacta)."""
    print("\n  ── Buscar País ──")
    termino = input("  Ingrese nombre o parte del nombre: ").strip().lower()
    if not termino:
        print("  [!] Debe ingresar un término de búsqueda.")
        return

    resultados = [p for p in paises if termino in p["nombre"].lower()]
    if resultados:
        print(f"\n  Resultados para '{termino}':")
        mostrar_lista(resultados)
    else:
        print(f"  [!] No se encontraron países con '{termino}'.")


def buscar_exacto(paises, nombre):
    """Devuelve el diccionario del país con nombre exacto (case-insensitive) o None."""
    for p in paises:
        if p["nombre"].lower() == nombre.lower():
            return p
    return None


# ─────────────────────────────────────────
# FILTROS
# ─────────────────────────────────────────

def menu_filtros(paises):
    """Submenú de filtros."""
    print("\n  ── Filtrar Países ──")
    print("  1. Por continente")
    print("  2. Por rango de población")
    print("  3. Por rango de superficie")
    opcion = input("  Opción: ").strip()

    if opcion == "1":
        filtrar_por_continente(paises)
    elif opcion == "2":
        filtrar_por_rango(paises, "poblacion", "población")
    elif opcion == "3":
        filtrar_por_rango(paises, "superficie", "superficie (km²)")
    else:
        print("  [!] Opción inválida.")


def filtrar_por_continente(paises):
    """Filtra y muestra los países de un continente dado."""
    continente = input("  Continente: ").strip()
    if not continente:
        print("  [!] Debe ingresar un continente.")
        return
    resultados = [p for p in paises if p["continente"].lower() == continente.lower()]
    if resultados:
        print(f"\n  Países en {continente}:")
        mostrar_lista(resultados)
    else:
        print(f"  [!] No se encontraron países en '{continente}'.")


def filtrar_por_rango(paises, campo, etiqueta):
    """Filtra países según un rango numérico de un campo dado."""
    minimo = pedir_entero(f"  Mínimo de {etiqueta} (Enter para 0): ", opcional=True)
    maximo = pedir_entero(f"  Máximo de {etiqueta} (Enter para sin límite): ", opcional=True)

    minimo = minimo if minimo is not None else 0
    maximo = maximo if maximo is not None else float("inf")

    if minimo > maximo:
        print("  [!] El mínimo no puede ser mayor que el máximo.")
        return

    resultados = [p for p in paises if minimo <= p[campo] <= maximo]
    if resultados:
        print(f"\n  Países con {etiqueta} entre {minimo:,} y {maximo if maximo != float('inf') else '∞'}:")
        mostrar_lista(resultados)
    else:
        print("  [!] No se encontraron países en ese rango.")


# ─────────────────────────────────────────
# ORDENAMIENTO
# ─────────────────────────────────────────

def menu_ordenar(paises):
    """Submenú de ordenamiento."""
    print("\n  ── Ordenar Países ──")
    print("  1. Por nombre")
    print("  2. Por población")
    print("  3. Por superficie")
    opcion = input("  Opción: ").strip()

    campos = {"1": "nombre", "2": "poblacion", "3": "superficie"}
    if opcion not in campos:
        print("  [!] Opción inválida.")
        return

    campo = campos[opcion]
    if opcion in ("2", "3"):
        orden = input("  Orden: (A)scendente / (D)escendente: ").strip().upper()
        descendente = orden == "D"
    else:
        descendente = False

    ordenados = sorted(paises, key=lambda p: p[campo], reverse=descendente)
    print(f"\n  Países ordenados por '{campo}' ({'desc' if descendente else 'asc'}):")
    mostrar_lista(ordenados)


# ─────────────────────────────────────────
# ESTADÍSTICAS
# ─────────────────────────────────────────

def mostrar_estadisticas(paises):
    """Calcula y muestra estadísticas del dataset."""
    if not paises:
        print("  [!] No hay datos suficientes para calcular estadísticas.")
        return

    print("\n  ── Estadísticas ──\n")

    # Mayor y menor población
    mayor_pob = max(paises, key=lambda p: p["poblacion"])
    menor_pob = min(paises, key=lambda p: p["poblacion"])
    promedio_pob = sum(p["poblacion"] for p in paises) / len(paises)

    print(f"  País con MAYOR población : {mayor_pob['nombre']} ({mayor_pob['poblacion']:,})")
    print(f"  País con MENOR población : {menor_pob['nombre']} ({menor_pob['poblacion']:,})")
    print(f"  Promedio de población    : {promedio_pob:,.0f}")

    # Superficie
    mayor_sup = max(paises, key=lambda p: p["superficie"])
    menor_sup = min(paises, key=lambda p: p["superficie"])
    promedio_sup = sum(p["superficie"] for p in paises) / len(paises)

    print(f"\n  País con MAYOR superficie: {mayor_sup['nombre']} ({mayor_sup['superficie']:,} km²)")
    print(f"  País con MENOR superficie: {menor_sup['nombre']} ({menor_sup['superficie']:,} km²)")
    print(f"  Promedio de superficie   : {promedio_sup:,.0f} km²")

    # Cantidad de países por continente
    print("\n  Países por continente:")
    continentes = {}
    for p in paises:
        cont = p["continente"]
        continentes[cont] = continentes.get(cont, 0) + 1
    for cont, cantidad in sorted(continentes.items()):
        print(f"    {cont:<15}: {cantidad}")

    print()


# ─────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────

def pedir_entero(mensaje, opcional=False):
    """Solicita un número entero positivo al usuario. Retorna None si es opcional y se deja vacío."""
    while True:
        entrada = input(mensaje).strip()
        if opcional and entrada == "":
            return None
        try:
            valor = int(entrada)
            if valor < 0:
                print("  [!] El valor no puede ser negativo.")
                continue
            return valor
        except ValueError:
            print("  [!] Ingrese un número entero válido.")


def limpiar_pantalla():
    """Limpia la consola según el sistema operativo."""
    os.system("cls" if os.name == "nt" else "clear")


# ─────────────────────────────────────────
# MENÚ PRINCIPAL
# ─────────────────────────────────────────

def mostrar_menu():
    """Imprime el menú principal."""
    print("\n" + "=" * 50)
    print("   GESTIÓN DE PAÍSES - Programación 1 - UTN")
    print("=" * 50)
    print("  1. Mostrar todos los países")
    print("  2. Agregar un país")
    print("  3. Actualizar un país")
    print("  4. Buscar un país por nombre")
    print("  5. Filtrar países")
    print("  6. Ordenar países")
    print("  7. Estadísticas")
    print("  0. Salir")
    print("=" * 50)


def main():
    """Función principal: carga datos y ejecuta el menú."""
    paises = cargar_paises(ARCHIVO_CSV)
    print(f"\n  [OK] {len(paises)} países cargados desde '{ARCHIVO_CSV}'.")

    while True:
        mostrar_menu()
        opcion = input("  Seleccione una opción: ").strip()

        if opcion == "1":
            mostrar_lista(paises)
        elif opcion == "2":
            agregar_pais(paises)
        elif opcion == "3":
            actualizar_pais(paises)
        elif opcion == "4":
            buscar_pais(paises)
        elif opcion == "5":
            menu_filtros(paises)
        elif opcion == "6":
            menu_ordenar(paises)
        elif opcion == "7":
            mostrar_estadisticas(paises)
        elif opcion == "0":
            print("\n  ¡Hasta luego!\n")
            break
        else:
            print("  [!] Opción inválida. Intente nuevamente.")
        
        input("\n  Presione ENTER para continuar...")


if __name__ == "__main__":
    main()
