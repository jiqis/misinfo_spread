CREATE TEMP VIEW v AS
    SELECT 
        MAX(article.canonical_url) as url, 
        COUNT(*) AS num_tweets
    FROM site 
        JOIN url
        ON site.id = url.site_id

        JOIN ass_tweet_url
        ON url.id = ass_tweet_url.url_id

        JOIN tweet
        ON tweet.id = ass_tweet_url.tweet_id

        JOIN article
        ON article.id = url.article_id
    WHERE site.site_type = 'claim' 
        AND tweet.created_at BETWEEN '20160516' AND '20170331'
    GROUP BY article.group_id
    ORDER BY num_tweets DESC
    LIMIT 100
    ;

\COPY (SELECT * FROM v) TO stdout WITH CSV HEADER;

DROP VIEW v;
