{{config(
    materialized = ' table'

)}}
select * from {{ ref('stg_core__members')}}