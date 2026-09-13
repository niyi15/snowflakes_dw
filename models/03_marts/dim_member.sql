-- dim_member.sql

{{ config(materialized='table') }}

select *
from {{ ref('int_members') }}