package engine

import (
	"encoding/json"
	"fmt"
	"sync"
	"time"

	"procesador-consultas/optimizer"

	jsoniter "github.com/json-iterator/go"
)

// OptimizedEngine representa el motor de consultas optimizado
type OptimizedEngine struct {
	*Engine
	optimizer *optimizer.Optimizer
	pool      *QueryPool
	stats     *OptimizedEngineStats
	statsMux  sync.RWMutex
}

// OptimizedEngineStats contiene estadísticas del motor optimizado
type OptimizedEngineStats struct {
	TotalQueries            int64
	OptimizedQueries        int64
	CacheHits               int64
	AverageOptimizationTime time.Duration
	TotalOptimizationTime   time.Duration
}

// QueryPool representa un pool de consultas para reutilización
type QueryPool struct {
	queries map[string]*QueryPlan
	mux     sync.RWMutex
}

// QueryPlan representa un plan de consulta optimizado
type QueryPlan struct {
	Query     []string
	Plan      *optimizer.QueryPlan
	CreatedAt time.Time
	UsedCount int64
}

// NewOptimizedEngine crea un nuevo motor optimizado
func NewOptimizedEngine() *OptimizedEngine {
	config := &optimizer.OptimizationConfig{
		EnableCache:       true,
		EnableMemoization: true,
		MaxCacheSize:      1000,
		EnableParallel:    true,
		OptimizationLevel: 2,
	}

	optimizedEngine := &OptimizedEngine{
		Engine:    NewEngine(),
		optimizer: optimizer.NewOptimizer(config),
		pool: &QueryPool{
			queries: make(map[string]*QueryPlan),
		},
		stats: &OptimizedEngineStats{},
	}

	return optimizedEngine
}

// QueryWithOptimization ejecuta una consulta con optimizaciones
func (oe *OptimizedEngine) QueryWithOptimization(jsonStr string, keys []string, library string) QueryResult {
	// Actualizar estadísticas
	oe.statsMux.Lock()
	oe.stats.TotalQueries++
	oe.statsMux.Unlock()

	// Generar clave de consulta
	queryKey := oe.generateQueryKey(keys, library)

	// Verificar pool de consultas
	if cached := oe.getFromPool(queryKey); cached != nil {
		oe.statsMux.Lock()
		oe.stats.CacheHits++
		oe.statsMux.Unlock()

		// Ejecutar consulta con plan optimizado
		return oe.executeOptimizedQuery(jsonStr, cached.Plan, library)
	}

	// Parsear JSON según la librería
	var data interface{}
	var parseErr error

	switch library {
	case "json-iterator":
		parseErr = jsoniter.Unmarshal([]byte(jsonStr), &data)
	case "fastjson":
		// Para fastjson, usamos la implementación existente
		return oe.QueryWithFastJSON(jsonStr, keys)
	default:
		parseErr = json.Unmarshal([]byte(jsonStr), &data)
	}

	if parseErr != nil {
		return QueryResult{
			Error: fmt.Sprintf("error parseando JSON: %v", parseErr),
			Keys:  keys,
		}
	}

	// Optimizar consulta
	optimizationStart := time.Now()
	plan := oe.optimizer.OptimizeQuery(keys, data)
	oe.stats.TotalOptimizationTime += time.Since(optimizationStart)

	// Guardar en pool
	oe.saveToPool(queryKey, &QueryPlan{
		Query:     keys,
		Plan:      plan,
		CreatedAt: time.Now(),
		UsedCount: 1,
	})

	// Ejecutar consulta optimizada
	result := oe.executeOptimizedQuery(jsonStr, plan, library)

	// Actualizar estadísticas
	oe.statsMux.Lock()
	oe.stats.OptimizedQueries++
	oe.statsMux.Unlock()

	return result
}

// executeOptimizedQuery ejecuta una consulta usando un plan optimizado
func (oe *OptimizedEngine) executeOptimizedQuery(jsonStr string, plan *optimizer.QueryPlan, library string) QueryResult {
	start := time.Now()

	result := QueryResult{
		Keys: []string{plan.Steps[0].Target}, // Usar el primer paso como clave
		Performance: Performance{
			LibraryType: library,
		},
	}

	// Ejecutar pasos del plan optimizado
	var current interface{}
	var parseErr error

	// Parsear JSON una sola vez
	parseStart := time.Now()
	switch library {
	case "json-iterator":
		parseErr = jsoniter.Unmarshal([]byte(jsonStr), &current)
	case "fastjson":
		// Para fastjson, usar implementación existente
		return oe.QueryWithFastJSON(jsonStr, []string{plan.Steps[0].Target})
	default:
		parseErr = json.Unmarshal([]byte(jsonStr), &current)
	}

	if parseErr != nil {
		result.Error = fmt.Sprintf("error parseando JSON: %v", parseErr)
		result.Performance.TotalTime = time.Since(start)
		return result
	}

	result.Performance.ParseTime = time.Since(parseStart)

	// Ejecutar pasos optimizados
	queryStart := time.Now()
	for _, step := range plan.Steps {
		switch step.Type {
		case "navigation", "direct_access":
			if value, found := oe.navigateOptimized(current, step.Target); found {
				current = value
			} else {
				result.Error = fmt.Sprintf("no se encontró el valor para: %s", step.Target)
				result.Performance.TotalTime = time.Since(start)
				return result
			}
		case "combined_navigation":
			// Para navegación combinada, dividir y ejecutar
			keys := oe.splitCombinedKey(step.Target)
			for _, key := range keys {
				if value, found := oe.navigateOptimized(current, key); found {
					current = value
				} else {
					result.Error = fmt.Sprintf("no se encontró el valor para: %s", key)
					result.Performance.TotalTime = time.Since(start)
					return result
				}
			}
		case "memoization":
			// Verificar cache (implementación simplificada)
			continue
		}
	}

	result.Performance.QueryTime = time.Since(queryStart)
	result.Performance.TotalTime = time.Since(start)
	result.Value = current
	result.Found = true

	return result
}

// navigateOptimized navega por la estructura JSON de forma optimizada
func (oe *OptimizedEngine) navigateOptimized(data interface{}, key string) (interface{}, bool) {
	switch v := data.(type) {
	case map[string]interface{}:
		if value, exists := v[key]; exists {
			return value, true
		}
	case map[interface{}]interface{}:
		if value, exists := v[key]; exists {
			return value, true
		}
	case []interface{}:
		// Intentar convertir la clave a índice
		var index int
		if _, err := fmt.Sscanf(key, "%d", &index); err == nil && index >= 0 && index < len(v) {
			return v[index], true
		}
	}
	return nil, false
}

// splitCombinedKey divide una clave combinada en claves individuales
func (oe *OptimizedEngine) splitCombinedKey(combinedKey string) []string {
	// Implementación simple: dividir por punto
	var keys []string
	var current string

	for _, ch := range combinedKey {
		if ch == '.' {
			if current != "" {
				keys = append(keys, current)
				current = ""
			}
		} else {
			current += string(ch)
		}
	}

	if current != "" {
		keys = append(keys, current)
	}

	return keys
}

// generateQueryKey genera una clave única para la consulta
func (oe *OptimizedEngine) generateQueryKey(keys []string, library string) string {
	key := library + ":"
	for _, k := range keys {
		key += k + "."
	}
	return key
}

// getFromPool obtiene un plan del pool
func (oe *OptimizedEngine) getFromPool(key string) *QueryPlan {
	oe.pool.mux.RLock()
	defer oe.pool.mux.RUnlock()

	if plan, exists := oe.pool.queries[key]; exists {
		plan.UsedCount++
		return plan
	}
	return nil
}

// saveToPool guarda un plan en el pool
func (oe *OptimizedEngine) saveToPool(key string, plan *QueryPlan) {
	oe.pool.mux.Lock()
	defer oe.pool.mux.Unlock()

	// Limpiar planes antiguos (más de 1 hora)
	now := time.Now()
	for k, p := range oe.pool.queries {
		if now.Sub(p.CreatedAt) > time.Hour {
			delete(oe.pool.queries, k)
		}
	}

	oe.pool.queries[key] = plan
}

// CompareOptimizedPerformance compara rendimiento con optimizaciones
func (oe *OptimizedEngine) CompareOptimizedPerformance(jsonStr string, keys []string) map[string]QueryResult {
	results := make(map[string]QueryResult)

	// Ejecutar con optimizaciones para cada librería
	libraries := []string{"standard", "json-iterator", "fastjson"}

	for _, library := range libraries {
		results[library+"_optimized"] = oe.QueryWithOptimization(jsonStr, keys, library)
	}

	// Comparar con versiones no optimizadas
	for _, library := range libraries {
		var result QueryResult
		switch library {
		case "standard":
			result = oe.QueryWithStandardLibrary(jsonStr, keys)
		case "json-iterator":
			result = oe.QueryWithJsonIterator(jsonStr, keys)
		case "fastjson":
			result = oe.QueryWithFastJSON(jsonStr, keys)
		}
		results[library+"_original"] = result
	}

	return results
}

// GetOptimizationStats retorna las estadísticas de optimización
func (oe *OptimizedEngine) GetOptimizationStats() *OptimizedEngineStats {
	oe.statsMux.RLock()
	defer oe.statsMux.RUnlock()

	// Crear una copia para evitar race conditions
	stats := &OptimizedEngineStats{
		TotalQueries:          oe.stats.TotalQueries,
		OptimizedQueries:      oe.stats.OptimizedQueries,
		CacheHits:             oe.stats.CacheHits,
		TotalOptimizationTime: oe.stats.TotalOptimizationTime,
	}

	// Calcular tiempo promedio
	if stats.TotalQueries > 0 {
		stats.AverageOptimizationTime = stats.TotalOptimizationTime / time.Duration(stats.TotalQueries)
	}

	return stats
}

// GetOptimizerStats retorna las estadísticas del optimizador
func (oe *OptimizedEngine) GetOptimizerStats() *optimizer.OptimizationStats {
	return oe.optimizer.GetStats()
}

// ClearOptimizationCache limpia el cache de optimización
func (oe *OptimizedEngine) ClearOptimizationCache() {
	oe.optimizer.ClearCache()

	oe.pool.mux.Lock()
	defer oe.pool.mux.Unlock()

	for k := range oe.pool.queries {
		delete(oe.pool.queries, k)
	}
}
