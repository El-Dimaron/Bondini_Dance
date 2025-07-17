import pydot
from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Draw database schema with pydot"

    def handle(self, *args, **kwargs):
        graph = pydot.Dot(graph_type="digraph", rankdir="LR")

        models = apps.get_models()
        table_nodes = {}

        # Step 1: Add all models as nodes
        for model in models:
            fields = [f.name for f in model._meta.fields]
            label = f"{model.__name__}|{'|'.join(fields)}"
            node = pydot.Node(model.__name__, shape="record", label=f"{{{label}}}")
            graph.add_node(node)
            table_nodes[model] = model.__name__

        # Step 2: Add foreign key relations
        for model in models:
            for field in model._meta.fields:
                if field.is_relation and field.remote_field:
                    from_node = model.__name__
                    to_node = field.related_model.__name__
                    edge = pydot.Edge(from_node, to_node, label=field.name)
                    graph.add_edge(edge)

        # Step 3: Output
        graph.write_png("db_schema.png")
        self.stdout.write(self.style.SUCCESS("Schema written to db_schema.png"))
