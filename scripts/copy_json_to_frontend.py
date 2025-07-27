#!/usr/bin/env python3
"""
Script para copiar JSONs generados al directorio público del frontend
Autor: Procesador de Consultas JSON
"""

import os
import shutil
import glob
from pathlib import Path

def copy_json_files():
    """Copia archivos JSON generados al directorio público del frontend"""
    
    # Directorios
    scripts_dir = Path("scripts")
    frontend_public_dir = Path("frontend/public")
    
    # Crear directorio público si no existe
    frontend_public_dir.mkdir(parents=True, exist_ok=True)
    
    # Buscar archivos JSON en el directorio scripts
    json_files = list(scripts_dir.glob("*.json"))
    
    if not json_files:
        print("❌ No se encontraron archivos JSON en el directorio scripts")
        print("💡 Ejecuta primero: python scripts/generate_test_json.py large 1000")
        return
    
    print(f"📁 Copiando {len(json_files)} archivos JSON al frontend...")
    
    copied_count = 0
    for json_file in json_files:
        try:
            # Copiar archivo
            destination = frontend_public_dir / json_file.name
            shutil.copy2(json_file, destination)
            
            # Obtener tamaño del archivo
            file_size = json_file.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            print(f"✅ {json_file.name} ({file_size_mb:.2f} MB)")
            copied_count += 1
            
        except Exception as e:
            print(f"❌ Error copiando {json_file.name}: {e}")
    
    print(f"\n🎉 {copied_count} archivos copiados exitosamente")
    print(f"📂 Ubicación: {frontend_public_dir.absolute()}")
    print("\n💡 Ahora puedes usar el botón 'Cargar JSON Grande' en la interfaz web")

def main():
    """Función principal"""
    print("🚀 Copiador de JSONs al Frontend")
    print("=" * 40)
    
    copy_json_files()

if __name__ == "__main__":
    main() 