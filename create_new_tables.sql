SET FOREIGN_KEY_CHECKS=0;
DROP TABLE type;
DROP TABLE genre;
DROP TABLE media;
DROP TABLE account;
DROP TABLE review;
DROP TABLE following;
SET FOREIGN_KEY_CHECKS=1;



CREATE TABLE type (
    id SERIAL,
    name VARCHAR(20),
    primary key (id)
);

CREATE TABLE genre (
    id SERIAL,
    name VARCHAR(20),
    primary key (id)
);

CREATE TABLE media (
    id SERIAL,
    type BIGINT UNSIGNED,
    genre BIGINT UNSIGNED,
    genre2 BIGINT UNSIGNED,
    genre3 BIGINT UNSIGNED,
    date_released DATE,
    studio VARCHAR(100),
    name VARCHAR(200),
    full_average REAL,
    total_reviews INT,

    FOREIGN KEY (type) REFERENCES type(id),
    FOREIGN KEY (genre) REFERENCES genre(id),
    FOREIGN KEY (genre2) REFERENCES genre(id),
    FOREIGN KEY (genre3) REFERENCES genre(id),
    PRIMARY KEY (id)
);

CREATE TABLE account (
    id SERIAL,
    name VARCHAR(30),
    username VARCHAR(50),
    date_created DATE,
    email VARCHAR(50),
    phone VARCHAR(10),
    total_reviews INT DEFAULT 0,
    total_followers INT DEFAULT 0,
    total_following INT DEFAULT 0,
    primary key (id)
);

CREATE TABLE review (
    account_id BIGINT UNSIGNED,
    media_id BIGINT UNSIGNED,
    rating real,
    description VARCHAR(200),
    date_reviewed DATE,
    FOREIGN KEY (account_id) REFERENCES account(id), 
    FOREIGN KEY (media_id) REFERENCES media(id),
    primary key (account_id, media_id)
);



CREATE TABLE following (
    account_id BIGINT UNSIGNED,
    follows_id BIGINT UNSIGNED,
    date_followed DATE,
    PRIMARY KEY (account_id, follows_id),
    FOREIGN KEY (account_id) REFERENCES account(id),
    FOREIGN KEY (follows_id) REFERENCES account(id)
);

