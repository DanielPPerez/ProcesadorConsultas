# Procesador de Consultas Simples para JSON (Mini GraphQL/JQ)

Un procesador de consultas JSON optimizado que demuestra el impacto de librerías de alto rendimiento en Go.

## 🚀 Características

- **Frontend**: Interfaz web moderna en React con TypeScript
- **Backend**: API REST en Go con analizador léxico/sintáctico personalizado
- **Optimización**: Comparación de rendimiento entre librerías JSON
- **Consultas**: Sintaxis simple tipo `user.address.city`
- **Análisis**: Métricas detalladas de tiempo y memoria

## 📁 Estructura del Proyecto

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
├── docs/                   # Documentación
├── examples/               # Ejemplos de uso
├── scripts/                # Scripts de configuración
└── README.md
```

## 🛠️ Tecnologías

### Backend
- **Go 1.21+**: Lenguaje principal
- **Gin**: Framework web de alto rendimiento
- **json-iterator/go**: Librería JSON optimizada
- **valyala/fastjson**: Librería JSON de máximo rendimiento
- **Analizador léxico/sintáctico**: Implementación personalizada

### Frontend
- **React 18**: Framework de UI
- **TypeScript**: Type safety
- **Tailwind CSS**: Framework de estilos
- **Axios**: Cliente HTTP
- **Lucide React**: Iconos modernos

## ⚡ Instalación Rápida

### Opción 1: Script Automático (Recomendado)

**Linux/macOS:**
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

**Windows:**
```cmd
scripts\setup.bat
```

### Opción 2: Instalación Manual

#### Prerrequisitos
- Go 1.21 o superior
- Node.js 16 o superior
- npm o yarn

#### Backend
```bash
cd backend
go mod tidy
go run main.go
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## 🎯 Uso

### 1. Consulta Simple
1. Abre http://localhost:3000
2. Ve a la pestaña "Consulta Simple"
3. Ingresa un JSON en el textarea
4. Escribe una consulta (ej: `user.address.city`)
5. Haz clic en "Procesar Consulta"
6. Visualiza el resultado y métricas de rendimiento

### 2. Comparación de Rendimiento
1. Ve a la pestaña "Comparación de Rendimiento"
2. Usa el botón "Cargar JSON Grande" para probar con datos masivos
3. Ejecuta la consulta para ver diferencias entre librerías
4. Analiza las métricas de tiempo y memoria

### 3. Ejemplos Incluidos
El sistema incluye ejemplos predefinidos:
- **Simple**: Consulta básica de usuario
- **Complejo**: Estructura de tienda con productos
- **Anidado**: Datos profundamente anidados

## 📊 Librerías Comparadas

| Librería | Ventajas | Desventajas |
|----------|----------|-------------|
| **Standard Library** | Compatibilidad total, API familiar | Rendimiento moderado |
| **json-iterator/go** | API compatible, mejor rendimiento | Dependencia externa |
| **valyala/fastjson** | Máximo rendimiento, menor memoria | API específica |

## 🔧 API Endpoints

- `GET /health` - Verificación de estado
- `POST /query` - Consulta simple
- `POST /query/compare` - Comparación de rendimiento

### Ejemplo de Uso de la API
```bash
curl -X POST http://localhost:8080/query \
  -H "Content-Type: application/json" \
  -d '{
    "json": "{\"user\": {\"name\": \"Juan\", \"age\": 30}}",
    "query": "user.name"
  }'
```

## 📈 Métricas de Rendimiento

El sistema mide:
- **Tiempo de Parse**: Duración del parseo JSON
- **Tiempo de Consulta**: Duración de la navegación
- **Tiempo Total**: Tiempo completo de la operación
- **Uso de Memoria**: Consumo de memoria por librería

## 🎓 Conceptos Demostrados

### Analizador Léxico
- Tokenización de consultas
- Identificación de identificadores y operadores
- Manejo de espacios en blanco

### Analizador Sintáctico
- Validación de estructura de consultas
- Generación de lista de claves
- Manejo de errores sintácticos

### Motor de Consultas
- Navegación por estructuras JSON
- Medición de rendimiento
- Comparación entre librerías

## 🚀 Ejecución

### Inicio Automático
```bash
# Linux/macOS
./run.sh

# Windows
run.bat
```

### Inicio Manual
```bash
# Terminal 1 - Backend
cd backend && go run main.go

# Terminal 2 - Frontend
cd frontend && npm start
```

## 📚 Documentación

- [Arquitectura del Sistema](docs/ARQUITECTURA.md)
- [Ejemplos de Uso](examples/ejemplos.json)
- [API Reference](docs/API.md)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- [Gin Framework](https://github.com/gin-gonic/gin)
- [json-iterator/go](https://github.com/json-iterator/go)
- [valyala/fastjson](https://github.com/valyala/fastjson)
- [React](https://reactjs.org/)
- [Tailwind CSS](https://tailwindcss.com/) 