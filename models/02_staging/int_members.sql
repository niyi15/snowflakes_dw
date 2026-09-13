{{config(
    materialized = 'view'
)}}
select * from {{ ref('stg_core__members')}}