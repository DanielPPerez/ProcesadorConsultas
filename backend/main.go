package main

import (
	"fmt"
	"log"
	"net/http"
	"time"

	"procesador-consultas/engine"
	"procesador-consultas/parser"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

// QueryRequest representa la solicitud de consulta
type QueryRequest struct {
	JSON  string `json:"json" binding:"required"`
	Query string `json:"query" binding:"required"`
}

// QueryResponse representa la respuesta de consulta
type QueryResponse struct {
	Success bool                          `json:"success"`
	Data    map[string]interface{}        `json:"data,omitempty"`
	Error   string                        `json:"error,omitempty"`
	Results map[string]engine.QueryResult `json:"results,omitempty"`
}

func main() {
	// Configurar Gin
	gin.SetMode(gin.ReleaseMode)
	r := gin.Default()

	// Configurar CORS
	config := cors.DefaultConfig()
	config.AllowOrigins = []string{"http://localhost:3000", "http://127.0.0.1:3000"}
	config.AllowMethods = []string{"GET", "POST", "OPTIONS"}
	config.AllowHeaders = []string{"Origin", "Content-Type", "Accept"}
	r.Use(cors.New(config))

	// Rutas
	r.GET("/health", healthCheck)
	r.POST("/query", handleQuery)
	r.POST("/query/compare", handleQueryCompare)

	// Ruta principal - redirigir al frontend
	r.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "Procesador de Consultas JSON API",
			"endpoints": []string{
				"GET /health",
				"POST /query",
				"POST /query/compare",
			},
			"frontend": "http://localhost:3000",
		})
	})

	// Configurar servidor
	srv := &http.Server{
		Addr:         ":8080",
		Handler:      r,
		ReadTimeout:  15 * time.Second,
		WriteTimeout: 15 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	log.Println("🚀 Servidor iniciado en http://localhost:8080")
	log.Fatal(srv.ListenAndServe())
}

// healthCheck verifica el estado del servidor
func healthCheck(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status":  "ok",
		"message": "Procesador de Consultas JSON funcionando correctamente",
		"time":    time.Now().Format(time.RFC3339),
	})
}

// handleQuery maneja una consulta simple
func handleQuery(c *gin.Context) {
	var req QueryRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, QueryResponse{
			Success: false,
			Error:   "Datos de entrada inválidos: " + err.Error(),
		})
		return
	}

	// Parsear la consulta
	keys, err := parser.ParseQueryString(req.Query)
	if err != nil {
		c.JSON(http.StatusBadRequest, QueryResponse{
			Success: false,
			Error:   "Error parseando consulta: " + err.Error(),
		})
		return
	}

	// Ejecutar consulta con la librería especificada
	eng := engine.NewEngine()
	var result engine.QueryResult

	// Determinar qué librería usar (por defecto standard)
	library := c.Query("library")
	if library == "" {
		library = "standard"
	}

	switch library {
	case "json-iterator":
		result = eng.QueryWithJsonIterator(req.JSON, keys)
	case "fastjson":
		result = eng.QueryWithFastJSON(req.JSON, keys)
	default:
		result = eng.QueryWithStandardLibrary(req.JSON, keys)
	}

	// Asegurar tiempos mínimos
	eng.EnsureMinimumTimes(&result)

	if result.Error != "" {
		c.JSON(http.StatusBadRequest, QueryResponse{
			Success: false,
			Error:   result.Error,
		})
		return
	}

	c.JSON(http.StatusOK, QueryResponse{
		Success: true,
		Data: map[string]interface{}{
			"value":       result.Value,
			"found":       result.Found,
			"path":        keys,
			"performance": result.Performance,
		},
	})
}

// handleQueryCompare maneja una consulta con comparación de rendimiento
func handleQueryCompare(c *gin.Context) {
	var req QueryRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, QueryResponse{
			Success: false,
			Error:   "Datos de entrada inválidos: " + err.Error(),
		})
		return
	}

	// Validar que el JSON sea válido
	if req.JSON == "" {
		c.JSON(http.StatusBadRequest, QueryResponse{
			Success: false,
			Error:   "JSON de entrada no puede estar vacío",
		})
		return
	}

	// Validar que la consulta no esté vacía
	if req.Query == "" {
		c.JSON(http.StatusBadRequest, QueryResponse{
			Success: false,
			Error:   "Consulta no puede estar vacía",
		})
		return
	}

	// Parsear la consulta
	keys, err := parser.ParseQueryString(req.Query)
	if err != nil {
		c.JSON(http.StatusBadRequest, QueryResponse{
			Success: false,
			Error:   "Error parseando consulta: " + err.Error(),
		})
		return
	}

	// Ejecutar consulta con todas las librerías
	eng := engine.NewEngine()
	results := eng.ComparePerformance(req.JSON, keys)

	// Limpiar errores de "no encontrado" de los resultados
	for key, result := range results {
		if result.Error == fmt.Sprintf("no se encontró el valor para la ruta: %v", keys) {
			result.Error = ""
			results[key] = result
		}
	}

	// Verificar si hay errores críticos en los resultados
	hasErrors := false
	for _, result := range results {
		if result.Error != "" {
			hasErrors = true
			break
		}
	}

	if hasErrors {
		c.JSON(http.StatusBadRequest, QueryResponse{
			Success: false,
			Error:   "Error procesando JSON con una o más librerías",
			Results: results,
		})
		return
	}

	c.JSON(http.StatusOK, QueryResponse{
		Success: true,
		Results: results,
	})
}
