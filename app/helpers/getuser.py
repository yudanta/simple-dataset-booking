#!/usr/bin/env python 

def get_user(current_user):
    if current_user:
        build_user = {
            'id': current_user.id,
            'username': current_user.username,
            'firstname': current_user.firstname,
            'lastname': current_user.lastname,
            'status': current_user.status,
        }
        
        return build_user
    else:
        return None 