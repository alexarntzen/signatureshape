.headers on
.mode csv

.output /Users/alexander/git_repos/git_skole/paalel-master/code/data/similarity.csv
SELECT animation_id1, animation_id2, signature_distance, se3_signature_distance
FROM similarity 
WHERE animation_id1 not in
(1649, 1516, 1491,1493,1521,1528)
and animation_id2 not in
(1649, 1516, 1491,1493,1521,1528)
ORDER BY animation_id1;

.output /Users/alexander/git_repos/git_skole/paalel-master/code/data/names.csv
SELECT animation_id,
description || ' (' || substr(file_name, -4, -100) || ')'
FROM animation 
WHERE animation_id IN (
	SELECT distinct(animation_id1) FROM similarity 
	WHERE animation_id1 not in
    (1649, 1516, 1491,1493,1521,1528)
)
ORDER BY animation_id;
.quit
