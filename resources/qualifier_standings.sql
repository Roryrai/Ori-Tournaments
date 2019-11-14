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
                          FROM race_participants rp
                            JOIN races r ON rp.race_id = r.id
                            JOIN users p ON rp.user_id = p.id
                         WHERE r.bracket_id IS NULL) x_1
                 WHERE x_1.row_num <= 7) fs
         WHERE fs."time" IS NOT NULL) x
 WHERE x.best_three <= 3 AND x.race_count >= 3
 GROUP BY x.tournament_id, x.display_name, x.participant_id
 ORDER BY x.tournament_id, (avg(x."time"));