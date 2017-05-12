-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- player table
-- match scores table

CREATE TABLE players (name text,
                      id serial primary key );

CREATE TABLE matches (winner integer references players(id),
                      loser integer references players(id),
                      id serial PRIMARY KEY);

CREATE VIEW standings AS
                      SELECT players.id,players.name,
                      (SELECT count(matches.winner)
                      FROM matches
                      WHERE matches.winner = players.id)
                      AS wins,
                      (SELECT count(matches.id)
                      FROM matches
                      WHERE players.id = matches.winner
                      OR players.id = matches.loser)
                      AS matches
                      FROM players
                      ORDER BY wins DESC;

CREATE VIEW ranks AS
                     SELECT
                     id,
                     name,
                     ROW_NUMBER() OVER (ORDER BY wins DESC) as position
                     FROM standings
                     ORDER BY position;

CREATE VIEW groups AS
                   SELECT *,
                   -- integer division -> (1+1)/2 = 1 (2+1)/2 = 1 (3+1)/2 = 2
                   -- gives same group number for position 1,2 then 3,4 etc
                   (position+1)/2 as group
                   FROM ranks;
