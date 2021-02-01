CREATE TABLE images (
    id SERIAL PRIMARY KEY, 
    name TEXT, 
    data BYTEA
);

CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    image_id INTEGER REFERENCES images ON DELETE CASCADE,
    points INTEGER
);

CREATE TABLE photographer (
    id SERIAL PRIMARY KEY,
    image_id INTEGER REFERENCES images ON DELETE CASCADE,
    name TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY, 
    username TEXT UNIQUE, 
    password TEXT
);