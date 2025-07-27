#!/usr/bin/env python3
"""
Script para generar JSONs grandes para pruebas de rendimiento
Autor: Procesador de Consultas JSON
"""

import json
import random
import string
import sys
from datetime import datetime, timedelta

def generate_random_string(length=10):
    """Genera una cadena aleatoria"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_email():
    """Genera un email aleatorio"""
    domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'example.com']
    username = generate_random_string(8)
    domain = random.choice(domains)
    return f"{username}@{domain}"

def generate_random_address():
    """Genera una dirección aleatoria"""
    streets = ['Main St', 'Oak Ave', 'Pine Rd', 'Elm St', 'Cedar Ln', 'Maple Dr']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia']
    states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA']
    
    return {
        "street": f"{random.randint(1, 9999)} {random.choice(streets)}",
        "city": random.choice(cities),
        "state": random.choice(states),
        "country": "USA",
        "zipCode": f"{random.randint(10000, 99999)}"
    }

def generate_random_post():
    """Genera un post aleatorio"""
    titles = [
        "The Future of Technology",
        "Programming Best Practices",
        "Web Development Trends",
        "Data Science Insights",
        "Artificial Intelligence Advances",
        "Cloud Computing Solutions",
        "Cybersecurity Tips",
        "Mobile App Development"
    ]
    
    content = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * random.randint(5, 15)
    
    return {
        "id": random.randint(1, 10000),
        "title": random.choice(titles),
        "content": content,
        "tags": random.sample(["technology", "programming", "web", "data", "ai", "cloud"], random.randint(2, 4)),
        "likes": random.randint(0, 1000),
        "comments": [
            {
                "id": random.randint(1, 100000),
                "author": generate_random_string(8),
                "content": "Great post! " * random.randint(1, 3),
                "timestamp": (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat()
            }
            for _ in range(random.randint(0, 5))
        ]
    }

def generate_user_profile():
    """Genera un perfil de usuario completo"""
    user_id = random.randint(1, 100000)
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
        "posts": [generate_random_post() for _ in range(random.randint(1, 10))],
        "created_at": (datetime.now() - timedelta(days=random.randint(0, 1000))).isoformat(),
        "last_login": (datetime.now() - timedelta(hours=random.randint(0, 24*7))).isoformat()
    }

def generate_large_json(num_users=1000, output_file="large_test_data.json"):
    """Genera un JSON grande con usuarios"""
    print(f"Generando JSON con {num_users} usuarios...")
    
    data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "total_users": num_users,
            "description": "JSON generado para pruebas de rendimiento"
        },
        "users": [generate_user_profile() for _ in range(num_users)]
    }
    
    # Calcular estadísticas
    total_posts = sum(len(user["posts"]) for user in data["users"])
    total_comments = sum(
        sum(len(post["comments"]) for post in user["posts"])
        for user in data["users"]
    )
    
    data["metadata"]["total_posts"] = total_posts
    data["metadata"]["total_comments"] = total_comments
    
    # Guardar archivo
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Calcular tamaño
    file_size = len(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"✅ JSON generado exitosamente!")
    print(f"📁 Archivo: {output_file}")
    print(f"📊 Tamaño: {file_size_mb:.2f} MB")
    print(f"👥 Usuarios: {num_users}")
    print(f"📝 Posts: {total_posts}")
    print(f"💬 Comentarios: {total_comments}")
    
    return data

def generate_nested_json(depth=10, output_file="deep_nested_data.json"):
    """Genera un JSON con estructura muy anidada"""
    print(f"Generando JSON anidado con profundidad {depth}...")
    
    def create_nested_structure(current_depth, max_depth):
        if current_depth >= max_depth:
            return {
                "value": generate_random_string(20),
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
    
    data = {
        "metadata": {
            "depth": depth,
            "generated_at": datetime.now().isoformat(),
            "description": "JSON con estructura muy anidada para pruebas"
        },
        "root": create_nested_structure(0, depth)
    }
    
    # Guardar archivo
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Calcular tamaño
    file_size = len(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"✅ JSON anidado generado exitosamente!")
    print(f"📁 Archivo: {output_file}")
    print(f"📊 Tamaño: {file_size_mb:.2f} MB")
    print(f"🔍 Profundidad máxima: {depth}")
    
    return data

def main():
    """Función principal"""
    print("🚀 Generador de JSONs para Pruebas de Rendimiento")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "large":
            num_users = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
            generate_large_json(num_users)
            
        elif command == "nested":
            depth = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            generate_nested_json(depth)
            
        elif command == "both":
            num_users = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
            depth = int(sys.argv[3]) if len(sys.argv) > 3 else 10
            
            generate_large_json(num_users)
            generate_nested_json(depth)
            
        else:
            print("❌ Comando no reconocido")
            print_usage()
    else:
        print_usage()

def print_usage():
    """Muestra el uso del script"""
    print("\n📖 Uso:")
    print("  python generate_test_json.py large [num_users]     # JSON grande con usuarios")
    print("  python generate_test_json.py nested [depth]        # JSON anidado profundo")
    print("  python generate_test_json.py both [users] [depth]  # Ambos tipos")
    print("\n💡 Ejemplos:")
    print("  python generate_test_json.py large 5000            # 5000 usuarios")
    print("  python generate_test_json.py nested 15             # Profundidad 15")
    print("  python generate_test_json.py both 2000 12          # Ambos")

if __name__ == "__main__":
    main() 