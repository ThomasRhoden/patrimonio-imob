create table despesa
(
	id integer not null auto_increment,
	imovel_id integer not null,
	descricao varchar(255) not null,
	valor decimal(12,2) not null,
	data_despesa date not null,
	primary key(id),
	constraint fk_imovel_despesa
		foreign key(imovel_id) references imovel(id)
);
