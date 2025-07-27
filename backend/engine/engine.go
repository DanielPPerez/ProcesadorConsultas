package engine

import (
	"encoding/json"
	"fmt"
	"time"

	jsoniter "github.com/json-iterator/go"
	"github.com/valyala/fastjson"
)

// QueryResult representa el resultado de una consulta
type QueryResult struct {
	Value       interface{} `json:"value"`
	Found       bool        `json:"found"`
	Path        []string    `json:"path"`
	Keys        []string    `json:"keys"`
	Error       string      `json:"error,omitempty"`
	Performance Performance `json:"performance"`
}

// Performance contiene métricas de rendimiento
type Performance struct {
	ParseTime   time.Duration `json:"parse_time"`
	QueryTime   time.Duration `json:"query_time"`
	TotalTime   time.Duration `json:"total_time"`
	MemoryUsage int64         `json:"memory_usage"`
	LibraryType string        `json:"library_type"`
}

// Engine representa el motor de consultas
type Engine struct {
	jsonData interface{}
	keys     []string
}

// NewEngine crea un nuevo motor de consultas
func NewEngine() *Engine {
	return &Engine{}
}

// EnsureMinimumTimes asegura que haya tiempos mínimos para mostrar diferencias
func (e *Engine) EnsureMinimumTimes(result *QueryResult) {
	if result.Performance.ParseTime == 0 {
		result.Performance.ParseTime = time.Nanosecond
	}
	if result.Performance.QueryTime == 0 {
		result.Performance.QueryTime = time.Nanosecond
	}
	if result.Performance.TotalTime == 0 {
		result.Performance.TotalTime = time.Nanosecond
	}
}

// QueryWithStandardLibrary ejecuta una consulta usando la librería estándar
func (e *Engine) QueryWithStandardLibrary(jsonStr string, keys []string) QueryResult {
	start := time.Now()

	var result QueryResult
	result.Performance.LibraryType = "standard"
	result.Keys = keys

	// Validar entrada
	if jsonStr == "" {
		result.Error = "JSON de entrada está vacío"
		result.Performance.TotalTime = time.Since(start)
		return result
	}

	if len(keys) == 0 {
		result.Error = "No hay claves para consultar"
		result.Performance.TotalTime = time.Since(start)
		return result
	}

	// Parsear JSON con librería estándar
	parseStart := time.Now()
	var data interface{}
	if err := json.Unmarshal([]byte(jsonStr), &data); err != nil {
		result.Error = fmt.Sprintf("error parseando JSON: %v", err)
		result.Performance.TotalTime = time.Since(start)
		return result
	}
	result.Performance.ParseTime = time.Since(parseStart)

	// Ejecutar consulta
	queryStart := time.Now()
	value, found := e.navigateJSON(data, keys)
	result.Performance.QueryTime = time.Since(queryStart)

	result.Value = value
	result.Found = found
	result.Performance.TotalTime = time.Since(start)

	// Si no se encontró el valor, agregar información de debug
	if !found {
		result.Error = fmt.Sprintf("no se encontró el valor para la ruta: %v", keys)
	}

	return result
}

// QueryWithJsonIterator ejecuta una consulta usando json-iterator
func (e *Engine) QueryWithJsonIterator(jsonStr string, keys []string) QueryResult {
	start := time.Now()

	var result QueryResult
	result.Performance.LibraryType = "json-iterator"
	result.Keys = keys

	// Validar entrada
	if jsonStr == "" {
		result.Error = "JSON de entrada está vacío"
		result.Performance.TotalTime = time.Since(start)
		return result
	}

	if len(keys) == 0 {
		result.Error = "No hay claves para consultar"
		result.Performance.TotalTime = time.Since(start)
		return result
	}

	// Parsear JSON con json-iterator
	parseStart := time.Now()
	var data interface{}
	if err := jsoniter.Unmarshal([]byte(jsonStr), &data); err != nil {
		result.Error = fmt.Sprintf("error parseando JSON: %v", err)
		result.Performance.TotalTime = time.Since(start)
		return result
	}
	result.Performance.ParseTime = time.Since(parseStart)

	// Ejecutar consulta
	queryStart := time.Now()
	value, found := e.navigateJSON(data, keys)
	result.Performance.QueryTime = time.Since(queryStart)

	result.Value = value
	result.Found = found
	result.Performance.TotalTime = time.Since(start)

	// Si no se encontró el valor, agregar información de debug
	if !found {
		result.Error = fmt.Sprintf("no se encontró el valor para la ruta: %v", keys)
	}

	return result
}

// QueryWithFastJSON ejecuta una consulta usando fastjson
func (e *Engine) QueryWithFastJSON(jsonStr string, keys []string) QueryResult {
	start := time.Now()

	var result QueryResult
	result.Performance.LibraryType = "fastjson"
	result.Keys = keys

	// Validar entrada
	if jsonStr == "" {
		result.Error = "JSON de entrada está vacío"
		result.Performance.TotalTime = time.Since(start)
		return result
	}

	if len(keys) == 0 {
		result.Error = "No hay claves para consultar"
		result.Performance.TotalTime = time.Since(start)
		return result
	}

	// Parsear JSON con fastjson
	parseStart := time.Now()
	var p fastjson.Parser
	v, err := p.Parse(jsonStr)
	if err != nil {
		result.Error = fmt.Sprintf("error parseando JSON: %v", err)
		result.Performance.TotalTime = time.Since(start)
		return result
	}
	result.Performance.ParseTime = time.Since(parseStart)

	// Ejecutar consulta
	queryStart := time.Now()
	value, found := e.navigateFastJSON(v, keys)
	result.Performance.QueryTime = time.Since(queryStart)

	result.Value = value
	result.Found = found
	result.Performance.TotalTime = time.Since(start)

	// Si no se encontró el valor, agregar información de debug
	if !found {
		result.Error = fmt.Sprintf("no se encontró el valor para la ruta: %v", keys)
	}

	return result
}

// navigateJSON navega por la estructura JSON usando la librería estándar
func (e *Engine) navigateJSON(data interface{}, keys []string) (interface{}, bool) {
	current := data

	for _, key := range keys {
		switch v := current.(type) {
		case map[string]interface{}:
			if value, exists := v[key]; exists {
				current = value
			} else {
				return nil, false
			}
		case map[interface{}]interface{}:
			if value, exists := v[key]; exists {
				current = value
			} else {
				return nil, false
			}
		case []interface{}:
			// Intentar convertir la clave a índice
			var index int
			if _, err := fmt.Sscanf(key, "%d", &index); err == nil && index >= 0 && index < len(v) {
				current = v[index]
			} else {
				return nil, false
			}
		default:
			return nil, false
		}
	}

	return current, true
}

// navigateFastJSON navega por la estructura JSON usando fastjson
func (e *Engine) navigateFastJSON(v *fastjson.Value, keys []string) (interface{}, bool) {
	current := v

	for _, key := range keys {
		// Intentar obtener como objeto primero
		obj := current.GetObject()
		if obj != nil {
			value := obj.Get(key)
			if value != nil {
				current = value
				continue
			}
		}

		// Si no es un objeto, intentar como array
		arr := current.GetArray()
		if arr != nil {
			// Intentar convertir la clave a índice
			var index int
			if _, err := fmt.Sscanf(key, "%d", &index); err == nil && index >= 0 && index < len(arr) {
				current = arr[index]
				continue
			}
		}

		// Si no se puede navegar, retornar error con información de debug
		return nil, false
	}

	// Convertir fastjson.Value a interface{}
	return e.fastJSONToInterface(current), true
}

// fastJSONToInterface convierte un fastjson.Value a interface{}
func (e *Engine) fastJSONToInterface(v *fastjson.Value) interface{} {
	switch v.Type() {
	case fastjson.TypeNull:
		return nil
	case fastjson.TypeTrue:
		return true
	case fastjson.TypeFalse:
		return false
	case fastjson.TypeNumber:
		if f, err := v.Float64(); err == nil {
			return f
		}
		if i, err := v.Int(); err == nil {
			return i
		}
		return v.String()
	case fastjson.TypeString:
		return string(v.GetStringBytes())
	case fastjson.TypeObject:
		obj := v.GetObject()
		result := make(map[string]interface{})
		obj.Visit(func(key []byte, value *fastjson.Value) {
			result[string(key)] = e.fastJSONToInterface(value)
		})
		return result
	case fastjson.TypeArray:
		arr := v.GetArray()
		result := make([]interface{}, len(arr))
		for i, item := range arr {
			result[i] = e.fastJSONToInterface(item)
		}
		return result
	default:
		return v.String()
	}
}

// ComparePerformance compara el rendimiento de diferentes librerías
func (e *Engine) ComparePerformance(jsonStr string, keys []string) map[string]QueryResult {
	results := make(map[string]QueryResult)

	// Validar entrada
	if jsonStr == "" {
		errorResult := QueryResult{
			Error: "JSON de entrada está vacío",
			Keys:  keys,
		}
		results["standard"] = errorResult
		results["json-iterator"] = errorResult
		results["fastjson"] = errorResult
		return results
	}

	if len(keys) == 0 {
		errorResult := QueryResult{
			Error: "No hay claves para consultar",
			Keys:  keys,
		}
		results["standard"] = errorResult
		results["json-iterator"] = errorResult
		results["fastjson"] = errorResult
		return results
	}

	// Ejecutar con librería estándar
	results["standard"] = e.QueryWithStandardLibrary(jsonStr, keys)

	// Ejecutar con json-iterator
	results["json-iterator"] = e.QueryWithJsonIterator(jsonStr, keys)

	// Ejecutar con fastjson
	results["fastjson"] = e.QueryWithFastJSON(jsonStr, keys)

	// Asegurar tiempos mínimos para todos los resultados
	for key, result := range results {
		e.EnsureMinimumTimes(&result)
		results[key] = result
	}

	return results
}
