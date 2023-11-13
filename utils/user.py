def auth(username: str, password: str):
    return {
        "error": 0, 
        "user_info": {
            "user_id": 1, 
            "username": username, 
            "password": password, 
            "email": None, 
            "is_admin": 1, 
            "is_trial": 0, 
            "status": "Active", 
            "exp_date": None, 
            "max_connections": 2, 
            "created_at": None, 
            "active_cons": 0, 
            "allowed_output_formats": ["m3u8", "ts"], 
            "auth_hash": None
        }
    }


def user_info_xtream(data, username, password):
    return {
        "username": username,
        "password": password,
        "message": "Welcome to My Xtream!",
        "auth": 1,
        "status": "Active",
        "exp_date": None,
        "is_trial": "0",
        "active_cons": "0",
        "created_at": None,
        "max_connections": "2",
        "allowed_output_formats": ["m3u8", "ts", "rtmp"],
    }

