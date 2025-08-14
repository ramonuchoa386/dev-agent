from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
from functools import wraps

webhook_requests_total = Counter(
    'github_webhook_requests_total',
    'Total webhook requests received',
    ['action', 'repository']
)

workflow_duration_seconds = Histogram(
    'workflow_duration_seconds',
    'Time spent processing workflow',
    ['step', 'status']
)

active_workflows = Gauge(
    'active_workflows',
    'Number of active workflows'
)

pull_requests_created = Counter(
    'pull_requests_created_total',
    'Total pull requests created',
    ['repository']
)

errors_total = Counter(
    'errors_total',
    'Total errors by type',
    ['error_type', 'agent']
)

def track_workflow_metrics(step_name: str):
    """Decorator para rastrear métricas de workflow"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            active_workflows.inc()
            
            try:
                result = await func(*args, **kwargs)
                status = "success" if not getattr(result, "error", None) else "error"
                
                if getattr(result, "error", None):
                    errors_total.labels(
                        error_type=type(getattr(result, "error", None)).__name__,
                        agent=step_name
                    ).inc()
                
                return result
                
            except Exception as e:                
                errors_total.labels(
                    error_type=type(e).__name__,
                    agent=step_name
                ).inc()
                raise
            
            finally:
                duration = time.time() - start_time
                workflow_duration_seconds.labels(
                    step=step_name,
                    status="success"
                ).observe(duration)
                active_workflows.dec()
        
        return wrapper
    return decorator

def start_metrics_server(port: int = 8001):
    """Inicia servidor de métricas Prometheus"""
    start_http_server(port)