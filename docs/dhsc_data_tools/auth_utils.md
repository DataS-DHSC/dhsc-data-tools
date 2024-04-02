Module dhsc_data_tools.auth_utils
=================================
These functions support underlying authentication processes.
They are not meant to be called directly.

Functions
---------

    
`check_auth_record(credential, authentication_record, authentication_record_path, scope)`
:   If there is no cached auth record, reauthenticate

    
`get_authentication_record_filename(**kwargs)`
:   Get auth record hashed filename.

    
`get_authentication_record_path(**kwargs)`
:   Get auth record path.

    
`read_authentication_record(authentication_record_path, use_cache=True)`
:   Reads authentication record.

    
`return_credential(client_id, tenant_id, cache_options, authentication_record)`
:   Returns an interactive

    
`write_authentication_record(authentication_record_path, authentication_record=None)`
:   Write auth record if authentication_record return is other than None type.