create table imovel_proprietario
(
	imovel_id integer not null,
	proprietario_id integer not null,
	percentual_participacao decimal(5,2) not null default 100.00,
	primary key(imovel_id, proprietario_id),
	constraint fk_imovel_imovel_proprietario
		foreign key(imovel_id)
		references imovel(id),
	constraint fk_proprietario_imovel_proprietario
		foreign key(proprietario_id)
		references proprietario(id)
);
