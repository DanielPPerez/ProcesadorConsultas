import React, { useState } from 'react';
import { BarChart3, Zap, TrendingUp, Clock } from 'lucide-react';
import axios from 'axios';

const PerformanceComparison = ({ onResults }) => {
  const [jsonInput, setJsonInput] = useState(`{
  "data": {
    "users": [
      {
        "id": 1,
        "name": "Usuario 1",
        "profile": {
          "email": "user1@example.com",
          "settings": {
            "theme": "dark",
            "notifications": true,
            "preferences": {
              "language": "es",
              "timezone": "Europe/Madrid"
            }
          }
        }
      },
      {
        "id": 2,
        "name": "Usuario 2",
        "profile": {
          "email": "user2@example.com",
          "settings": {
            "theme": "light",
            "notifications": false,
            "preferences": {
              "language": "en",
              "timezone": "America/New_York"
            }
          }
        }
      },
      {
        "id": 3,
        "name": "Usuario 3",
        "profile": {
          "email": "user3@example.com",
          "settings": {
            "theme": "dark",
            "notifications": true,
            "preferences": {
              "language": "fr",
              "timezone": "Europe/Paris"
            }
          }
        }
      }
    ],
    "metadata": {
      "version": "1.0.0",
      "timestamp": "2024-01-01T00:00:00Z",
      "config": {
        "features": ["auth", "api", "dashboard"],
        "limits": {
          "requests": 1000,
          "storage": "1GB"
        }
      }
    }
  }
}`);
  const [query, setQuery] = useState('data.users.1.profile.settings.preferences.language');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:8080/query/compare', {
        json: jsonInput,
        query: query
      });

      if (response.data.success) {
        onResults(response.data.results);
      } else {
        setError(response.data.error || 'Error desconocido');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error de conexión');
    } finally {
      setLoading(false);
    }
  };

  const loadLargeExample = () => {
    // Generar un JSON grande para demostrar las diferencias de rendimiento
    const largeData = {
      data: {
        users: Array.from({ length: 1000 }, (_, i) => ({
          id: i + 1,
          name: `Usuario ${i + 1}`,
          email: `user${i + 1}@example.com`,
          profile: {
            avatar: `https://example.com/avatar${i + 1}.jpg`,
            bio: `Biografía del usuario ${i + 1}`,
            settings: {
              theme: i % 2 === 0 ? 'dark' : 'light',
              notifications: i % 3 === 0,
              preferences: {
                language: ['es', 'en', 'fr'][i % 3],
                timezone: ['Europe/Madrid', 'America/New_York', 'Asia/Tokyo'][i % 3],
                currency: ['EUR', 'USD', 'JPY'][i % 3]
              }
            }
          },
          posts: Array.from({ length: 10 }, (_, j) => ({
            id: j + 1,
            title: `Post ${j + 1} del usuario ${i + 1}`,
            content: `Contenido del post ${j + 1} del usuario ${i + 1}`,
            tags: ['tag1', 'tag2', 'tag3'],
            metadata: {
              created: new Date().toISOString(),
              views: Math.floor(Math.random() * 1000),
              likes: Math.floor(Math.random() * 100)
            }
          }))
        })),
        metadata: {
          version: "1.0.0",
          timestamp: new Date().toISOString(),
          totalUsers: 1000,
          config: {
            features: ["auth", "api", "dashboard", "analytics", "notifications"],
            limits: {
              requests: 10000,
              storage: "10GB",
              bandwidth: "100GB"
            }
          }
        }
      }
    };

    setJsonInput(JSON.stringify(largeData, null, 2));
    setQuery('data.users.999.profile.settings.preferences.language');
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center mb-6">
        <div className="flex items-center justify-center w-10 h-10 bg-purple-100 rounded-lg mr-3">
          <BarChart3 className="w-5 h-5 text-purple-600" />
        </div>
        <div>
          <h2 className="text-xl font-semibold text-gray-900">
            Comparación de Rendimiento
          </h2>
          <p className="text-sm text-gray-500">
            Compara el rendimiento entre diferentes librerías JSON
          </p>
        </div>
      </div>

      {/* Información sobre las librerías */}
      <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
        <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center">
          <TrendingUp className="w-4 h-4 mr-2 text-blue-600" />
          Librerías Comparadas
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

      {/* Ejemplos de consultas */}
      <div className="mb-6">
        <h3 className="text-sm font-medium text-gray-700 mb-3">Ejemplos de consultas:</h3>
        <div className="flex flex-wrap gap-2 mb-4">
          <button
            onClick={() => setQuery('data.users.0.profile.settings.preferences.language')}
            className="px-3 py-1 text-xs bg-blue-100 text-blue-700 rounded-full hover:bg-blue-200 transition-colors"
          >
            Usuario 1 - Idioma
          </button>
          <button
            onClick={() => setQuery('data.users.1.profile.settings.preferences.language')}
            className="px-3 py-1 text-xs bg-green-100 text-green-700 rounded-full hover:bg-green-200 transition-colors"
          >
            Usuario 2 - Idioma
          </button>
          <button
            onClick={() => setQuery('data.users.2.profile.settings.preferences.language')}
            className="px-3 py-1 text-xs bg-purple-100 text-purple-700 rounded-full hover:bg-purple-200 transition-colors"
          >
            Usuario 3 - Idioma
          </button>
          <button
            onClick={() => setQuery('data.metadata.config.features')}
            className="px-3 py-1 text-xs bg-orange-100 text-orange-700 rounded-full hover:bg-orange-200 transition-colors"
          >
            Features
          </button>
        </div>
        
        <button
          onClick={loadLargeExample}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors"
        >
          <Zap className="w-4 h-4 mr-2" />
          Cargar JSON Grande (1000 usuarios)
        </button>
        <p className="mt-2 text-xs text-gray-500">
          Carga un JSON grande para ver mejor las diferencias de rendimiento entre librerías
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* JSON Input */}
        <div>
          <label htmlFor="json-input-compare" className="block text-sm font-medium text-gray-700 mb-2">
            JSON de Entrada
          </label>
          <textarea
            id="json-input-compare"
            value={jsonInput}
            onChange={(e) => setJsonInput(e.target.value)}
            className="w-full h-64 px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 json-viewer"
            placeholder="Ingresa tu JSON aquí..."
            required
          />
        </div>

        {/* Query Input */}
        <div>
          <label htmlFor="query-input-compare" className="block text-sm font-medium text-gray-700 mb-2">
            Consulta
          </label>
          <input
            id="query-input-compare"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
            placeholder="ej: data.users.0.profile.settings.preferences.language"
            required
          />
          <p className="mt-1 text-xs text-gray-500">
            La consulta se ejecutará con las tres librerías para comparar rendimiento
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
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Comparando...
              </>
            ) : (
              <>
                <Clock className="w-4 h-4 mr-2" />
                Comparar Rendimiento
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default PerformanceComparison; 