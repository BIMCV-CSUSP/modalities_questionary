#! /usr/bin/env python3

from app import db

from app.models import User

u = User(username='cafetero', email='example@example.com')
u.set_password("GVApass2000")
db.session.add(u)
db.session.commit()
