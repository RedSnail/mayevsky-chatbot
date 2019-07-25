CREATE TABLE IF NOT EXISTS taxa (
    id integer PRIMARY KEY,
    name text,
    description text,
    species bit,
    status integer
);

CREATE TABLE IF NOT EXISTS descriptions (
    id integer PRIMARY KEY,
    taxon text,
    number integer,
    thesa text,
    thesa_num integer,
    thesa_taxon text,
    athesa text,
    athesa_num integer,
    athesa_taxon text,
    status integer
);

DELETE FROM taxa;
DELETE FROM descriptions;

INSERT INTO taxa (name, species, status)
VALUES(".", 0, 1);
