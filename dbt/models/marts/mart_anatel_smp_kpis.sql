{{ config(materialized='table') }}

with base as (
    select *
    from {{ ref('stg_anatel_ida_smp') }}
),

kpis as (
    select
        competencia,
        grupo_economico,
        count(*) as record_count,
        count(distinct variavel) as distinct_variavel_count,
        sum(valor) as total_valor,
        avg(valor) as avg_valor,
        max(ingestion_timestamp) as last_ingestion_timestamp
    from base
    group by competencia, grupo_economico
)

select *
from kpis
