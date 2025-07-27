@echo off
REM Script para descargar JSONs grandes para pruebas de rendimiento
REM Autor: Procesador de Consultas JSON

echo 🚀 Descargador de JSONs para Pruebas de Rendimiento
echo ===================================================

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

REM Verificar si requests está instalado
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando dependencias...
    pip install -r requirements.txt
)

echo.
echo 📥 Opciones disponibles:
echo 1. JSONPlaceholder (posts, users, comments)
echo 2. GitHub API (usuarios, repositorios)
echo 3. Random User API (usuarios aleatorios)
echo 4. Datos de e-commerce (simulado)
echo 5. Todos los datos
echo 6. Generar JSON grande personalizado
echo.

set /p choice="Selecciona una opción (1-6): "

if "%choice%"=="1" (
    echo.
    python download_test_data.py jsonplaceholder
) else if "%choice%"=="2" (
    echo.
    python download_test_data.py github
) else if "%choice%"=="3" (
    echo.
    python download_test_data.py randomuser
) else if "%choice%"=="4" (
    echo.
    python download_test_data.py ecommerce
) else if "%choice%"=="5" (
    echo.
    python download_test_data.py all
) else if "%choice%"=="6" (
    echo.
    set /p users="Número de usuarios (default 1000): "
    if "%users%"=="" set users=1000
    python generate_test_json.py large %users%
) else (
    echo ❌ Opción no válida
)

echo.
echo ✅ Proceso completado!
echo 📁 Los archivos JSON están en el directorio actual
echo.

REM Copiar archivos al frontend
echo 📂 Copiando archivos al frontend...
python copy_json_to_frontend.py

echo.
echo 🎉 ¡Listo! Ahora puedes usar el botón "Cargar JSON Grande" en la interfaz web
pause 