import requests


def make_get_request(url, session):
    return requests.get(url, headers={'Username': session["username"], 'Session-Token': session["sessionToken"]})

def make_patch_request(url, session):
    return requests.patch(url, headers={'Username': session["username"], 'Session-Token': session["sessionToken"]})

def make_delete_request(url, session):
    return requests.delete(url, headers={'Username': session["username"], 'Session-Token': session["sessionToken"]})