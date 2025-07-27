#!/usr/bin/env python3
"""
Script para generar estadísticas de prueba
Autor: Procesador de Consultas JSON
"""

import requests
import json
import time

def generate_test_stats():
    """Genera estadísticas de prueba ejecutando consultas optimizadas"""
    
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
    
    queries = [
        "users.0.profile.preferences.language",
        "users.1.profile.preferences.language",
        "users.0.profile.email",
        "users.1.profile.email",
        "users.0.name",
        "users.1.name"
    ]
    
    print("🚀 Generando Estadísticas de Prueba...")
    print("=" * 45)
    
    try:
        # Verificar backend
        print("1. Verificando backend...")
        response = requests.get(f"{base_url}/health")
        if response.status_code != 200:
            print("❌ Backend no está funcionando")
            return
        print("✅ Backend funcionando")
        
        # Ejecutar consultas para generar estadísticas
        print("\n2. Ejecutando consultas optimizadas...")
        for i, query in enumerate(queries, 1):
            print(f"   Consulta {i}: {query}")
            
            response = requests.post(f"{base_url}/query/update-stats", 
                                   json={"json": json.dumps(test_json), "query": query})
            
            if response.status_code == 200:
                print(f"   ✅ Consulta {i} exitosa")
            else:
                print(f"   ❌ Error en consulta {i}: {response.status_code}")
            
            time.sleep(0.2)  # Pequeña pausa
        
        # Repetir algunas consultas para generar cache hits
        print("\n3. Generando cache hits...")
        for i in range(3):
            for query in queries[:3]:  # Solo las primeras 3 consultas
                response = requests.post(f"{base_url}/query/update-stats", 
                                       json={"json": json.dumps(test_json), "query": query})
                if response.status_code == 200:
                    print(f"   ✅ Cache hit {i+1} para: {query}")
                time.sleep(0.1)
        
        # Verificar estadísticas finales
        print("\n4. Verificando estadísticas finales...")
        response = requests.get(f"{base_url}/optimization/stats")
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                stats = data.get("data", {})
                print("✅ Estadísticas generadas:")
                print(f"   Consultas totales: {stats.get('optimization_stats', {}).get('TotalQueries', 0)}")
                print(f"   Consultas optimizadas: {stats.get('optimization_stats', {}).get('OptimizedQueries', 0)}")
                print(f"   Cache hits: {stats.get('optimization_stats', {}).get('CacheHits', 0)}")
                print(f"   Tiempo promedio: {stats.get('optimization_stats', {}).get('AverageOptimizationTime', '0ms')}")
            else:
                print(f"❌ Error: {data.get('error')}")
        else:
            print(f"❌ Error HTTP: {response.status_code}")
        
        print("\n🎉 Estadísticas de prueba generadas!")
        print("💡 Ahora puedes ver los resultados en la pestaña 'Optimizaciones'")
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend")
        print("💡 Asegúrate de que el backend esté ejecutándose en http://localhost:8080")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    generate_test_stats() 