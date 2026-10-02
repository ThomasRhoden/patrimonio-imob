create table estado
(
	id integer not null auto_increment,
	nome varchar(100) not null,
	sigla char(2) not null,
	primary key(id),
	constraint uk_estado_sigla unique(sigla)
);
