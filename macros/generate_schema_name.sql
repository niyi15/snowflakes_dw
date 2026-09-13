{% macro generate_schema_name(custom_schema_name, node) -%}

    {%- if target.name in ['dev','stag','prod'] -%}

        {{ custom_schema_name }}

    {%- else -%}

        {{ target.schema ~ '_' ~ custom_schema_name }}

    {%- endif -%}

{%- endmacro %}