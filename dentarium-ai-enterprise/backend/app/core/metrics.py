# -*- coding: utf-8 -*-
"""
Métricas Prometheus para monitoramento.
Autor: Roberto Ribeiro
"""

from prometheus_client import Counter, Histogram, Gauge
from fastapi import Request

# Métricas de requisições HTTP
http_requests_total = Counter(
    "http_requests_total",
    "Total de requisições HTTP",
    ["method", "endpoint", "status_code"],
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "Duração das requisições HTTP em segundos",
    ["method", "endpoint"],
    buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0],
)

# Métricas de upload de arquivos
file_uploads_total = Counter(
    "file_uploads_total",
    "Total de arquivos enviados",
    ["file_type", "status"],
)

file_size_bytes = Histogram(
    "file_size_bytes",
    "Tamanho dos arquivos enviados em bytes",
    ["file_type"],
    buckets=[1024, 10240, 102400, 1048576, 10485760, 104857600],
)

# Métricas de processamento AI
ai_requests_total = Counter(
    "ai_requests_total",
    "Total de requisições para serviços de IA",
    ["service", "status"],
)

ai_processing_duration_seconds = Histogram(
    "ai_processing_duration_seconds",
    "Duração do processamento de IA em segundos",
    ["service"],
    buckets=[1.0, 5.0, 10.0, 30.0, 60.0, 120.0],
)

# Métricas de usuários
active_users = Gauge(
    "active_users",
    "Número de usuários ativos no momento",
)

# Métricas de banco de dados
db_connections_active = Gauge(
    "db_connections_active",
    "Número de conexões ativas no banco de dados",
)

db_query_duration_seconds = Histogram(
    "db_query_duration_seconds",
    "Duração das queries no banco de dados",
    ["operation"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.5],
)

# Métricas de cache
cache_hits_total = Counter(
    "cache_hits_total",
    "Total de hits no cache Redis",
)

cache_misses_total = Counter(
    "cache_misses_total",
    "Total de misses no cache Redis",
)


def setup_metrics(app):
    """Configura middleware de métricas para a aplicação."""
    
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        """Middleware para coletar métricas de requisições."""
        import time
        
        # Ignorar métricas do próprio endpoint de métricas
        if request.url.path == "/metrics":
            return await call_next(request)
        
        # Marcar início
        start_time = time.time()
        
        # Processar requisição
        response = await call_next(request)
        
        # Calcular duração
        duration = time.time() - start_time
        
        # Registrar métricas
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code,
        ).inc()
        
        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=request.url.path,
        ).observe(duration)
        
        return response