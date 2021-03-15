from app import get_db_session
from app.models import Constant

def not_empty():
    session = get_db_session()
    return True if session.query(Constant).filter(Constant.title == 'w').first() else False

def constants_into_db():
    if not_empty():
        return
    
    constants = []
    with open('data/constants.txt', 'r') as f:
        line = f.readline()
        while line != '':
            constants.append(tuple(line.split('==')))
            line = f.readline()
    
    session = get_db_session()
    for title, value in constants:
        constant = Constant()
        constant.title = title
        constant.value = value

        session.add(constant)
    session.commit()

if __name__ == '__main__':
    constants_into_db()