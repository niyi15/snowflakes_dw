-- dim_member.sql

{{ config(materialized='table') }}

select *
from {{ ref('dim_member') }}