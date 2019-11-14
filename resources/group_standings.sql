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
                          FROM race_participants grp) ordered
                    JOIN races r ON ordered.race_id = r.id
                    JOIN users u ON ordered.user_id = u.id
                    JOIN runner_groups rg ON rg.user_id = u.id
                    JOIN group_names gn ON gn.id = rg.group_id
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
                          FROM race_participants grp) ordered
                    JOIN races r ON ordered.race_id = r.id
                    JOIN users u ON ordered.user_id = u.id
                    JOIN runner_groups rg ON rg.user_id = u.id
                    JOIN group_names gn ON gn.id = rg.group_id
                 WHERE ordered.place > 1 AND r.bracket_id IS NULL
                 ORDER BY gn.group_name) group_losers
         GROUP BY group_losers.tournament_id, group_losers.group_name, group_losers.username) losers ON winners.username = losers.username AND winners.tournament_id = losers.tournament_id
 ORDER BY (COALESCE(winners.tournament_id, losers.tournament_id)), (COALESCE(winners.group_name, losers.group_name)), (COALESCE(winners.wins, 0::bigint)) DESC, (COALESCE(winners.username, losers.username));