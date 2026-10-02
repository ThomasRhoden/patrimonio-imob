create table usuario
(
	id integer not null auto_increment,
	nome varchar(150) not null,
	login varchar(50) not null,
	senha_hash varchar(255) not null,
	primary key(id),
	constraint uk_usuario_login unique(login)
);
