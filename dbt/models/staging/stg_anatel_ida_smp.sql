{{ config(enabled=true, materialized='view') }}

with source as (

    select
        grupo_economico,
        variavel,
        arquivo_origem,
        aba_origem,
        modelo,
        ano_arquivo,
        competencia,
        valor,
        _ingestion_timestamp,
        _processing_date,
        _record_hash

    from read_parquet(
        's3://anatel-lake/silver/anatel_long/SMP*.parquet'
    )

),

staged as (

    select
        trim(grupo_economico) as grupo_economico,
        trim(variavel) as variavel,
        trim(arquivo_origem) as arquivo_origem,
        trim(aba_origem) as aba_origem,

        upper(trim(modelo)) as modelo,

        cast(ano_arquivo as integer) as ano_arquivo,
        cast(competencia || '-01' as date) as competencia,
        cast(valor as double) as valor,

        cast(_ingestion_timestamp as timestamp) as ingestion_timestamp,
        cast(_processing_date as date) as processing_date,

        trim(_record_hash) as record_hash

    from source

)

select *
from staged