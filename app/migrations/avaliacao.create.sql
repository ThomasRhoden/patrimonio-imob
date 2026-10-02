create table avaliacao
(
	id integer not null auto_increment,
	imovel_id integer not null,
	data_avaliacao date not null,
	valor_estimado decimal(12,2) not null,
	observacao text,
	primary key(id),
	constraint fk_imovel_avaliacao
		foreign key(imovel_id) references imovel(id)
);
