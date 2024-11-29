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
    type INT,
    genre INT,
    genre2 INT,
    genre3 INT,
    date_released DATE,
    studio VARCHAR(100),
    producer VARCHAR(100),
    name VARCHAR(150),
    full_average REAL DEFAULT 0,
    total_reviews INT DEFAULT 0,
    description VARCHAR(1000),
    popularity REAL,
    language VARCHAR(10),

    FOREIGN KEY (type) REFERENCES type(id),
    FOREIGN KEY (genre) REFERENCES genre(id),
    primary key (id)
);


CREATE TABLE account (
    id  SERIAL,
    name VARCHAR(30),
    username VARCHAR(50),
    date_created DATE,
    email VARCHAR(50),
    phone VARCHAR(10),
    password VARCHAR(30),
    total_reviews INT DEFAULT 0,
    average_review REAL DEFAULT 0,
    average_expected REAL DEFAULT 0,
    total_followers INT DEFAULT 0,
    total_following INT DEFAULT 0,
    primary key (id)
);
ALTER TABLE account ADD CONSTRAINT unique_user UNIQUE (username);

CREATE TABLE review (
    account_id INT,
    media_id INT,
    rating real,
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
