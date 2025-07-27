import React, { useState } from 'react';
import { Play, Zap, BarChart3, Code, Database, Settings } from 'lucide-react';
import QueryProcessor from './components/QueryProcessor.jsx';
import PerformanceComparison from './components/PerformanceComparison.jsx';
import OptimizationPanel from './components/OptimizationPanel.jsx';

// Función para formatear duraciones de tiempo
function formatDuration(duration) {
  if (typeof duration === 'string') {
    return duration;
  }
  
  // Si es un número (nanosegundos), convertir a formato legible
  if (typeof duration === 'number') {
    if (duration < 1000) {
      return `${duration}ns`;
    } else if (duration < 1000000) {
      return `${(duration / 1000).toFixed(2)}μs`;
    } else {
      return `${(duration / 1000000).toFixed(2)}ms`;
    }
  }
  
  return duration;
}

function App() {
  const [activeTab, setActiveTab] = useState('query');
  const [queryResult, setQueryResult] = useState(null);
  const [comparisonResults, setComparisonResults] = useState(null);

  const handleQueryResult = (result) => {
    setQueryResult(result);
  };

  const handleComparisonResults = (results) => {
    setComparisonResults(results);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="flex items-center justify-center w-10 h-10 bg-blue-600 rounded-lg">
                <Database className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  Procesador de Consultas JSON
                </h1>
                <p className="text-sm text-gray-500">
                  Analizador léxico/sintáctico con comparación de rendimiento
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <Code className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('query')}
              className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'query'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Play className="w-4 h-4" />
              <span>Consulta Simple</span>
            </button>
            <button
              onClick={() => setActiveTab('compare')}
              className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'compare'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <BarChart3 className="w-4 h-4" />
              <span>Comparación de Rendimiento</span>
            </button>
            <button
              onClick={() => setActiveTab('optimization')}
              className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'optimization'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <Settings className="w-4 h-4" />
              <span>Optimizaciones</span>
            </button>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'query' ? (
          <QueryProcessor onResult={handleQueryResult} />
        ) : activeTab === 'compare' ? (
          <PerformanceComparison onResults={handleComparisonResults} />
        ) : (
          <OptimizationPanel />
        )}

        {/* Results Section */}
        {activeTab === 'query' && queryResult && (
          <div className="mt-8">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Zap className="w-5 h-5 mr-2 text-green-500" />
                Resultado de la Consulta
              </h3>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Valor Extraído</h4>
                  <div className="bg-gray-50 rounded-md p-4 json-viewer">
                    <pre className="text-sm text-gray-800">
                      {JSON.stringify(queryResult.value, null, 2)}
                    </pre>
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium text-gray-700 mb-2">Información de Rendimiento</h4>
                  <div className="bg-blue-50 rounded-md p-4">
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Librería:</span>
                        <span className="font-medium">{queryResult.performance.library_type}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Tiempo de Parse:</span>
                        <span className="font-medium">{formatDuration(queryResult.performance.parse_time)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Tiempo de Consulta:</span>
                        <span className="font-medium">{formatDuration(queryResult.performance.query_time)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Tiempo Total:</span>
                        <span className="font-medium">{formatDuration(queryResult.performance.total_time)}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Estadísticas de Optimización */}
              {queryResult.optimizationStats && (
                <div className="mt-6">
                  <h4 className="font-medium text-gray-700 mb-2">📊 Estadísticas de Optimización</h4>
                  <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-md p-4 border border-purple-200">
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div className="text-center">
                        <div className="font-semibold text-purple-700">{queryResult.optimizationStats.TotalQueries || 0}</div>
                        <div className="text-gray-600 text-xs">Consultas Totales</div>
                      </div>
                      <div className="text-center">
                        <div className="font-semibold text-purple-700">{queryResult.optimizationStats.OptimizedQueries || 0}</div>
                        <div className="text-gray-600 text-xs">Consultas Optimizadas</div>
                      </div>
                      <div className="text-center">
                        <div className="font-semibold text-purple-700">{queryResult.optimizationStats.CacheHits || 0}</div>
                        <div className="text-gray-600 text-xs">Cache Hits</div>
                      </div>
                      <div className="text-center">
                        <div className="font-semibold text-purple-700">{formatDuration(queryResult.optimizationStats.AverageOptimizationTime)}</div>
                        <div className="text-gray-600 text-xs">Tiempo Promedio</div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'compare' && comparisonResults && (
          <div className="mt-8">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <BarChart3 className="w-5 h-5 mr-2 text-purple-500" />
                Comparación de Rendimiento
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {Object.entries(comparisonResults).map(([library, result]) => (
                  <div key={library} className="performance-card bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg p-4 border border-gray-200">
                    <h4 className="font-semibold text-gray-900 mb-3 capitalize">{library}</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-600">Parse:</span>
                        <span className="font-medium">{formatDuration(result.performance.parse_time)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Consulta:</span>
                        <span className="font-medium">{formatDuration(result.performance.query_time)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Total:</span>
                        <span className="font-medium">{formatDuration(result.performance.total_time)}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600">Encontrado:</span>
                        <span className={`font-medium ${result.found ? 'text-green-600' : 'text-red-600'}`}>
                          {result.found ? 'Sí' : 'No'}
                        </span>
                      </div>
                      {result.value !== undefined && result.found && (
                        <div className="mt-2 p-2 bg-blue-50 rounded text-xs">
                          <span className="text-gray-600">Valor: </span>
                          <span className="font-mono">{JSON.stringify(result.value)}</span>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500 text-sm">
            <p>
              Procesador de Consultas JSON - Demostración de optimización de librerías
            </p>
            <p className="mt-2">
              Analizador léxico/sintáctico personalizado en Go con comparación de rendimiento
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App; 