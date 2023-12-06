CREATE TABLE usuario (
    email varchar(100) PRIMARY KEY,
    password1 varchar(12),
    token varchar(12),
    timestamp1 varchar(12),
    estado varchar(12)
);

INSERT INTO usuario (email, password1, token, timestamp1, estado)
VALUES ('Dany@gmail.com', '123456789', 'xyz123', "60", 'activo');
