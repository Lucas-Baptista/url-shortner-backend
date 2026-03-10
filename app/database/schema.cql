CREATE KEYSPACE IF NOT EXISTS url_shortener
WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': 1
};

USE url_shortener;

CREATE TABLE IF NOT EXISTS urls (
    short_code text PRIMARY KEY,
    original_url text,
    created_at timestamp
);

CREATE TABLE IF NOT EXISTS url_clicks (
    short_code text PRIMARY KEY,
    clicks counter
);