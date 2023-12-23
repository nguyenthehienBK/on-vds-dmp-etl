SELECT 
    id
    ,user_id
    ,role_type_id
    ,tier_id
    ,status
    ,phone_number_otp
    ,pin
    ,password
    ,count_invalid_otp
    ,count_invalid_pin
    ,created_at
    ,created_by
    ,updated_at
    ,updated_by
    ,deleted_at
    ,deleted_by
    ,client_id
    ,last_ip_address
    ,count_invalid_pw
    ,last_login_device_id
FROM w3_core_uaa_datawarehouse.user_role_type_ref