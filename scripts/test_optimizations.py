#!/usr/bin/env python3
"""
Script para probar las optimizaciones y verificar estadísticas
Autor: Procesador de Consultas JSON
"""

import requests
import json
import time

def test_optimizations():
    """Prueba las optimizaciones y verifica que las estadísticas se actualizan"""
    
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
        "users.1.profile.email"
    ]
    
    print("🚀 Probando Optimizaciones...")
    print("=" * 40)
    
    try:
        # Verificar que el backend esté funcionando
        print("1. Verificando backend...")
        response = requests.get(f"{base_url}/health")
        if response.status_code != 200:
            print("❌ Backend no está funcionando")
            return
        print("✅ Backend funcionando")
        
        # Obtener estadísticas iniciales
        print("\n2. Estadísticas iniciales...")
        response = requests.get(f"{base_url}/optimization/stats")
        if response.status_code == 200:
            initial_stats = response.json()
            print(f"   Consultas totales: {initial_stats.get('optimization_stats', {}).get('TotalQueries', 0)}")
            print(f"   Consultas optimizadas: {initial_stats.get('optimization_stats', {}).get('OptimizedQueries', 0)}")
            print(f"   Cache hits: {initial_stats.get('optimization_stats', {}).get('CacheHits', 0)}")
        
        # Ejecutar consultas optimizadas
        print("\n3. Ejecutando consultas optimizadas...")
        for i, query in enumerate(queries, 1):
            print(f"   Consulta {i}: {query}")
            
            # Ejecutar consulta optimizada
            response = requests.post(f"{base_url}/query/update-stats", 
                                   json={"json": json.dumps(test_json), "query": query})
            
            if response.status_code == 200:
                print(f"   ✅ Consulta {i} exitosa")
            else:
                print(f"   ❌ Error en consulta {i}: {response.status_code}")
            
            # Pequeña pausa para ver los cambios
            time.sleep(0.5)
        
        # Verificar estadísticas finales
        print("\n4. Estadísticas finales...")
        response = requests.get(f"{base_url}/optimization/stats")
        if response.status_code == 200:
            final_stats = response.json()
            print("✅ Estadísticas finales:")
            print(f"   Consultas totales: {final_stats.get('optimization_stats', {}).get('TotalQueries', 0)}")
            print(f"   Consultas optimizadas: {final_stats.get('optimization_stats', {}).get('OptimizedQueries', 0)}")
            print(f"   Cache hits: {final_stats.get('optimization_stats', {}).get('CacheHits', 0)}")
            print(f"   Tiempo promedio: {final_stats.get('optimization_stats', {}).get('AverageOptimizationTime', '0ms')}")
        
        # Probar cache hits ejecutando las mismas consultas
        print("\n5. Probando cache hits...")
        for i, query in enumerate(queries, 1):
            print(f"   Repitiendo consulta {i}: {query}")
            
            response = requests.post(f"{base_url}/query/update-stats", 
                                   json={"json": json.dumps(test_json), "query": query})
            
            if response.status_code == 200:
                print(f"   ✅ Cache hit para consulta {i}")
            else:
                print(f"   ❌ Error en cache hit {i}")
            
            time.sleep(0.5)
        
        # Verificar estadísticas después de cache hits
        print("\n6. Estadísticas después de cache hits...")
        response = requests.get(f"{base_url}/optimization/stats")
        if response.status_code == 200:
            cache_stats = response.json()
            print("✅ Estadísticas con cache:")
            print(f"   Consultas totales: {cache_stats.get('optimization_stats', {}).get('TotalQueries', 0)}")
            print(f"   Consultas optimizadas: {cache_stats.get('optimization_stats', {}).get('OptimizedQueries', 0)}")
            print(f"   Cache hits: {cache_stats.get('optimization_stats', {}).get('CacheHits', 0)}")
        
        print("\n🎉 Pruebas de optimización completadas!")
        print("\n💡 Ahora puedes ver las estadísticas actualizadas en la interfaz web")
        
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al backend")
        print("💡 Asegúrate de que el backend esté ejecutándose en http://localhost:8080")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    test_optimizations() 