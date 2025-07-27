import React, { useState, useEffect } from 'react';
import './OptimizationPanel.css';

const OptimizationPanel = () => {
  const [optimizationStats, setOptimizationStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchOptimizationStats = async () => {
    try {
      const response = await fetch('http://localhost:8080/optimization/stats');
      if (!response.ok) {
        throw new Error('Error al obtener estadísticas de optimización');
      }
      
      const data = await response.json();
      if (data.success) {
        setOptimizationStats(data.data);
        setError(null);
        setIsLoading(false);
      } else {
        setError(data.error || 'Error al obtener estadísticas');
        setIsLoading(false);
      }
    } catch (err) {
      setError(err.message);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // Cargar estadísticas iniciales
    fetchOptimizationStats();
    
    // Actualizar estadísticas cada 5 segundos (menos frecuente)
    const interval = setInterval(fetchOptimizationStats, 5000);
    return () => clearInterval(interval);
  }, []);

  const formatDuration = (duration) => {
    if (!duration) return '0ms';
    
    const ms = duration / 1000000; // Convertir de nanosegundos a milisegundos
    if (ms < 1) return `${(ms * 1000).toFixed(2)}μs`;
    if (ms < 1000) return `${ms.toFixed(2)}ms`;
    return `${(ms / 1000).toFixed(2)}s`;
  };

  const formatNumber = (num) => {
    return new Intl.NumberFormat('es-ES').format(num);
  };

  if (isLoading && !optimizationStats) {
    return (
      <div className="optimization-panel">
        <h3>🚀 Optimizaciones de Código Intermedio</h3>
        <div className="loading">Cargando estadísticas...</div>
      </div>
    );
  }

  if (error && !optimizationStats) {
    return (
      <div className="optimization-panel">
        <h3>🚀 Optimizaciones de Código Intermedio</h3>
        <div className="error">Error: {error}</div>
        <button onClick={fetchOptimizationStats} className="retry-btn">
          Reintentar
        </button>
      </div>
    );
  }

  return (
    <div className="optimization-panel">
      <h3>🚀 Optimizaciones de Código Intermedio</h3>
      
      {optimizationStats && (
        <div className="stats-container">
          <div className="stats-section">
            <h4>📊 Estadísticas del Motor Optimizado</h4>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-label">Consultas Totales:</span>
                <span className="stat-value">{formatNumber(optimizationStats.optimization_stats?.TotalQueries || 0)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Consultas Optimizadas:</span>
                <span className="stat-value">{formatNumber(optimizationStats.optimization_stats?.OptimizedQueries || 0)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Cache Hits:</span>
                <span className="stat-value">{formatNumber(optimizationStats.optimization_stats?.CacheHits || 0)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Tiempo Promedio de Optimización:</span>
                <span className="stat-value">{formatDuration(optimizationStats.optimization_stats?.AverageOptimizationTime)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Tiempo Total de Optimización:</span>
                <span className="stat-value">{formatDuration(optimizationStats.optimization_stats?.TotalOptimizationTime)}</span>
              </div>
            </div>
          </div>

          <div className="stats-section">
            <h4>⚡ Estadísticas del Optimizador</h4>
            <div className="stats-grid">
              <div className="stat-item">
                <span className="stat-label">Consultas Procesadas:</span>
                <span className="stat-value">{formatNumber(optimizationStats.optimizer_stats?.TotalQueries || 0)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Hits de Cache:</span>
                <span className="stat-value">{formatNumber(optimizationStats.optimizer_stats?.CacheHits || 0)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Optimizaciones Aplicadas:</span>
                <span className="stat-value">{formatNumber(optimizationStats.optimizer_stats?.Optimizations || 0)}</span>
              </div>
              <div className="stat-item">
                <span className="stat-label">Tiempo Promedio:</span>
                <span className="stat-value">{formatDuration(optimizationStats.optimizer_stats?.AverageTime)}</span>
              </div>
            </div>
          </div>

          <div className="optimization-info">
            <h4>🔧 Tipos de Optimizaciones Implementadas</h4>
            <div className="optimization-list">
              <div className="optimization-item">
                <span className="optimization-icon">🎯</span>
                <span className="optimization-name">Eliminación de Pasos Redundantes</span>
                <span className="optimization-desc">Elimina consultas duplicadas y pasos innecesarios</span>
              </div>
              <div className="optimization-item">
                <span className="optimization-icon">🔗</span>
                <span className="optimization-name">Combinación de Pasos</span>
                <span className="optimization-desc">Combina múltiples navegaciones en una sola operación</span>
              </div>
              <div className="optimization-item">
                <span className="optimization-icon">📋</span>
                <span className="optimization-name">Reordenamiento de Pasos</span>
                <span className="optimization-desc">Reordena operaciones para mejor rendimiento</span>
              </div>
              <div className="optimization-item">
                <span className="optimization-icon">💾</span>
                <span className="optimization-name">Memoización</span>
                <span className="optimization-desc">Cache de resultados para consultas repetidas</span>
              </div>
              <div className="optimization-item">
                <span className="optimization-icon">🏗️</span>
                <span className="optimization-name">AST (Abstract Syntax Tree)</span>
                <span className="optimization-desc">Análisis de estructura para optimizaciones avanzadas</span>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="refresh-section">
        <button onClick={fetchOptimizationStats} className="refresh-btn">
          🔄 Actualizar Estadísticas
        </button>
      </div>
    </div>
  );
};

export default OptimizationPanel; 