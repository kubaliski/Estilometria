# main.py
import sys
import os
from typing import Optional
from analyzer import TextStyleAnalyzer, format_analysis_results

def clear_screen():
    """Limpia la pantalla de la terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def read_file(file_path: str) -> Optional[str]:
    """
    Lee el contenido de un archivo de texto.

    Args:
        file_path (str): Ruta al archivo

    Returns:
        Optional[str]: Contenido del archivo o None si hay error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def get_input_text() -> Optional[str]:
    """
    Obtiene el texto de entrada del usuario.

    Returns:
        Optional[str]: Texto ingresado o None si se cancela
    """
    print("\n¿Cómo deseas ingresar el texto?")
    print("1. Escribir directamente")
    print("2. Cargar desde archivo")
    print("3. Salir")

    choice = input("\nSelecciona una opción (1-3): ").strip()

    if choice == '1':
        print("\nEscribe o pega el texto a analizar (presiona Ctrl+D o Ctrl+Z para terminar):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            return '\n'.join(lines)
    elif choice == '2':
        file_path = input("\nIngresa la ruta del archivo: ").strip()
        return read_file(file_path)
    elif choice == '3':
        return None
    else:
        print("\nOpción no válida. Por favor, intenta de nuevo.")
        return get_input_text()

def configure_analysis_parameters() -> dict:
    """
    Permite al usuario configurar los parámetros del análisis.

    Returns:
        dict: Diccionario con los parámetros configurados
    """
    print("\nConfiguración del análisis:")

    try:
        min_similarity = float(input(
            "Ingresa el umbral mínimo de similitud (0-100) [valor por defecto: 70]: "
        ).strip() or "70")
        min_similarity = max(0, min(100, min_similarity))
    except ValueError:
        print("Valor no válido. Se usará el valor por defecto: 70")
        min_similarity = 70.0

    return {
        'min_similarity': min_similarity
    }

def save_results(results: str):
    """
    Pregunta al usuario si desea guardar los resultados en un archivo.

    Args:
        results (str): Resultados del análisis
    """
    save = input("\n¿Deseas guardar los resultados en un archivo? (s/n): ").lower().strip()

    if save == 's':
        file_name = input("Ingresa el nombre del archivo (por defecto: resultados.txt): ").strip() or "resultados.txt"
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(results)
            print(f"\nResultados guardados exitosamente en: {file_name}")
        except Exception as e:
            print(f"Error al guardar los resultados: {e}")

def main():
    """Función principal del programa."""
    analyzer = TextStyleAnalyzer()

    while True:
        clear_screen()
        print("=== Analizador de Similitud de Textos ===")

        # Obtener texto de entrada
        input_text = get_input_text()
        if input_text is None:
            print("\n¡Hasta luego!")
            sys.exit(0)

        if not input_text.strip():
            print("\nEl texto está vacío. Por favor, intenta de nuevo.")
            input("\nPresiona Enter para continuar...")
            continue

        # Configurar parámetros
        params = configure_analysis_parameters()

        print("\nAnalizando texto...")

        # Realizar análisis
        results = analyzer.analyze_against_database(
            input_text,
            min_similarity=params['min_similarity']
        )

        # Formatear y mostrar resultados
        formatted_results = format_analysis_results(results)
        print("\nResultados del análisis:")
        print(formatted_results)

        # Guardar resultados
        save_results(formatted_results)

        # Preguntar si desea realizar otro análisis
        continue_analysis = input("\n¿Deseas analizar otro texto? (s/n): ").lower().strip()
        if continue_analysis != 's':
            print("\n¡Hasta luego!")
            break

if __name__ == "__main__":
    main()