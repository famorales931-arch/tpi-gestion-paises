# 🌍 Gestión de Datos de Países en Python

**Trabajo Práctico Integrador (TPI) — Programación 1**
Tecnicatura Universitaria en Programación — UTN

---

## Descripción

Aplicación de consola en Python que permite gestionar información sobre países del mundo. Lee datos desde un archivo CSV y ofrece funcionalidades de búsqueda, filtrado, ordenamiento y estadísticas.

---

## Integrantes

| Nombre |
|--------|--------|
| Morales Aliaga Fabian] |
| [Nombre Estudiante 2] |

---

## Requisitos

- Python 3.x
- No requiere librerías externas (sólo módulos estándar: `csv`, `os`)

---

## Cómo ejecutar

1. Clonar el repositorio o descargar los archivos.
2. Asegurarse de que `paises.csv` esté en el mismo directorio que `gestion_paises.py`.
3. Ejecutar:

```bash
python gestion_paises.py
```

---

## Funcionalidades

| Opción | Descripción |
|--------|-------------|
| 1 | Mostrar todos los países |
| 2 | Agregar un nuevo país |
| 3 | Actualizar población y/o superficie de un país |
| 4 | Buscar por nombre (parcial o exacto) |
| 5 | Filtrar por continente, rango de población o superficie |
| 6 | Ordenar por nombre, población o superficie (asc/desc) |
| 7 | Ver estadísticas generales |
| 0 | Salir |

---

## Ejemplos de uso

### Agregar un país
```
Seleccione una opción: 2
  Nombre del país: Ecuador
  Población: 17900000
  Superficie en km²: 283561
  Continente: América
  [OK] País 'Ecuador' agregado exitosamente.
```

### Buscar por nombre parcial
```
Seleccione una opción: 4
  Ingrese nombre o parte del nombre: arg
  
  Resultados para 'arg':
  #    Nombre                  Población   Superficie (km²)  Continente
  ────────────────────────────────────────────────────────────────────────
  1    Argentina              45,376,763          2,780,400  América
```

### Estadísticas
```
Seleccione una opción: 7
  País con MAYOR población : China (1,411,100,000)
  País con MENOR población : Uruguay (3,473,730)
  Promedio de población    : 107,234,512
  ...
  Países por continente:
    África         : 8
    América        : 11
    Asia           : 9
    Europa         : 10
    Oceanía        : 2
```

---

## Estructura del proyecto

```
tpi_paises/
├── gestion_paises.py   # Código fuente principal
├── paises.csv          # Dataset base
└── README.md           # Este archivo
```

---

## Dataset (paises.csv)

El CSV incluye 40 países con los campos:

```
nombre,poblacion,superficie,continente
Argentina,45376763,2780400,América
...
```

---

## 🎥 Video demostrativo

> [Insertar enlace al video aquí]

## 📄 Documentación PDF

> [Insertar enlace al PDF aquí]

---

## Bibliografía

- Documentación oficial de Python: https://docs.python.org/3/
- Módulo CSV: https://docs.python.org/3/library/csv.html
- Tutorial de listas y diccionarios en Python: https://docs.python.org/3/tutorial/datastructures.html
