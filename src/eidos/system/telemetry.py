import functools
import inspect
from typing import Callable, Any, TypeVar, ParamSpec
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource

from .config import settings

# Setup Global Tracer
resource = Resource(attributes={
    "service.name": "eidos-framework",
    "service.version": "1.0.0"
})

provider = TracerProvider(resource=resource)

# In a real scenario, we would check settings.otel_exporter_otlp_endpoint
# For now, we just use Console if in debug mode, or NoOp implicitly (Provider default)
if settings.log_level == "DEBUG":
    # export to console for visibility in dev
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    provider.add_span_processor(processor)

trace.set_tracer_provider(provider)
tracer = trace.get_tracer("eidos.core")

P = ParamSpec("P")
R = TypeVar("R")

def trace_span(name: str | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator to auto-instrument functions with OpenTelemetry spans.
    Supports both sync and async functions.
    """
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        span_name = name or func.__qualname__

        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                with tracer.start_as_current_span(span_name) as span:
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(trace.Status(trace.StatusCode.ERROR))
                        raise e
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                with tracer.start_as_current_span(span_name) as span:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        span.record_exception(e)
                        span.set_status(trace.Status(trace.StatusCode.ERROR))
                        raise e
            return sync_wrapper
    return decorator
