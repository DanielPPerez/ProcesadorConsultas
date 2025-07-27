#!/bin/bash

# Script para descargar JSONs grandes para pruebas de rendimiento
# Autor: Procesador de Consultas JSON

echo "🚀 Descargador de JSONs para Pruebas de Rendimiento"
echo "=================================================="

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado"
    echo "Por favor instala Python desde https://python.org"
    exit 1
fi

# Verificar si requests está instalado
if ! python3 -c "import requests" &> /dev/null; then
    echo "📦 Instalando dependencias..."
    pip3 install -r requirements.txt
fi

echo ""
echo "📥 Opciones disponibles:"
echo "1. JSONPlaceholder (posts, users, comments)"
echo "2. GitHub API (usuarios, repositorios)"
echo "3. Random User API (usuarios aleatorios)"
echo "4. Datos de e-commerce (simulado)"
echo "5. Todos los datos"
echo "6. Generar JSON grande personalizado"
echo ""

read -p "Selecciona una opción (1-6): " choice

case $choice in
    1)
        echo ""
        python3 download_test_data.py jsonplaceholder
        ;;
    2)
        echo ""
        python3 download_test_data.py github
        ;;
    3)
        echo ""
        python3 download_test_data.py randomuser
        ;;
    4)
        echo ""
        python3 download_test_data.py ecommerce
        ;;
    5)
        echo ""
        python3 download_test_data.py all
        ;;
    6)
        echo ""
        read -p "Número de usuarios (default 1000): " users
        users=${users:-1000}
        python3 generate_test_json.py large $users
        ;;
    *)
        echo "❌ Opción no válida"
        ;;
esac

echo ""
echo "✅ Proceso completado!"
echo "📁 Los archivos JSON están en el directorio actual"
echo ""

# Copiar archivos al frontend
echo "📂 Copiando archivos al frontend..."
python3 copy_json_to_frontend.py

echo ""
echo "🎉 ¡Listo! Ahora puedes usar el botón 'Cargar JSON Grande' en la interfaz web"
echo "" 