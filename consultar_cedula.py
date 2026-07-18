import sys

from cedula_service import buscar_por_cedula, buscar_por_nombre


def _imprimir(resultados, con_estado=False):
    if not resultados:
        print("Sin resultados.")
        return

    print("\n" + "=" * 60)
    print("RESULTADOS")
    print("=" * 60)
    for item in resultados:
        print(f"\n  Cédula : {item['cedula']}")
        print(f"  Nombre : {item['nombre']}")
        if con_estado:
            print(f"  Estado : {item['estado']}")
    print("\n" + "=" * 60)


def main():
    if len(sys.argv) < 3:
        print("Uso:")
        print("  python3 consultar_cedula.py cedula <número_de_cédula>")
        print("  python3 consultar_cedula.py nombre <apellidos_y_nombres>")
        print("\nEjemplos:")
        print("  python3 consultar_cedula.py cedula 1710034065")
        print("  python3 consultar_cedula.py nombre 'Castillo Calle Nestor'")
        sys.exit(1)

    modo  = sys.argv[1].lower()
    valor = sys.argv[2]

    if modo not in ("cedula", "nombre"):
        print("El modo debe ser 'cedula' o 'nombre'.")
        sys.exit(1)

    print(f"Consultando por {'cédula' if modo == 'cedula' else 'nombre'}: {valor}")

    if modo == "cedula":
        _imprimir(buscar_por_cedula(valor))
    else:
        _imprimir(buscar_por_nombre(valor), con_estado=True)


if __name__ == "__main__":
    main()
