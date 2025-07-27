#!/usr/bin/env python3
"""
Script para descargar JSONs de APIs públicas para pruebas de rendimiento
Autor: Procesador de Consultas JSON
"""

import requests
import json
import sys
import os
from datetime import datetime

def download_json(url, filename, description=""):
    """Descarga un JSON de una URL"""
    print(f"📥 Descargando {description}...")
    print(f"🔗 URL: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Guardar archivo
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # Calcular tamaño
        file_size = len(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        file_size_mb = file_size / (1024 * 1024)
        
        print(f"✅ Descarga exitosa!")
        print(f"📁 Archivo: {filename}")
        print(f"📊 Tamaño: {file_size_mb:.2f} MB")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al descargar: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error al parsear JSON: {e}")
        return None

def download_jsonplaceholder_data():
    """Descarga datos de JSONPlaceholder"""
    print("\n🌐 Descargando datos de JSONPlaceholder...")
    
    base_url = "https://jsonplaceholder.typicode.com"
    endpoints = [
        ("/posts", "jsonplaceholder_posts.json", "Posts"),
        ("/users", "jsonplaceholder_users.json", "Usuarios"),
        ("/comments", "jsonplaceholder_comments.json", "Comentarios"),
        ("/photos", "jsonplaceholder_photos.json", "Fotos"),
        ("/todos", "jsonplaceholder_todos.json", "Tareas")
    ]
    
    for endpoint, filename, description in endpoints:
        url = base_url + endpoint
        download_json(url, filename, description)

def download_github_data():
    """Descarga datos de GitHub API"""
    print("\n🐙 Descargando datos de GitHub API...")
    
    # Datos públicos de GitHub
    endpoints = [
        ("https://api.github.com/users/octocat", "github_user.json", "Usuario GitHub"),
        ("https://api.github.com/repos/octocat/Hello-World", "github_repo.json", "Repositorio GitHub"),
        ("https://api.github.com/repos/octocat/Hello-World/issues", "github_issues.json", "Issues GitHub")
    ]
    
    for url, filename, description in endpoints:
        download_json(url, filename, description)

def download_random_user_data():
    """Descarga datos de Random User API"""
    print("\n👤 Descargando datos de Random User API...")
    
    # Generar múltiples usuarios
    for i in range(1, 6):
        url = f"https://randomuser.me/api/?results={i*100}&format=json"
        filename = f"random_users_{i*100}.json"
        description = f"{i*100} usuarios aleatorios"
        download_json(url, filename, description)

def download_weather_data():
    """Descarga datos de OpenWeatherMap (ejemplo)"""
    print("\n🌤️ Descargando datos de clima (ejemplo)...")
    
    # Nota: Para usar OpenWeatherMap necesitas una API key
    # Este es un ejemplo con datos simulados
    weather_data = {
        "metadata": {
            "source": "OpenWeatherMap (simulado)",
            "generated_at": datetime.now().isoformat(),
            "description": "Datos de clima para pruebas"
        },
        "cities": [
            {
                "id": 1,
                "name": "New York",
                "country": "US",
                "weather": {
                    "temperature": 22.5,
                    "humidity": 65,
                    "description": "Partly cloudy",
                    "wind_speed": 12.3
                },
                "forecast": [
                    {
                        "date": "2024-01-15",
                        "temp_min": 18,
                        "temp_max": 25,
                        "description": "Sunny"
                    },
                    {
                        "date": "2024-01-16",
                        "temp_min": 15,
                        "temp_max": 22,
                        "description": "Cloudy"
                    }
                ]
            }
        ]
    }
    
    filename = "weather_data.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(weather_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Datos de clima generados: {filename}")

def download_ecommerce_data():
    """Descarga datos de e-commerce (simulado)"""
    print("\n🛒 Generando datos de e-commerce...")
    
    # Datos simulados de e-commerce
    ecommerce_data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "description": "Datos de e-commerce para pruebas"
        },
        "products": [
            {
                "id": i,
                "name": f"Producto {i}",
                "category": f"Categoría {i % 5 + 1}",
                "price": round(10 + (i * 1.5), 2),
                "stock": 100 - (i % 50),
                "rating": round(1 + (i % 5), 1),
                "reviews": [
                    {
                        "user": f"Usuario {j}",
                        "rating": round(1 + (j % 5), 1),
                        "comment": f"Comentario {j} del producto {i}",
                        "date": datetime.now().isoformat()
                    }
                    for j in range(1, 6)
                ],
                "specifications": {
                    "brand": f"Marca {i}",
                    "model": f"Modelo {i}",
                    "weight": f"{i * 0.5} kg",
                    "dimensions": f"{i * 10}x{i * 8}x{i * 5} cm"
                }
            }
            for i in range(1, 101)
        ],
        "orders": [
            {
                "id": f"ORD-{i:06d}",
                "customer": {
                    "name": f"Cliente {i}",
                    "email": f"cliente{i}@example.com",
                    "phone": f"+1-555-{i:04d}"
                },
                "items": [
                    {
                        "product_id": j,
                        "quantity": j % 3 + 1,
                        "price": round(10 + (j * 1.5), 2)
                    }
                    for j in range(1, (i % 5) + 2)
                ],
                "total": round(sum(j * (10 + (j * 1.5)) for j in range(1, (i % 5) + 2)), 2),
                "status": ["pending", "shipped", "delivered"][i % 3],
                "created_at": datetime.now().isoformat()
            }
            for i in range(1, 51)
        ]
    }
    
    filename = "ecommerce_data.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(ecommerce_data, f, indent=2, ensure_ascii=False)
    
    file_size = len(json.dumps(ecommerce_data, ensure_ascii=False).encode('utf-8'))
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"✅ Datos de e-commerce generados: {filename}")
    print(f"📊 Tamaño: {file_size_mb:.2f} MB")

def main():
    """Función principal"""
    print("🚀 Descargador de JSONs para Pruebas de Rendimiento")
    print("=" * 55)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "jsonplaceholder":
            download_jsonplaceholder_data()
            
        elif command == "github":
            download_github_data()
            
        elif command == "randomuser":
            download_random_user_data()
            
        elif command == "weather":
            download_weather_data()
            
        elif command == "ecommerce":
            download_ecommerce_data()
            
        elif command == "all":
            download_jsonplaceholder_data()
            download_github_data()
            download_random_user_data()
            download_weather_data()
            download_ecommerce_data()
            
        else:
            print("❌ Comando no reconocido")
            print_usage()
    else:
        print_usage()

def print_usage():
    """Muestra el uso del script"""
    print("\n📖 Uso:")
    print("  python download_test_data.py jsonplaceholder  # Datos de JSONPlaceholder")
    print("  python download_test_data.py github          # Datos de GitHub API")
    print("  python download_test_data.py randomuser      # Datos de Random User API")
    print("  python download_test_data.py weather         # Datos de clima (simulado)")
    print("  python download_test_data.py ecommerce       # Datos de e-commerce (simulado)")
    print("  python download_test_data.py all             # Todos los tipos de datos")
    print("\n💡 Ejemplos de consultas para probar:")
    print("  users.0.name                                # Nombre del primer usuario")
    print("  users.0.address.city                        # Ciudad del primer usuario")
    print("  products.0.reviews.0.rating                 # Rating de la primera review")
    print("  orders.0.items.0.product_id                 # ID del primer producto en orden")

if __name__ == "__main__":
    main() 