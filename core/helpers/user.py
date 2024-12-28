import database as db
from core.helpers import pickle

def user():
    user_id = pickle.read('user_id')
    if user_id != None:
        with db.session() as session:
            query = session.query(db.models['main__users']).filter(db.models['main__users'].id == user_id)
        return query.first() if query.count() > 0 else None
    else:
        return None