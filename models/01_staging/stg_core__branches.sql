{{    
  config(
    materialized='view'
  )
}}
select 
    BRANCH_ID,
    BRANCH_CODE,
    BRANCH_NAME,
    CITY,
    STATE_CODE,
    ZIP_CODE,
    OPEN_DATE,
    BRANCH_STATUS,
    PROCESS_DATE
from
    {{ source('raw', 'SRC_BRANCHES') }}