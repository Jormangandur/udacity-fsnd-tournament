#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
from functools import wraps
import psycopg2


def db_wrap(func):
    '''Wrap function in PostgreSQL transaction.

    Connects to database, creates a cursor, begins transaction, executes
    function then closes connection.
    Wrapped function needs cursor as first arg - other are preserved.

    Args:
        func: function to wrap with first argument as cursor
    '''
    @wraps(func)
    def connected_func(*args, **kwargs):
        conn = connect()
        c = conn.cursor()
        try:
            c.execute("BEGIN")
            transaction = func(c, *args, **kwargs)  # Pass cursor to func
            conn.commit()
        except:
            conn.rollback()  # Prevent any incorrect transactions on any error
            raise
        finally:
            c.close()
            conn.close()
        return transaction
    return connected_func


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect(dbname="tournament")


@db_wrap
def deleteMatches(cursor):
    """Remove all the match records from the database."""
    cursor.execute("DELETE FROM matches;")


@db_wrap
def deletePlayers(cursor):
    """Remove all the player records from the database."""
    cursor.execute("DELETE FROM players;")


@db_wrap
def countPlayers(cursor):
    """Returns the number of players currently registered."""
    cursor.execute("select count(*) from players;")
    count = cursor.fetchall()
    return count[0][0]  # first column, first row of result table


@db_wrap
def registerPlayer(cursor, name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    cursor.execute("INSERT INTO players VALUES (%s);", (name,))


@db_wrap
def playerStandings(cursor):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player'pair_orders full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    cursor.execute("SELECT * FROM standings;")
    standings = cursor.fetchall()
    return standings


@db_wrap
def reportMatch(cursor, winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    cursor.execute("INSERT INTO matches values (%s, %s);", (winner, loser,))


@db_wrap
def swissPairings(cursor):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    cursor.execute("SELECT id, name FROM groups;")
    pair_order = cursor.fetchall()  # list of tuples [(id,name),(id,name)...]
    pairs_list = []
    # zip lists created from alternate list item slices
    for p1, p2 in zip(pair_order[0::2], pair_order[1::2]):  # [start_pos::step]
        # p1 = (id1,name1)
        # p2 = (id2,name2)
        # takes each item from p1, p2 tuples into new tuple
        pairs_list.append((p1[0], p1[1], p2[0], p2[1]))
    return pairs_list
