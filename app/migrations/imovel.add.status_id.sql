alter table imovel add column status_id integer not null;
alter table imovel add constraint fk_status_imovel_imovel
	foreign key(status_id) references status_imovel(id);
