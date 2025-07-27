#!/usr/bin/env python3
"""
Script para generar y copiar archivos JSON al frontend
Autor: Procesador de Consultas JSON
"""

import json
import random
import string
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path

def generate_large_json(num_users=1000):
    """Genera un JSON grande con usuarios"""
    print(f"Generando JSON con {num_users} usuarios...")
    
    def generate_user_profile(user_id):
        return {
            "id": user_id,
            "name": f"Usuario {user_id}",
            "email": f"user{user_id}@example.com",
            "phone": f"+1-555-{user_id:04d}",
            "address": {
                "street": f"{user_id} Main St",
                "city": random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']),
                "state": random.choice(['NY', 'CA', 'IL', 'TX', 'AZ']),
                "country": "USA",
                "zipCode": f"{10000 + user_id}"
            },
            "profile": {
                "avatar": f"https://example.com/avatars/user{user_id}.jpg",
                "bio": f"Software developer with {random.randint(1, 20)} years of experience",
                "website": f"https://user{user_id}.com",
                "preferences": {
                    "theme": random.choice(["light", "dark", "auto"]),
                    "language": random.choice(["en", "es", "fr", "de"]),
                    "notifications": random.choice([True, False]),
                    "timezone": random.choice(["UTC", "EST", "PST", "CST"])
                },
                "social": {
                    "twitter": f"@user{user_id}",
                    "linkedin": f"linkedin.com/in/user{user_id}",
                    "github": f"github.com/user{user_id}"
                }
            },
            "posts": [
                {
                    "id": j + 1,
                    "title": f"Post {j + 1} del usuario {user_id}",
                    "content": f"Contenido del post {j + 1} del usuario {user_id}. Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                    "tags": ['technology', 'programming', 'web', 'data', 'ai', 'cloud'][:random.randint(2, 4)],
                    "likes": random.randint(0, 1000),
                    "comments": [
                        {
                            "id": k + 1,
                            "author": f"Usuario {k + 1}",
                            "content": f"Comentario {k + 1} del post {j + 1}",
                            "timestamp": datetime.now().isoformat()
                        }
                        for k in range(random.randint(0, 5))
                    ]
                }
                for j in range(random.randint(1, 10))
            ],
            "created_at": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat()
        }
    
    data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_users": num_users,
            "description": "JSON generado para pruebas de rendimiento"
        },
        "users": [generate_user_profile(i + 1) for i in range(num_users)]
    }
    
    return data

def setup_frontend_data():
    """Configura los archivos JSON para el frontend"""
    
    print("🚀 Configurando datos para el frontend...")
    print("=" * 50)
    
    # Directorios
    scripts_dir = Path("scripts")
    frontend_public_dir = Path("frontend/public")
    
    # Crear directorio público si no existe
    frontend_public_dir.mkdir(parents=True, exist_ok=True)
    
    # Generar JSON grande
    print("1. Generando JSON grande...")
    large_data = generate_large_json(1000)
    
    # Guardar archivo
    large_file = frontend_public_dir / "large_test_data.json"
    with open(large_file, 'w', encoding='utf-8') as f:
        json.dump(large_data, f, indent=2, ensure_ascii=False)
    
    # Calcular tamaño
    file_size = len(json.dumps(large_data, ensure_ascii=False).encode('utf-8'))
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"✅ JSON grande generado!")
    print(f"📁 Archivo: {large_file}")
    print(f"📊 Tamaño: {file_size_mb:.2f} MB")
    print(f"👥 Usuarios: 1000")
    
    # Generar JSON anidado también
    print("\n2. Generando JSON anidado...")
    nested_data = {
        "metadata": {
            "depth": 10,
            "generated_at": datetime.now().isoformat(),
            "description": "JSON con estructura muy anidada para pruebas"
        },
        "root": create_nested_structure(0, 10)
    }
    
    nested_file = frontend_public_dir / "deep_nested_data.json"
    with open(nested_file, 'w', encoding='utf-8') as f:
        json.dump(nested_data, f, indent=2, ensure_ascii=False)
    
    nested_size = len(json.dumps(nested_data, ensure_ascii=False).encode('utf-8'))
    nested_size_mb = nested_size / (1024 * 1024)
    
    print(f"✅ JSON anidado generado!")
    print(f"📁 Archivo: {nested_file}")
    print(f"📊 Tamaño: {nested_size_mb:.2f} MB")
    print(f"🔍 Profundidad máxima: 10")
    
    print("\n🎉 Datos del frontend configurados exitosamente!")
    print("💡 Ahora puedes usar el botón 'Cargar JSON Grande' en la interfaz web")

def create_nested_structure(current_depth, max_depth):
    """Crea una estructura anidada"""
    if current_depth >= max_depth:
        return {
            "value": ''.join(random.choices(string.ascii_letters + string.digits, k=20)),
            "number": random.randint(1, 1000),
            "boolean": random.choice([True, False]),
            "array": [random.randint(1, 100) for _ in range(random.randint(1, 5))]
        }
    
    return {
        f"level_{current_depth}": {
            f"data_{i}": create_nested_structure(current_depth + 1, max_depth)
            for i in range(random.randint(2, 5))
        },
        f"array_{current_depth}": [
            create_nested_structure(current_depth + 1, max_depth)
            for _ in range(random.randint(1, 3))
        ]
    }

if __name__ == "__main__":
    setup_frontend_data() 