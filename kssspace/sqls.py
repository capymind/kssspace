FETCH_ALL_GIANTS_SQL = """
SELECT    GA.id
        , GA.name
        , GA.description
        , GA.homepage
        , GA.github
        , GA.twitter_x
        , GA.mastodon
        , TG.tag_names
FROM giant                  AS GA
LEFT JOIN 
(
    SELECT    G.id
            , group_concat(T.name, ',') AS tag_names
    FROM giant                  AS G
    LEFT JOIN giant_tag_assoc   AS A
    ON 1=1
        AND G.id        = A.giant_id
    LEFT JOIN giant_tag         AS T
    ON 1=1
        AND A.tag_id    = T.id
    GROUP BY G.id
)   AS TG
ON 1=1
    AND GA.id    = TG.id
"""

SEARCH_GIANTS_SQL = """
SELECT    GA.id
        , GA.name
        , GA.description
        , GA.homepage
        , GA.github
        , GA.twitter_x
        , GA.mastodon
        , TG.tag_names
FROM giant                  AS GA
INNER JOIN
(
    SELECT    G.id
            , group_concat(T.name, ',') AS tag_names
    FROM giant                  AS G
    LEFT JOIN giant_tag_assoc   AS A
    ON 1=1
        AND G.id        = A.giant_id
    LEFT JOIN giant_tag         AS T
    ON 1=1
        AND A.tag_id    = T.id
    WHERE 1=1
        AND lower(G.name) LIKE '%' || lower(:searchword) || '%'
    GROUP BY G.id
) AS TG
ON 1=1
    AND GA.id       = TG.id
"""

FETCH_ALL_GIANT_TAGS = """
SELECT    id
        , name
FROM giant_tag
"""


def get_search_giants_by_tags_sql(and_or_condition: str, in_: str, num_of_tags: int):
    having = 1 if and_or_condition == "or" else num_of_tags
    return f"""
SELECT    GA.id
        , GA.name
        , GA.description
        , GA.homepage
        , GA.github
        , GA.twitter_x
        , GA.mastodon
        , TG.tag_names
FROM giant                  AS GA
INNER JOIN
(
    SELECT    G.id
            , group_concat(T.name, ',') AS tag_names
    FROM giant                  AS G
    LEFT JOIN giant_tag_assoc   AS A
    ON 1=1
        AND G.id        = A.giant_id
    LEFT JOIN giant_tag         AS T
    ON 1=1
        AND A.tag_id    = T.id
    GROUP BY G.id
) AS TG
ON 1=1
    AND GA.id       = TG.id
WHERE 1=1
    AND GA.id       IN (
                            SELECT    G.id
                            FROM giant                  AS G
                            LEFT JOIN giant_tag_assoc   AS A
                            ON 1=1
                                AND G.id        = A.giant_id
                            LEFT JOIN giant_tag         AS T
                            ON 1=1
                                AND A.tag_id    = T.id
                                WHERE 1=1  
                                    AND T.name      IN ({in_})
                            GROUP BY G.id
                            HAVING COUNT(*) >= {having}
    )
"""
