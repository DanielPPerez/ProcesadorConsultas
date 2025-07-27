#!/usr/bin/env python3
"""
Script para probar el backend y verificar optimizaciones
Autor: Procesador de Consultas JSON
"""

import requests
import json
import time

def test_backend():
    """Prueba el backend y verifica las optimizaciones"""
    
    base_url = "http://localhost:8080"
    
    # JSON de prueba
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
    
    test_query = "users.0.profile.preferences.language"
    
    print("🚀 Probando Backend...")
    print("=" * 40)
    
    try:
        # Probar endpoint de salud
        print("1. Probando endpoint de salud...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Backend está funcionando")
        else:
            print("❌ Backend no responde")
            return
        
        # Probar consulta simple
        print("\n2. Probando consulta simple...")
        response = requests.post(f"{base_url}/query", 
                               json={"json": json.dumps(test_json), "query": test_query})
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Consulta simple exitosa")
                print(f"   Valor encontrado: {data['data']['value']}")
                
                # Verificar estadísticas de optimización
                if "optimization_stats" in data:
                    stats = data["optimization_stats"]
                    print(f"   Consultas totales: {stats.get('TotalQueries', 0)}")
                    print(f"   Consultas optimizadas: {stats.get('OptimizedQueries', 0)}")
                    print(f"   Cache hits: {stats.get('CacheHits', 0)}")
                else:
                    print("   ⚠️ No se encontraron estadísticas de optimización")
            else:
                print(f"❌ Error en consulta: {data.get('error')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
        
        # Probar estadísticas de optimización
        print("\n3. Probando estadísticas de optimización...")
        response = requests.get(f"{base_url}/optimization/stats")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                stats = data.get("data", {})
                print("✅ Estadísticas de optimización:")
                print(f"   Consultas totales: {stats.get('TotalQueries', 0)}")
                print(f"   Consultas optimizadas: {stats.get('OptimizedQueries', 0)}")
                print(f"   Cache hits: {stats.get('CacheHits', 0)}")
                print(f"   Tiempo promedio: {stats.get('AverageOptimizationTime', '0ms')}")
            else:
                print(f"❌ Error obteniendo estadísticas: {data.get('error')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
        
        # Probar múltiples consultas para ver incremento
        print("\n4. Probando múltiples consultas...")
        for i in range(3):
            response = requests.post(f"{base_url}/query", 
                                   json={"json": json.dumps(test_json), "query": test_query})
            if response.status_code == 200:
                print(f"   Consulta {i+1}: ✅")
            else:
                print(f"   Consulta {i+1}: ❌")
        
        # Verificar estadísticas finales
        print("\n5. Estadísticas finales...")
        response = requests.get(f"{base_url}/optimization/stats")
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                stats = data.get("data", {})
                print("✅ Estadísticas finales:")
                print(f"   Consultas totales: {stats.get('TotalQueries', 0)}")
                print(f"   Consultas optimizadas: {stats.get('OptimizedQueries', 0)}")
                print(f"   Cache hits: {stats.get('CacheHits', 0)}")
                print(f"   Tiempo promedio: {stats.get('AverageOptimizationTime', '0ms')}")
            else:
                print(f"❌ Error: {data.get('error')}")
        
        print("\n🎉 Pruebas completadas!")
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend")
        print("💡 Asegúrate de que el backend esté ejecutándose en http://localhost:8080")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_backend() 