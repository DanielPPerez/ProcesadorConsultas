import React, { useState } from 'react';
import { Send, FileText, Search, Database } from 'lucide-react';
import axios from 'axios';

const QueryProcessor = ({ onResult }) => {
  const [selectedLibrary, setSelectedLibrary] = useState('standard');
  const [jsonInput, setJsonInput] = useState(`{
  "user": {
    "name": "Juan Pérez",
    "age": 30,
    "address": {
      "street": "Calle Principal 123",
      "city": "Madrid",
      "country": "España"
    },
    "hobbies": ["programación", "música", "deportes"]
  },
  "company": {
    "name": "TechCorp",
    "employees": 150,
    "location": {
      "city": "Barcelona",
      "country": "España"
    }
  }
}`);
  const [query, setQuery] = useState('user.address.city');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`http://localhost:8080/query?library=${selectedLibrary}`, {
        json: jsonInput,
        query: query
      });

      if (response.data.success) {
        // Incluir estadísticas de optimización en el resultado
        const resultWithStats = {
          ...response.data.data,
          optimizationStats: response.data.optimization_stats
        };
        onResult(resultWithStats);
      } else {
        setError(response.data.error || 'Error desconocido');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error de conexión');
    } finally {
      setLoading(false);
    }
  };

  const loadExample = (example) => {
    switch (example) {
      case 'simple':
        setJsonInput(`{
  "user": {
    "name": "María García",
    "email": "maria@example.com",
    "profile": {
      "avatar": "https://example.com/avatar.jpg",
      "bio": "Desarrolladora Full Stack"
    }
  }
}`);
        setQuery('user.profile.bio');
        break;
      case 'complex':
        setJsonInput(`{
  "store": {
    "name": "SuperMarket",
    "products": [
      {
        "id": 1,
        "name": "Laptop",
        "price": 999.99,
        "category": "electronics"
      },
      {
        "id": 2,
        "name": "Mouse",
        "price": 29.99,
        "category": "electronics"
      }
    ],
    "employees": {
      "manager": {
        "name": "Carlos López",
        "department": "sales"
      }
    }
  }
}`);
        setQuery('store.employees.manager.name');
        break;
      case 'nested':
        setJsonInput(`{
  "data": {
    "users": [
      {
        "id": 1,
        "personal": {
          "name": "Ana",
          "contact": {
            "phone": "+34 123 456 789",
            "address": {
              "street": "Gran Vía 1",
              "postal": "28013"
            }
          }
        }
      }
    ],
    "metadata": {
      "version": "1.0",
      "timestamp": "2024-01-01T00:00:00Z"
    }
  }
}`);
        setQuery('data.users.0.personal.contact.address.street');
        break;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center mb-6">
        <div className="flex items-center justify-center w-10 h-10 bg-blue-100 rounded-lg mr-3">
          <FileText className="w-5 h-5 text-blue-600" />
        </div>
        <div>
          <h2 className="text-xl font-semibold text-gray-900">
            Procesador de Consultas
          </h2>
          <p className="text-sm text-gray-500">
            Ingresa JSON y una consulta para extraer datos específicos
          </p>
        </div>
      </div>

      {/* Información sobre librerías */}
      <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-green-50 rounded-lg border border-blue-200">
        <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
          <Database className="w-4 h-4 mr-2 text-blue-600" />
          Librerías Disponibles
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
          <div className="bg-white p-3 rounded border">
            <h4 className="font-medium text-gray-900 mb-1">Standard Library</h4>
            <p className="text-gray-600 text-xs">Librería estándar de Go, flexible pero más lenta</p>
          </div>
          <div className="bg-white p-3 rounded border">
            <h4 className="font-medium text-gray-900 mb-1">json-iterator/go</h4>
            <p className="text-gray-600 text-xs">Librería optimizada, compatible con la API estándar</p>
          </div>
          <div className="bg-white p-3 rounded border">
            <h4 className="font-medium text-gray-900 mb-1">valyala/fastjson</h4>
            <p className="text-gray-600 text-xs">Librería de máximo rendimiento, API específica</p>
          </div>
        </div>
      </div>

      {/* Ejemplos */}
      <div className="mb-6">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Ejemplos de consulta:</h3>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => loadExample('simple')}
            className="px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200 transition-colors"
          >
            Simple
          </button>
          <button
            onClick={() => loadExample('complex')}
            className="px-3 py-1 text-xs bg-green-100 text-green-700 rounded-full hover:bg-green-200 transition-colors"
          >
            Complejo
          </button>
          <button
            onClick={() => loadExample('nested')}
            className="px-3 py-1 text-xs bg-purple-100 text-purple-700 rounded-full hover:bg-purple-200 transition-colors"
          >
            Anidado
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* JSON Input */}
        <div>
          <label htmlFor="json-input" className="block text-sm font-medium text-gray-700 mb-2">
            JSON de Entrada
          </label>
          <textarea
            id="json-input"
            value={jsonInput}
            onChange={(e) => setJsonInput(e.target.value)}
            className="w-full h-64 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 json-viewer"
            placeholder="Ingresa tu JSON aquí..."
            required
          />
        </div>

        {/* Query Input */}
        <div>
          <label htmlFor="query-input" className="block text-sm font-medium text-gray-700 mb-2">
            Consulta
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-gray-400" />
            </div>
            <input
              id="query-input"
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="ej: user.address.city"
              required
            />
          </div>
          <p className="mt-1 text-xs text-gray-500">
            Usa notación de punto para navegar por el JSON (ej: propiedad.subpropiedad)
          </p>
        </div>

        {/* Library Selection */}
        <div>
          <label htmlFor="library-select" className="block text-sm font-medium text-gray-700 mb-2">
            Librería JSON
          </label>
          <select
            id="library-select"
            value={selectedLibrary}
            onChange={(e) => setSelectedLibrary(e.target.value)}
            className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="standard">Standard Library (Go)</option>
            <option value="json-iterator">json-iterator/go</option>
            <option value="fastjson">valyala/fastjson</option>
          </select>
          <p className="mt-1 text-xs text-gray-500">
            Selecciona la librería JSON que quieres usar para procesar la consulta
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Procesando...
              </>
            ) : (
              <>
                <Send className="w-4 h-4 mr-2" />
                Procesar Consulta
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default QueryProcessor; 