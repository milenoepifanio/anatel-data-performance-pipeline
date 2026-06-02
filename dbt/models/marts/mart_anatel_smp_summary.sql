{{ config(materialized='table') }}

with base as (
    select *
    from {{ ref('stg_anatel_ida_smp') }}
),

summary as (
    select
        grupo_economico,
        modelo,
        variavel,
        min(competencia) as first_competencia,
        max(competencia) as last_competencia,
        count(*) as record_count,
        sum(valor) as total_valor,
        avg(valor) as avg_valor,
        min(valor) as min_valor,
        max(valor) as max_valor
    from base
    group by grupo_economico, modelo, variavel
)

select *
from summary
