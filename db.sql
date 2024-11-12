CREATE TABLE media_type (
    id SERIAL,
    name VARCHAR(20),
    primary key (id)
);

CREATE TABLE media_genre (
    id SERIAL,
    name VARCHAR(20),
    primary key (id)
);

CREATE TABLE media (
    id SERIAL,
    type INT,
    genre INT,
    date_released DATE,
    name VARCHAR(50),
    FOREIGN KEY (type) REFERENCES media_type(id),
    FOREIGN KEY (genre) REFERENCES media_genre(id),
    primary key (id)
);

CREATE TABLE account (
    id  SERIAL,
    name VARCHAR(30),
    date_created DATE,
    total_reviews INT,
    primary key (id)
);

CREATE TABLE review (
    account_id INT,
    media_id INT,
    rating REAL,
    description VARCHAR(200),
    date_reviewed DATE,
    FOREIGN KEY (account_id) REFERENCES account(id), 
    FOREIGN KEY (media_id) REFERENCES media(id),
    primary key (account_id, media_id)
);



CREATE TABLE following (
    account_id INT,
    follows_id INT,
    date_followed DATE,
    PRIMARY KEY (account_id, follows_id),
    FOREIGN KEY (account_id) REFERENCES account(id),
    FOREIGN KEY (follows_id) REFERENCES account(id)
);
