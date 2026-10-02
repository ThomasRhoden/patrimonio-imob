create table proprietario
(
	id integer not null auto_increment,
	nome varchar(150) not null,
	cpf varchar(14),
	email varchar(180),
	telefone varchar(30),
	primary key(id)
);
