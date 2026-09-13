-- dim_branches.sql


{{ config(materialized='table') }}

select *
from {{ ref('int_branches') }}