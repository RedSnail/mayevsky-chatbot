DELETE FROM taxa;
DELETE FROM descriptions;

INSERT INTO taxa (name, species, status)
VALUES(".", 0, 1);
