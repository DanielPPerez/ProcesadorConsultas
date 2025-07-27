#!/bin/bash

# Script para probar las optimizaciones de código intermedio
# Autor: Procesador de Consultas JSON
# Fecha: $(date)

echo "🚀 Probando Optimizaciones de Código Intermedio"
echo "================================================"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con color
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[ℹ]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[⚠]${NC} $1"
}

# Verificar que el servidor esté corriendo
check_server() {
    print_info "Verificando que el servidor esté corriendo..."
    
    if curl -s http://localhost:8080/health > /dev/null; then
        print_status "Servidor backend está corriendo en http://localhost:8080"
        return 0
    else
        print_error "Servidor backend no está corriendo. Inicia el servidor primero:"
        echo "  cd backend && go run main.go"
        return 1
    fi
}

# Probar endpoint de estadísticas de optimización
test_optimization_stats() {
    print_info "Probando endpoint de estadísticas de optimización..."
    
    response=$(curl -s http://localhost:8080/optimization/stats)
    
    if [ $? -eq 0 ]; then
        print_status "Endpoint de estadísticas funcionando correctamente"
        echo "Respuesta: $response" | head -c 200
        echo "..."
    else
        print_error "Error al obtener estadísticas de optimización"
    fi
}

# Probar consulta optimizada
test_optimized_query() {
    print_info "Probando consulta optimizada..."
    
    json_data='{"user":{"name":"John","age":30,"address":{"city":"New York","country":"USA"}}}'
    query="user.address.city"
    
    response=$(curl -s -X POST http://localhost:8080/query/optimized \
        -H "Content-Type: application/json" \
        -d "{\"json\":\"$json_data\",\"query\":\"$query\"}")
    
    if [ $? -eq 0 ]; then
        print_status "Consulta optimizada funcionando correctamente"
        echo "Respuesta: $response" | head -c 200
        echo "..."
    else
        print_error "Error en consulta optimizada"
    fi
}

# Probar comparación optimizada
test_optimized_comparison() {
    print_info "Probando comparación optimizada..."
    
    json_data='{"data":{"items":[{"id":1,"value":"test"},{"id":2,"value":"example"}]}}'
    query="data.items.0.value"
    
    response=$(curl -s -X POST http://localhost:8080/query/optimized/compare \
        -H "Content-Type: application/json" \
        -d "{\"json\":\"$json_data\",\"query\":\"$query\"}")
    
    if [ $? -eq 0 ]; then
        print_status "Comparación optimizada funcionando correctamente"
        echo "Respuesta: $response" | head -c 300
        echo "..."
    else
        print_error "Error en comparación optimizada"
    fi
}

# Probar diferentes librerías con optimizaciones
test_library_optimizations() {
    print_info "Probando optimizaciones con diferentes librerías..."
    
    json_data='{"nested":{"deep":{"structure":{"value":"found"}}}}'
    query="nested.deep.structure.value"
    
    libraries=("standard" "json-iterator" "fastjson")
    
    for lib in "${libraries[@]}"; do
        print_info "Probando librería: $lib"
        
        response=$(curl -s -X POST "http://localhost:8080/query/optimized?library=$lib" \
            -H "Content-Type: application/json" \
            -d "{\"json\":\"$json_data\",\"query\":\"$query\"}")
        
        if [ $? -eq 0 ]; then
            print_status "Librería $lib optimizada funcionando"
        else
            print_error "Error con librería $lib optimizada"
        fi
    done
}

# Probar cache y memoización
test_cache_performance() {
    print_info "Probando rendimiento del cache..."
    
    json_data='{"test":{"data":{"value":"cached_result"}}}'
    query="test.data.value"
    
    # Primera consulta (sin cache)
    start_time=$(date +%s%N)
    response1=$(curl -s -X POST http://localhost:8080/query/optimized \
        -H "Content-Type: application/json" \
        -d "{\"json\":\"$json_data\",\"query\":\"$query\"}")
    end_time=$(date +%s%N)
    first_time=$((end_time - start_time))
    
    # Segunda consulta (con cache)
    start_time=$(date +%s%N)
    response2=$(curl -s -X POST http://localhost:8080/query/optimized \
        -H "Content-Type: application/json" \
        -d "{\"json\":\"$json_data\",\"query\":\"$query\"}")
    end_time=$(date +%s%N)
    second_time=$((end_time - start_time))
    
    if [ $second_time -lt $first_time ]; then
        print_status "Cache funcionando correctamente"
        echo "Primera consulta: ${first_time}ns"
        echo "Segunda consulta: ${second_time}ns"
        echo "Mejora: $(( (first_time - second_time) * 100 / first_time ))%"
    else
        print_warning "Cache no muestra mejora significativa"
    fi
}

# Probar consultas complejas
test_complex_queries() {
    print_info "Probando consultas complejas optimizadas..."
    
    json_data='{"users":[{"id":1,"profile":{"name":"Alice","settings":{"theme":"dark"}}},{"id":2,"profile":{"name":"Bob","settings":{"theme":"light"}}}]}'
    queries=("users.0.profile.name" "users.1.profile.settings.theme" "users.0.profile.settings.theme")
    
    for query in "${queries[@]}"; do
        print_info "Probando consulta: $query"
        
        response=$(curl -s -X POST http://localhost:8080/query/optimized \
            -H "Content-Type: application/json" \
            -d "{\"json\":\"$json_data\",\"query\":\"$query\"}")
        
        if [ $? -eq 0 ]; then
            print_status "Consulta compleja '$query' optimizada funcionando"
        else
            print_error "Error en consulta compleja '$query'"
        fi
    done
}

# Mostrar estadísticas finales
show_final_stats() {
    print_info "Obteniendo estadísticas finales..."
    
    stats=$(curl -s http://localhost:8080/optimization/stats)
    
    if [ $? -eq 0 ]; then
        print_status "Estadísticas de optimización:"
        echo "$stats" | python3 -m json.tool 2>/dev/null || echo "$stats"
    else
        print_error "No se pudieron obtener estadísticas finales"
    fi
}

# Función principal
main() {
    echo ""
    print_info "Iniciando pruebas de optimizaciones..."
    echo ""
    
    # Verificar servidor
    if ! check_server; then
        exit 1
    fi
    
    # Ejecutar pruebas
    test_optimization_stats
    echo ""
    
    test_optimized_query
    echo ""
    
    test_optimized_comparison
    echo ""
    
    test_library_optimizations
    echo ""
    
    test_cache_performance
    echo ""
    
    test_complex_queries
    echo ""
    
    show_final_stats
    echo ""
    
    print_status "✅ Todas las pruebas completadas"
    print_info "Revisa la interfaz web en http://localhost:3000 para más detalles"
}

# Ejecutar función principal
main "$@" 