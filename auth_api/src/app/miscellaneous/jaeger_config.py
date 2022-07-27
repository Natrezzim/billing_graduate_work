
import os

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider(resource=Resource.create({SERVICE_NAME: "auth_service"})))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=os.getenv("JAEGER_HOST"),
                agent_port=int(os.getenv("JAEGER_PORT")),
            )
        )
    )
