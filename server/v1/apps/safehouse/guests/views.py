# Guest
#
# 1. Create a guest account/model
# 2. Set Requirements for safehouse (e.g. no dogs, female host)
# 3. Set Traits of guest (e.g. smoker, male)
# 4. Send safehouse requests to all nearby and matching hosts
# 5. Chat with hosts and schedule meeting
# 6. Review hosts

from flask_socketio import SocketIO, emit, disconnect
from flask import Flask, request, jsonify, abort

from v1.apps import socketio, db

#Error handling
from v1.apps.errors import *

from . import safehouse_guests

from v1.apps.users.models import authenticate, user_auth
from .models import Guest
from ..models import Trait

from v1.apps.parsers import *



@safehouse_guests.route('/register', methods=['POST'])
def register_guest_account():
    user = user_auth(request)
    if user is None or Guest.query.filter_by(user = user).first() is not None:
        abort(400)
    guest = Guest(user=user, traits=Trait(), requirements=Trait())
    db.session.add(guest)
    db.session.commit()
    return jsonify({
        'username': user.username,
        'guest': parse_guest(guest),
    })

@safehouse_guests.route('/traits', methods=['POST'])
def edit_guest_traits():
    user = user_auth(request)
    data = request.get_json()
    if user is not None:
        if (user.guest.process_traits(data)):
            return jsonify({
                'username': user.username,
                'guest': parse_guest(user.guest),
            })
    else:
        abort(400)

@safehouse_guests.route('/requirements', methods=['POST'])
def edit_guest_requirements():
    user = user_auth(request)
    data = request.get_json()
    if user is not None:
        if (user.guest.process_requirements(data)):
            return jsonify({
                'username': user.username,
                'guest': parse_guest(user.guest),
            })
    else:
        abort(400)
