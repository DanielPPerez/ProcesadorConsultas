package optimizer

import (
	"fmt"
	"sync"
	"time"
)

// NodeType representa el tipo de nodo en el AST
type NodeType int

const (
	NODE_ROOT NodeType = iota
	NODE_OBJECT
	NODE_ARRAY
	NODE_PROPERTY
	NODE_VALUE
)

// ASTNode representa un nodo en el árbol de sintaxis abstracta
type ASTNode struct {
	Type     NodeType
	Value    interface{}
	Children []*ASTNode
	Parent   *ASTNode
	Metadata map[string]interface{}
}

// QueryPlan representa un plan de consulta optimizado
type QueryPlan struct {
	Steps         []QueryStep
	EstimatedCost int64
	Optimizations []string
}

// QueryStep representa un paso en el plan de consulta
type QueryStep struct {
	Type          string
	Operation     string
	Target        string
	Conditions    []string
	EstimatedTime time.Duration
}

// Optimizer representa el optimizador de código intermedio
type Optimizer struct {
	cache    map[string]*QueryPlan
	cacheMux sync.RWMutex
	stats    *OptimizationStats
	config   *OptimizationConfig
}

// OptimizationStats contiene estadísticas de optimización
type OptimizationStats struct {
	TotalQueries  int64
	CacheHits     int64
	Optimizations int64
	AverageTime   time.Duration
	TotalTime     time.Duration
}

// OptimizationConfig contiene configuración del optimizador
type OptimizationConfig struct {
	EnableCache       bool
	EnableMemoization bool
	MaxCacheSize      int
	EnableParallel    bool
	OptimizationLevel int // 0=none, 1=basic, 2=aggressive
}

// NewOptimizer crea un nuevo optimizador
func NewOptimizer(config *OptimizationConfig) *Optimizer {
	if config == nil {
		config = &OptimizationConfig{
			EnableCache:       true,
			EnableMemoization: true,
			MaxCacheSize:      1000,
			EnableParallel:    true,
			OptimizationLevel: 2,
		}
	}

	return &Optimizer{
		cache:  make(map[string]*QueryPlan),
		stats:  &OptimizationStats{},
		config: config,
	}
}

// OptimizeQuery optimiza una consulta y retorna un plan optimizado
func (o *Optimizer) OptimizeQuery(query []string, jsonData interface{}) *QueryPlan {
	start := time.Now()

	// Generar clave de cache
	cacheKey := o.generateCacheKey(query)

	// Verificar cache
	if o.config.EnableCache {
		if cached := o.getFromCache(cacheKey); cached != nil {
			o.stats.CacheHits++
			return cached
		}
	}

	// Crear AST
	ast := o.buildAST(jsonData)

	// Aplicar optimizaciones
	plan := o.createQueryPlan(query, ast)

	// Aplicar optimizaciones según el nivel
	switch o.config.OptimizationLevel {
	case 1:
		o.applyBasicOptimizations(plan)
	case 2:
		o.applyAggressiveOptimizations(plan)
	}

	// Calcular costo estimado
	plan.EstimatedCost = o.calculateEstimatedCost(plan)

	// Guardar en cache
	if o.config.EnableCache {
		o.saveToCache(cacheKey, plan)
	}

	// Actualizar estadísticas
	o.stats.TotalQueries++
	o.stats.TotalTime += time.Since(start)
	o.stats.AverageTime = o.stats.TotalTime / time.Duration(o.stats.TotalQueries)

	return plan
}

// buildAST construye el árbol de sintaxis abstracta
func (o *Optimizer) buildAST(data interface{}) *ASTNode {
	root := &ASTNode{
		Type:     NODE_ROOT,
		Metadata: make(map[string]interface{}),
	}

	o.buildASTRecursive(data, root)
	return root
}

// buildASTRecursive construye el AST recursivamente
func (o *Optimizer) buildASTRecursive(data interface{}, parent *ASTNode) {
	switch v := data.(type) {
	case map[string]interface{}:
		node := &ASTNode{
			Type:     NODE_OBJECT,
			Parent:   parent,
			Metadata: make(map[string]interface{}),
		}
		parent.Children = append(parent.Children, node)

		for key, value := range v {
			propNode := &ASTNode{
				Type:     NODE_PROPERTY,
				Value:    key,
				Parent:   node,
				Metadata: make(map[string]interface{}),
			}
			node.Children = append(node.Children, propNode)
			o.buildASTRecursive(value, propNode)
		}

	case []interface{}:
		node := &ASTNode{
			Type:     NODE_ARRAY,
			Parent:   parent,
			Metadata: make(map[string]interface{}),
		}
		parent.Children = append(parent.Children, node)

		for idx, value := range v {
			indexNode := &ASTNode{
				Type:     NODE_PROPERTY,
				Value:    fmt.Sprintf("%d", idx),
				Parent:   node,
				Metadata: make(map[string]interface{}),
			}
			node.Children = append(node.Children, indexNode)
			o.buildASTRecursive(value, indexNode)
		}

	default:
		valueNode := &ASTNode{
			Type:   NODE_VALUE,
			Value:  v,
			Parent: parent,
		}
		parent.Children = append(parent.Children, valueNode)
	}
}

// createQueryPlan crea un plan de consulta básico
func (o *Optimizer) createQueryPlan(query []string, ast *ASTNode) *QueryPlan {
	plan := &QueryPlan{
		Steps: make([]QueryStep, 0, len(query)),
	}

	for _, key := range query {
		step := QueryStep{
			Type:          "navigation",
			Operation:     "access",
			Target:        key,
			EstimatedTime: time.Microsecond * 10,
		}

		// Optimización: si es un índice numérico, marcar como acceso directo
		if o.isNumericIndex(key) {
			step.Type = "direct_access"
			step.EstimatedTime = time.Microsecond * 5
		}

		plan.Steps = append(plan.Steps, step)
	}

	return plan
}

// applyBasicOptimizations aplica optimizaciones básicas
func (o *Optimizer) applyBasicOptimizations(plan *QueryPlan) {
	// Eliminar pasos redundantes
	plan.Steps = o.removeRedundantSteps(plan.Steps)

	// Combinar pasos consecutivos
	plan.Steps = o.combineConsecutiveSteps(plan.Steps)

	plan.Optimizations = append(plan.Optimizations, "redundant_elimination", "step_combination")
}

// applyAggressiveOptimizations aplica optimizaciones agresivas
func (o *Optimizer) applyAggressiveOptimizations(plan *QueryPlan) {
	// Aplicar optimizaciones básicas primero
	o.applyBasicOptimizations(plan)

	// Reordenar pasos para mejor rendimiento
	plan.Steps = o.reorderSteps(plan.Steps)

	// Aplicar memoización
	if o.config.EnableMemoization {
		plan.Steps = o.addMemoizationSteps(plan.Steps)
	}

	plan.Optimizations = append(plan.Optimizations, "step_reordering", "memoization")
}

// removeRedundantSteps elimina pasos redundantes
func (o *Optimizer) removeRedundantSteps(steps []QueryStep) []QueryStep {
	if len(steps) <= 1 {
		return steps
	}

	var optimized []QueryStep
	for i, step := range steps {
		// Evitar pasos consecutivos del mismo tipo
		if i > 0 && steps[i-1].Type == step.Type && steps[i-1].Target == step.Target {
			continue
		}
		optimized = append(optimized, step)
	}

	return optimized
}

// combineConsecutiveSteps combina pasos consecutivos
func (o *Optimizer) combineConsecutiveSteps(steps []QueryStep) []QueryStep {
	if len(steps) <= 1 {
		return steps
	}

	var combined []QueryStep
	for i := 0; i < len(steps); i++ {
		if i+1 < len(steps) && steps[i].Type == "navigation" && steps[i+1].Type == "navigation" {
			// Combinar dos pasos de navegación
			combinedStep := QueryStep{
				Type:          "combined_navigation",
				Operation:     "multi_access",
				Target:        steps[i].Target + "." + steps[i+1].Target,
				EstimatedTime: steps[i].EstimatedTime + steps[i+1].EstimatedTime,
			}
			combined = append(combined, combinedStep)
			i++ // Saltar el siguiente paso
		} else {
			combined = append(combined, steps[i])
		}
	}

	return combined
}

// reorderSteps reordena los pasos para mejor rendimiento
func (o *Optimizer) reorderSteps(steps []QueryStep) []QueryStep {
	// Mover accesos directos al principio
	var directAccess, others []QueryStep

	for _, step := range steps {
		if step.Type == "direct_access" {
			directAccess = append(directAccess, step)
		} else {
			others = append(others, step)
		}
	}

	// Combinar manteniendo el orden relativo
	return append(directAccess, others...)
}

// addMemoizationSteps agrega pasos de memoización
func (o *Optimizer) addMemoizationSteps(steps []QueryStep) []QueryStep {
	var memoized []QueryStep

	for i, step := range steps {
		// Agregar paso de memoización antes de operaciones costosas
		if step.EstimatedTime > time.Microsecond*50 {
			memoStep := QueryStep{
				Type:          "memoization",
				Operation:     "cache_check",
				Target:        fmt.Sprintf("memo_%d", i),
				EstimatedTime: time.Microsecond * 2,
			}
			memoized = append(memoized, memoStep)
		}
		memoized = append(memoized, step)
	}

	return memoized
}

// isNumericIndex verifica si una clave es un índice numérico
func (o *Optimizer) isNumericIndex(key string) bool {
	for _, ch := range key {
		if ch < '0' || ch > '9' {
			return false
		}
	}
	return len(key) > 0
}

// generateCacheKey genera una clave única para el cache
func (o *Optimizer) generateCacheKey(query []string) string {
	key := ""
	for _, q := range query {
		key += q + "."
	}
	return key
}

// getFromCache obtiene un plan del cache
func (o *Optimizer) getFromCache(key string) *QueryPlan {
	o.cacheMux.RLock()
	defer o.cacheMux.RUnlock()

	if plan, exists := o.cache[key]; exists {
		return plan
	}
	return nil
}

// saveToCache guarda un plan en el cache
func (o *Optimizer) saveToCache(key string, plan *QueryPlan) {
	o.cacheMux.Lock()
	defer o.cacheMux.Unlock()

	// Verificar límite de cache
	if len(o.cache) >= o.config.MaxCacheSize {
		// Eliminar entrada más antigua (implementación simple)
		for k := range o.cache {
			delete(o.cache, k)
			break
		}
	}

	o.cache[key] = plan
}

// calculateEstimatedCost calcula el costo estimado del plan
func (o *Optimizer) calculateEstimatedCost(plan *QueryPlan) int64 {
	var cost int64
	for _, step := range plan.Steps {
		cost += int64(step.EstimatedTime.Microseconds())
	}
	return cost
}

// GetStats retorna las estadísticas de optimización
func (o *Optimizer) GetStats() *OptimizationStats {
	return o.stats
}

// ClearCache limpia el cache
func (o *Optimizer) ClearCache() {
	o.cacheMux.Lock()
	defer o.cacheMux.Unlock()

	for k := range o.cache {
		delete(o.cache, k)
	}
}
