from ZODB import DB
from persistent import Persistent
import transaction
from ZEO.ClientStorage import ClientStorage

from persistent.list import PersistentList

from data.classes.Board import *

def open_cs2(zhost, zport):
    storage = ClientStorage((zhost, zport))
    db = DB(storage)
    conn = db.open()
    return conn

WINDOW_SIZE = (800, 800)

board = Board(800,800)

def refreshSrvBoard(c):
    transaction.begin()
    root = c.root()
    board = root['board']
    transaction.commit()
    return board

if __name__ == '__main__':
    try:
        c = open_cs2('localhost', 2709)
        transaction.begin()
        root = c.root()
        root['board'] = PersistentList()
        root['board'] = board
        board = root['board']
        transaction.commit() 
        print('*'*40)
        print("Game created successfully. Enjoy!")
        print('*'*40)
    except:
        print('*'*40)
        print("Couldn't create game. Error happened.")
        print('*'*40)