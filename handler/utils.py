from pydantic import BaseModel
from handler import structure_tools
from django.utils.safestring import mark_safe

import inspect
import sys
import os


def get_structure_tool_classes():

    classes = []
    for name, obj in inspect.getmembers(
        sys.modules[structure_tools.__name__], inspect.isclass
    ):
        if issubclass(obj, BaseModel) and obj.__module__ == structure_tools.__name__:
            classes.append(name)
    return classes


def get_structure_tool_class(structure_name: str):

    for name, obj in inspect.getmembers(
        sys.modules[structure_tools.__name__], inspect.isclass
    ):
        if (
            issubclass(obj, BaseModel)
            and obj.__module__ == structure_tools.__name__
            and name == structure_name
        ):
            return obj
    return None


def get_structure_tool_as_html(prompt_id: str):
    from handler.models import Prompt

    def resolve_schema(schema, resolved_schemas):
        if "$ref" in schema:
            ref = schema["$ref"].split("/")[-1]
            return resolve_schema(resolved_schemas.get(ref, {}), resolved_schemas)

        if "enum" in schema:
            options = ", ".join([f"'{str(v)}'" for v in schema["enum"]])
            return f"literal[{options}]"

        if "anyOf" in schema:
            constants = [
                str(item.get("const")) for item in schema["anyOf"] if "const" in item
            ]
            if constants:
                return f"options: {' | '.join(constants)}"
            return "multiple types"

        type_name = schema.get("type", "any")

        if type_name == "object" and "properties" in schema:
            return {
                field: resolve_schema(prop, resolved_schemas)
                for field, prop in schema["properties"].items()
            }
        elif type_name == "array" and "items" in schema:
            return [resolve_schema(schema["items"], resolved_schemas)]

        return type_name

    try:
        prompt = Prompt.objects.get(id=prompt_id)

        structure_class = get_structure_tool_class(prompt.structure_result)

        if not structure_class:
            return "No hay esquema definido."

        schema = structure_class.model_json_schema()
        resolved_schemas = schema.get("$defs", {})
        fields = resolve_schema(schema, resolved_schemas)

        def generate_html(data, indent_level=0):
            html = []
            if isinstance(data, dict):
                for field, value in data.items():
                    margin = indent_level * 20
                    if isinstance(value, (dict, list)):
                        html.append(
                            f'<div style="margin-left:{margin}px; margin-top:8px;">'
                        )
                        html.append(
                            f'<strong style="color: #4f46e5; font-size: 0.9rem;">{field}</strong>'
                        )
                        html.append(generate_html(value, indent_level + 1))
                        html.append("</div>")
                    else:
                        html.append(
                            f'<div style="margin-left:{margin}px; margin-bottom:6px;">'
                        )
                        html.append(f'<span style="color: #374151;">{field}:</span> ')
                        html.append(f'<span class="type-badge">{value}</span>')
                        html.append("</div>")
            elif isinstance(data, list):
                html.append(
                    '<span style="color: #9ca3af; font-size: 0.8rem; margin-left: 5px;">[ Lista ]</span>'
                )
                html.append(generate_html(data[0], indent_level))
            return "".join(html)

        formatted_html = generate_html(fields)

        container = f"""
        <div class="schema-container">
            <div style="font-size: 0.75rem; color: #9ca3af; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.05em;">
                Estructura de Salida Esperada
            </div>
            {formatted_html}
        </div>
        """
        return mark_safe(container)

    except Exception as e:
        return f"Error procesando el esquema: {str(e)}"


def get_mcp_files():
    mcp_dir = "handler/mcp_server"
    return [
        os.path.join(mcp_dir, file)
        for file in os.listdir(mcp_dir)
        if file.endswith(".py") and file != "__init__.py"
    ]
