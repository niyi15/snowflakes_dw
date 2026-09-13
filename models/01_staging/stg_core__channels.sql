{{    
  config(
    materialized='view'
  )
}}
select 
    CHANNEL_ID,
    CHANNEL_CODE,
    CHANNEL_NAME,
    CHANNEL_TYPE,
    ACTIVE_FLAG,
    PROCESS_DATE
from
    {{ source('raw', 'SRC_CHANNELS') }}