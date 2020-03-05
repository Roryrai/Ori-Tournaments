from sqlalchemy import text

from app import db

from app.models import GroupStandings
from app.models import QualifierStandings

class StandingsService():

    # Gets qualifier standings for a given tournament
    def getQualifierStandings(tournament):
        statement = text("""
            SELECT x.tournament_id,
                x.display_name,
                avg(x."time") AS average_time,
                x.participant_id AS id
               FROM ( SELECT row_number() OVER (PARTITION BY fs.tournament_id, fs.display_name ORDER BY fs."time") AS best_three,
                        count(*) OVER (PARTITION BY fs.tournament_id, fs.display_name) AS race_count,
                        fs.row_num,
                        fs.display_name,
                        fs."time",
                        fs.date,
                        fs.participant_id,
                        fs.tournament_id
                       FROM ( SELECT x_1.row_num,
                                x_1.tournament_id,
                                x_1.date,
                                x_1.display_name,
                                x_1."time",
                                x_1.participant_id
                               FROM ( SELECT row_number() OVER (PARTITION BY r.tournament_id, p.username ORDER BY r.date) AS row_num,
                                        r.date,
                                        r.tournament_id,
                                        p.username AS display_name,
                                        rp.user_id AS participant_id,
                                        rp."time"
                                       FROM race_result rp
                                         JOIN race r ON rp.race_id = r.id
                                         JOIN "user" p ON rp.user_id = p.id
                                      WHERE r.bracket_id IS NULL) x_1
                              WHERE x_1.row_num <= 7) fs
                      WHERE fs."time" IS NOT NULL) x
              WHERE x.best_three <= 3 AND x.race_count >= 3
                AND x.tournament_id = :tournament_id
              GROUP BY x.tournament_id, x.display_name, x.participant_id
              ORDER BY x.tournament_id, (avg(x."time"))
        """)

        params = {"tournament_id": tournament.id}
        result = db.session.execute(statement, params)

        standings = list()
        place = 0
        for row in result:
            place += 1
            record = QualifierStandings(place=place, user=row[1], average_time=row[2])
            standings.append(record)

        return standings

    # Retrieves the standings of a tournament formatted as group stage
    def getGroupStandings(tournament):
        statement = text("""
            SELECT COALESCE(winners.tournament_id, losers.tournament_id) AS tournament_id,
                COALESCE(winners.group_name, losers.group_name) AS group_name,
                COALESCE(winners.username, losers.username) AS username,
                COALESCE(winners.wins, 0::bigint) AS wins,
                COALESCE(losers.losses, 0::bigint) AS losses
               FROM ( SELECT group_winners.tournament_id,
                        group_winners.group_name,
                        group_winners.username,
                        count(*) AS wins
                       FROM ( SELECT gn.group_name,
                                ordered.place,
                                u.username,
                                ordered."time",
                                r.date,
                                r.tournament_id
                               FROM ( SELECT row_number() OVER (PARTITION BY grp.race_id ORDER BY grp."time") AS place,
                                        grp.id,
                                        grp.race_id,
                                        grp.user_id,
                                        grp."time",
                                        grp.comments
                                       FROM race_result grp) ordered
                                 JOIN race r ON ordered.race_id = r.id
                                 JOIN "user" u ON ordered.user_id = u.id
                                 JOIN group_member rg ON rg.user_id = u.id
                                 JOIN group_name gn ON gn.id = rg.group_id
                              WHERE ordered.place = 1 AND r.bracket_id IS NULL
                              ORDER BY gn.group_name) group_winners
                      GROUP BY group_winners.tournament_id, group_winners.group_name, group_winners.username) winners
                 FULL JOIN ( SELECT group_losers.tournament_id,
                        group_losers.group_name,
                        group_losers.username,
                        count(*) AS losses
                       FROM ( SELECT gn.group_name,
                                ordered.place,
                                u.username,
                                ordered."time",
                                r.date,
                                r.tournament_id
                               FROM ( SELECT row_number() OVER (PARTITION BY grp.race_id ORDER BY grp."time") AS place,
                                        grp.id,
                                        grp.race_id,
                                        grp.user_id,
                                        grp."time",
                                        grp.comments
                                       FROM race_result grp) ordered
                                 JOIN race r ON ordered.race_id = r.id
                                 JOIN "user" u ON ordered.user_id = u.id
                                 JOIN group_member rg ON rg.user_id = u.id
                                 JOIN group_name gn ON gn.id = rg.group_id
                              WHERE ordered.place > 1 AND r.bracket_id IS NULL
                              ORDER BY gn.group_name) group_losers
                      GROUP BY group_losers.tournament_id, group_losers.group_name, group_losers.username) losers ON winners.username = losers.username AND winners.tournament_id = losers.tournament_id
              WHERE winners.tournament_id = :tournament_id OR losers.tournament_id = :tournament_id
              ORDER BY (COALESCE(winners.tournament_id, losers.tournament_id)), (COALESCE(winners.group_name, losers.group_name)), (COALESCE(winners.wins, 0::bigint)) DESC, (COALESCE(winners.username, losers.username))
            """)

        params = {"tournament_id": tournament.id}
        result = db.session.execute(statement, params)

        standings = list()
        place = 0
        current_group = None
        for row in result:
            if not current_group or row[1] != current_group.group:
                current_group = GroupStandings(group=row[1], standings=list())
                standings.append(current_group)
            record = GroupStandings.Standing(user=row[2], wins=row[3], losses=row[4])
            current_group.standings.append(record)

        return standings


