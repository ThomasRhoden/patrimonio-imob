create table movimentacao
(
	id integer not null auto_increment,
	imovel_id integer not null,
	tipo varchar(50) not null,
	valor decimal(12,2),
	data_movimentacao date not null,
	observacao text,
	primary key(id),
	constraint fk_imovel_movimentacao
		foreign key(imovel_id) references imovel(id)
);
