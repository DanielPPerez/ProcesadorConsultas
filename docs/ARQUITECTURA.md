# Arquitectura del Procesador de Consultas JSON

## Descripción General

Este proyecto implementa un procesador de consultas JSON con un analizador léxico/sintáctico personalizado en Go, diseñado para demostrar las diferencias de rendimiento entre diferentes librerías JSON.

## Estructura del Proyecto

```
ProcesadorConsultas/
├── backend/                 # Servidor Go
│   ├── lexer/              # Analizador léxico
│   ├── parser/             # Analizador sintáctico
│   ├── engine/             # Motor de consultas
│   ├── main.go             # Servidor principal
│   └── go.mod              # Dependencias Go
├── frontend/               # Aplicación React
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   ├── App.tsx         # Componente principal
│   │   └── index.tsx       # Punto de entrada
│   ├── public/             # Archivos estáticos
│   └── package.json        # Dependencias Node.js
└── docs/                   # Documentación
```

## Componentes Principales

### 1. Analizador Léxico (`backend/lexer/`)

**Responsabilidades:**
- Tokenización de la consulta de entrada
- Identificación de identificadores y operadores
- Manejo de espacios en blanco y caracteres especiales

**Tokens Soportados:**
- `TOKEN_IDENTIFIER`: Nombres de propiedades (ej: "user", "address")
- `TOKEN_DOT`: Operador de navegación (".")
- `TOKEN_EOF`: Fin de archivo
- `TOKEN_ERROR`: Errores léxicos

**Ejemplo:**
```
Consulta: "user.address.city"
Tokens: [IDENTIFIER("user"), DOT("."), IDENTIFIER("address"), DOT("."), IDENTIFIER("city"), EOF]
```

### 2. Analizador Sintáctico (`backend/parser/`)

**Responsabilidades:**
- Análisis sintáctico de la secuencia de tokens
- Validación de la estructura de la consulta
- Generación de la lista de claves para navegación

**Gramática:**
```
query ::= identifier ('.' identifier)*
identifier ::= letter (letter | digit | '_')*
```

**Ejemplo:**
```
Tokens: [IDENTIFIER("user"), DOT("."), IDENTIFIER("address"), DOT("."), IDENTIFIER("city")]
Claves: ["user", "address", "city"]
```

### 3. Motor de Consultas (`backend/engine/`)

**Responsabilidades:**
- Parseo de JSON con diferentes librerías
- Navegación por la estructura JSON
- Medición de rendimiento
- Comparación entre librerías

**Librerías Soportadas:**
1. **Standard Library** (`encoding/json`)
   - Librería estándar de Go
   - Máxima compatibilidad
   - Rendimiento moderado

2. **json-iterator/go**
   - API compatible con la estándar
   - Optimizaciones de rendimiento
   - Menor uso de memoria

3. **valyala/fastjson**
   - Máximo rendimiento
   - API específica
   - Uso mínimo de memoria

### 4. Servidor API (`backend/main.go`)

**Endpoints:**
- `GET /health`: Verificación de estado
- `POST /query`: Consulta simple con librería estándar
- `POST /query/compare`: Comparación de rendimiento

**Características:**
- Framework Gin para alta performance
- CORS configurado para frontend
- Manejo de errores robusto
- Logging estructurado

### 5. Frontend React (`frontend/`)

**Componentes Principales:**
- `App.tsx`: Componente raíz con navegación
- `QueryProcessor.tsx`: Interfaz para consultas simples
- `PerformanceComparison.tsx`: Comparación de rendimiento

**Características:**
- TypeScript para type safety
- Tailwind CSS para estilos
- Axios para comunicación HTTP
- Lucide React para iconos

## Flujo de Datos

### Consulta Simple
1. Usuario ingresa JSON y consulta en el frontend
2. Frontend envía POST a `/query`
3. Backend parsea la consulta con el analizador léxico/sintáctico
4. Se ejecuta la consulta con la librería estándar
5. Se retorna el resultado con métricas de rendimiento

### Comparación de Rendimiento
1. Usuario ingresa JSON y consulta en el frontend
2. Frontend envía POST a `/query/compare`
3. Backend parsea la consulta
4. Se ejecuta la consulta con las tres librerías
5. Se retornan los resultados comparativos

## Optimizaciones Implementadas

### 1. Analizador Léxico Optimizado
- Lectura de caracteres eficiente
- Minimización de asignaciones de memoria
- Manejo directo de buffers

### 2. Parser Predictivo
- Análisis LL(1) para máxima eficiencia
- Validación temprana de errores
- Generación directa de claves

### 3. Motor de Consultas
- Reutilización de estructuras de datos
- Medición precisa de tiempos
- Comparación justa entre librerías

### 4. Frontend Optimizado
- Lazy loading de componentes
- Debouncing de inputs
- Caching de resultados

## Métricas de Rendimiento

### Tiempos Medidos
- **Parse Time**: Tiempo para parsear el JSON
- **Query Time**: Tiempo para ejecutar la consulta
- **Total Time**: Tiempo total de la operación

### Memoria
- **Memory Usage**: Uso de memoria por librería
- **Allocations**: Número de asignaciones

## Casos de Uso

### 1. Consultas Simples
```
JSON: {"user": {"name": "Juan", "age": 30}}
Query: "user.name"
Result: "Juan"
```

### 2. Consultas Anidadas
```
JSON: {"data": {"users": [{"profile": {"email": "test@example.com"}}]}}
Query: "data.users.0.profile.email"
Result: "test@example.com"
```

### 3. Comparación de Rendimiento
- JSON grande (varios MB)
- Múltiples consultas
- Análisis de tendencias

## Extensiones Futuras

1. **Soporte para Arrays**: Consultas con índices numéricos
2. **Operadores de Filtrado**: Condiciones en consultas
3. **Caching**: Almacenamiento de resultados parseados
4. **Streaming**: Procesamiento de JSONs muy grandes
5. **Plugins**: Sistema de librerías extensible 