#!/bin/bash

# Script de configuración para el Procesador de Consultas JSON
# Este script instala las dependencias y configura el entorno

set -e

echo "🚀 Configurando Procesador de Consultas JSON..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar que Go esté instalado
check_go() {
    if ! command -v go &> /dev/null; then
        print_error "Go no está instalado. Por favor instala Go 1.21 o superior."
        exit 1
    fi
    
    GO_VERSION=$(go version | awk '{print $3}' | sed 's/go//')
    print_success "Go $GO_VERSION detectado"
}

# Verificar que Node.js esté instalado
check_node() {
    if ! command -v node &> /dev/null; then
        print_error "Node.js no está instalado. Por favor instala Node.js 16 o superior."
        exit 1
    fi
    
    NODE_VERSION=$(node --version | sed 's/v//')
    print_success "Node.js $NODE_VERSION detectado"
}

# Configurar backend
setup_backend() {
    print_status "Configurando backend..."
    
    cd backend
    
    # Instalar dependencias de Go
    print_status "Instalando dependencias de Go..."
    go mod tidy
    
    # Verificar que las dependencias se instalaron correctamente
    if [ $? -eq 0 ]; then
        print_success "Dependencias de Go instaladas correctamente"
    else
        print_error "Error instalando dependencias de Go"
        exit 1
    fi
    
    # Compilar para verificar que todo funciona
    print_status "Compilando backend..."
    go build -o procesador-consultas .
    
    if [ $? -eq 0 ]; then
        print_success "Backend compilado correctamente"
        rm procesador-consultas # Limpiar binario de prueba
    else
        print_error "Error compilando backend"
        exit 1
    fi
    
    cd ..
}

# Configurar frontend
setup_frontend() {
    print_status "Configurando frontend..."
    
    cd frontend
    
    # Instalar dependencias de Node.js
    print_status "Instalando dependencias de Node.js..."
    npm install
    
    if [ $? -eq 0 ]; then
        print_success "Dependencias de Node.js instaladas correctamente"
    else
        print_error "Error instalando dependencias de Node.js"
        exit 1
    fi
    
    cd ..
}

# Crear archivo de configuración
create_config() {
    print_status "Creando archivo de configuración..."
    
    cat > .env << EOF
# Configuración del Procesador de Consultas JSON

# Backend
BACKEND_PORT=8080
BACKEND_HOST=localhost

# Frontend
FRONTEND_PORT=3000
FRONTEND_HOST=localhost

# Configuración de desarrollo
NODE_ENV=development
GIN_MODE=debug
EOF

    print_success "Archivo .env creado"
}

# Crear script de ejecución
create_run_script() {
    print_status "Creando script de ejecución..."
    
    cat > run.sh << 'EOF'
#!/bin/bash

# Script para ejecutar el Procesador de Consultas JSON

set -e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🚀 Iniciando Procesador de Consultas JSON...${NC}"

# Función para limpiar procesos al salir
cleanup() {
    echo -e "${BLUE}🛑 Deteniendo servicios...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 0
}

# Capturar Ctrl+C
trap cleanup SIGINT

# Iniciar backend
echo -e "${GREEN}📡 Iniciando backend en puerto 8080...${NC}"
cd backend
go run main.go &
BACKEND_PID=$!
cd ..

# Esperar un momento para que el backend inicie
sleep 2

# Iniciar frontend
echo -e "${GREEN}🌐 Iniciando frontend en puerto 3000...${NC}"
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo -e "${GREEN}✅ Servicios iniciados correctamente${NC}"
echo -e "${BLUE}📱 Frontend: http://localhost:3000${NC}"
echo -e "${BLUE}🔧 Backend: http://localhost:8080${NC}"
echo -e "${BLUE}📊 Health Check: http://localhost:8080/health${NC}"
echo ""
echo -e "${BLUE}Presiona Ctrl+C para detener los servicios${NC}"

# Esperar a que los procesos terminen
wait
EOF

    chmod +x run.sh
    print_success "Script run.sh creado"
}

# Función principal
main() {
    print_status "Iniciando configuración del proyecto..."
    
    # Verificar dependencias
    check_go
    check_node
    
    # Configurar componentes
    setup_backend
    setup_frontend
    
    # Crear archivos de configuración
    create_config
    create_run_script
    
    print_success "✅ Configuración completada exitosamente!"
    echo ""
    echo -e "${BLUE}🎉 El proyecto está listo para usar:${NC}"
    echo -e "${GREEN}• Ejecuta './run.sh' para iniciar todos los servicios${NC}"
    echo -e "${GREEN}• O ejecuta manualmente:${NC}"
    echo -e "${BLUE}  - Backend: cd backend && go run main.go${NC}"
    echo -e "${BLUE}  - Frontend: cd frontend && npm start${NC}"
    echo ""
    echo -e "${BLUE}📚 Documentación disponible en docs/ARQUITECTURA.md${NC}"
}

# Ejecutar función principal
main "$@" 