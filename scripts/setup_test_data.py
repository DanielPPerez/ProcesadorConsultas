#!/usr/bin/env python3
"""
Script completo para generar y copiar datos de prueba
Autor: Procesador de Consultas JSON
"""

import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completado")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ Error en {description}")
            if result.stderr:
                print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {description}: {e}")
        return False
    return True

def main():
    """Función principal"""
    print("🚀 Setup Completo de Datos de Prueba")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Error: Debes ejecutar este script desde la raíz del proyecto")
        return
    
    # Generar JSON grande
    if not run_command("python scripts/generate_test_json.py large 1000", "Generando JSON grande"):
        return
    
    # Descargar datos de APIs
    if not run_command("python scripts/download_test_data.py jsonplaceholder", "Descargando datos de JSONPlaceholder"):
        return
    
    # Copiar archivos al frontend
    if not run_command("python scripts/copy_json_to_frontend.py", "Copiando archivos al frontend"):
        return
    
    print("\n🎉 ¡Setup completado exitosamente!")
    print("\n📋 Resumen:")
    print("  ✅ JSON grande generado (1000 usuarios)")
    print("  ✅ Datos de JSONPlaceholder descargados")
    print("  ✅ Archivos copiados al frontend")
    print("\n💡 Ahora puedes:")
    print("  1. Iniciar el backend: cd backend && go run main.go")
    print("  2. Iniciar el frontend: cd frontend && npm start")
    print("  3. Usar el botón 'Cargar JSON Grande' en la interfaz web")
    print("  4. Ver las estadísticas de optimización en tiempo real")

if __name__ == "__main__":
    main() 