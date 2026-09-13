-- dim_addresses.sql


{{ config(materialized='table') }}

select *
from {{ ref('int_addresses') }}