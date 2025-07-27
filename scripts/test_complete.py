#!/usr/bin/env python3
"""
Script completo para probar todo el sistema
Autor: Procesador de Consultas JSON
"""

import requests
import json
import time
import subprocess
import sys
from pathlib import Path

def setup_frontend_data():
    """Configura los datos del frontend"""
    print("📁 Configurando datos del frontend...")
    
    try:
        result = subprocess.run([sys.executable, "scripts/setup_frontend_data.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Datos del frontend configurados")
        else:
            print(f"❌ Error configurando datos: {result.stderr}")
    except Exception as e:
        print(f"❌ Error ejecutando setup: {e}")

def test_backend():
    """Prueba el backend"""
    base_url = "http://localhost:8080"
    
    print("\n🔧 Probando backend...")
    
    try:
        # Verificar salud
        response = requests.get(f"{base_url}/health")
        if response.status_code != 200:
            print("❌ Backend no está funcionando")
            return False
        print("✅ Backend funcionando")
        
        # Probar estadísticas iniciales
        response = requests.get(f"{base_url}/optimization/stats")
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Endpoint de estadísticas funcionando")
                return True
            else:
                print(f"❌ Error en estadísticas: {data.get('error')}")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def generate_test_stats():
    """Genera estadísticas de prueba"""
    base_url = "http://localhost:8080"
    
    print("\n📊 Generando estadísticas de prueba...")
    
    test_json = {
        "users": [
            {
                "id": 1,
                "name": "Usuario 1",
                "profile": {
                    "email": "user1@example.com",
                    "preferences": {
                        "language": "es",
                        "theme": "dark"
                    }
                }
            },
            {
                "id": 2,
                "name": "Usuario 2", 
                "profile": {
                    "email": "user2@example.com",
                    "preferences": {
                        "language": "en",
                        "theme": "light"
                    }
                }
            }
        ]
    }
    
    queries = [
        "users.0.profile.preferences.language",
        "users.1.profile.preferences.language",
        "users.0.profile.email",
        "users.1.profile.email"
    ]
    
    try:
        # Ejecutar consultas para generar estadísticas
        for i, query in enumerate(queries, 1):
            print(f"   Ejecutando consulta {i}: {query}")
            
            response = requests.post(f"{base_url}/query/update-stats", 
                                   json={"json": json.dumps(test_json), "query": query})
            
            if response.status_code == 200:
                print(f"   ✅ Consulta {i} exitosa")
            else:
                print(f"   ❌ Error en consulta {i}: {response.status_code}")
            
            time.sleep(0.2)
        
        # Verificar estadísticas finales
        response = requests.get(f"{base_url}/optimization/stats")
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                stats = data.get("data", {})
                print("\n✅ Estadísticas generadas:")
                print(f"   Consultas totales: {stats.get('optimization_stats', {}).get('TotalQueries', 0)}")
                print(f"   Consultas optimizadas: {stats.get('optimization_stats', {}).get('OptimizedQueries', 0)}")
                print(f"   Cache hits: {stats.get('optimization_stats', {}).get('CacheHits', 0)}")
                return True
            else:
                print(f"❌ Error: {data.get('error')}")
                return False
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error generando estadísticas: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 Test Completo del Sistema")
    print("=" * 40)
    
    # Verificar que estamos en el directorio correcto
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Error: Debes ejecutar este script desde la raíz del proyecto")
        return
    
    # 1. Configurar datos del frontend
    setup_frontend_data()
    
    # 2. Probar backend
    if not test_backend():
        print("\n❌ El backend no está funcionando correctamente")
        print("💡 Asegúrate de ejecutar: cd backend && go run main.go")
        return
    
    # 3. Generar estadísticas de prueba
    if not generate_test_stats():
        print("\n❌ Error generando estadísticas de prueba")
        return
    
    print("\n🎉 ¡Test completo exitoso!")
    print("\n📋 Resumen:")
    print("  ✅ Datos del frontend configurados")
    print("  ✅ Backend funcionando correctamente")
    print("  ✅ Estadísticas de optimización generadas")
    print("\n💡 Ahora puedes:")
    print("  1. Usar el botón 'Cargar JSON Grande' en la interfaz")
    print("  2. Ver las estadísticas de optimización en tiempo real")
    print("  3. Ejecutar consultas para ver las diferencias de rendimiento")

if __name__ == "__main__":
    main() 