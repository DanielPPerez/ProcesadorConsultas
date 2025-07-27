@echo off
setlocal enabledelayedexpansion

REM Script de configuración para el Procesador de Consultas JSON (Windows)
REM Este script instala las dependencias y configura el entorno

echo 🚀 Configurando Procesador de Consultas JSON...

REM Verificar que Go esté instalado
echo [INFO] Verificando Go...
go version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Go no está instalado. Por favor instala Go 1.21 o superior.
    exit /b 1
)
for /f "tokens=3" %%i in ('go version') do set GO_VERSION=%%i
echo [SUCCESS] Go !GO_VERSION! detectado

REM Verificar que Node.js esté instalado
echo [INFO] Verificando Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js no está instalado. Por favor instala Node.js 16 o superior.
    exit /b 1
)
for /f "tokens=1" %%i in ('node --version') do set NODE_VERSION=%%i
echo [SUCCESS] Node.js !NODE_VERSION! detectado

REM Configurar backend
echo [INFO] Configurando backend...
cd backend

echo [INFO] Instalando dependencias de Go...
go mod tidy
if %errorlevel% neq 0 (
    echo [ERROR] Error instalando dependencias de Go
    exit /b 1
)
echo [SUCCESS] Dependencias de Go instaladas correctamente

echo [INFO] Compilando backend...
go build -o procesador-consultas.exe .
if %errorlevel% neq 0 (
    echo [ERROR] Error compilando backend
    exit /b 1
)
echo [SUCCESS] Backend compilado correctamente
del procesador-consultas.exe >nul 2>&1

cd ..

REM Configurar frontend
echo [INFO] Configurando frontend...
cd frontend

echo [INFO] Instalando dependencias de Node.js...
call npm install
if %errorlevel% neq 0 (
    echo [ERROR] Error instalando dependencias de Node.js
    exit /b 1
)
echo [SUCCESS] Dependencias de Node.js instaladas correctamente

cd ..

REM Crear archivo de configuración
echo [INFO] Creando archivo de configuración...
(
echo # Configuración del Procesador de Consultas JSON
echo.
echo # Backend
echo BACKEND_PORT=8080
echo BACKEND_HOST=localhost
echo.
echo # Frontend
echo FRONTEND_PORT=3000
echo FRONTEND_HOST=localhost
echo.
echo # Configuración de desarrollo
echo NODE_ENV=development
echo GIN_MODE=debug
) > .env

echo [SUCCESS] Archivo .env creado

REM Crear script de ejecución para Windows
echo [INFO] Creando script de ejecución...
(
echo @echo off
echo REM Script para ejecutar el Procesador de Consultas JSON
echo.
echo echo 🚀 Iniciando Procesador de Consultas JSON...
echo.
echo REM Iniciar backend
echo echo 📡 Iniciando backend en puerto 8080...
echo cd backend
echo start "Backend" cmd /k "go run main.go"
echo cd ..
echo.
echo REM Esperar un momento para que el backend inicie
echo timeout /t 3 /nobreak ^>nul
echo.
echo REM Iniciar frontend
echo echo 🌐 Iniciando frontend en puerto 3000...
echo cd frontend
echo start "Frontend" cmd /k "npm start"
echo cd ..
echo.
echo echo ✅ Servicios iniciados correctamente
echo echo 📱 Frontend: http://localhost:3000
echo echo 🔧 Backend: http://localhost:8080
echo echo 📊 Health Check: http://localhost:8080/health
echo echo.
echo echo Presiona cualquier tecla para salir...
echo pause ^>nul
) > run.bat

echo [SUCCESS] Script run.bat creado

echo.
echo [SUCCESS] ✅ Configuración completada exitosamente!
echo.
echo 🎉 El proyecto está listo para usar:
echo • Ejecuta 'run.bat' para iniciar todos los servicios
echo • O ejecuta manualmente:
echo   - Backend: cd backend ^&^& go run main.go
echo   - Frontend: cd frontend ^&^& npm start
echo.
echo 📚 Documentación disponible en docs/ARQUITECTURA.md

pause 