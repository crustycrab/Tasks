drop table if exists classes;
drop table if exists tasks;
drop table if exists workers;
create table tasks (
	id int auto_increment not null,
	date timestamp not null,
	task text not null,
	result tinyint(1) not null,
	primary key (id)
) ENGINE=InnoDB CHARSET=utf8;
create table workers (
	id int auto_increment not null,
	worker varchar(255) not null,
	primary key (id)
) ENGINE=InnoDB CHARSET=utf8;
create table classes (
	id int auto_increment not null,
	task_id int not null,
	worker_id int not null,
	primary key (id),
	foreign key (task_id) references tasks(id),
	foreign key (worker_id) references workers(id)
) ENGINE=InnoDB;
insert into workers (worker) values ('John');
insert into workers (worker) values ('Patrick');
insert into workers (worker) values ('Max');
insert into workers (worker) values ('Kesha');
-- 0 == Done, 1 == In process, 2 == Canceled
insert into tasks (date, task, result) values ('2014-05-14 17:16:34', 'Убраться в доме', 0);
insert into tasks (date, task, result) values ('2014-05-13 20:54:34', 'Подстричь лужайку', 2);
insert into tasks (date, task, result) values ('2014-05-13 08:33:34', 'Нарубить дров', 1);
insert into tasks (date, task, result) values ('2014-05-12 11:06:34', 'Расчистить дорожку у дома', 0);
insert into tasks (date, task, result) values ('2014-05-11 13:01:34', 'Собрать урожай', 1);
insert into classes (task_id, worker_id) values (1, 2);
insert into classes (task_id, worker_id) values (1, 4);
insert into classes (task_id, worker_id) values (2, 1);
insert into classes (task_id, worker_id) values (2, 2);
insert into classes (task_id, worker_id) values (3, 3);
insert into classes (task_id, worker_id) values (3, 1);
insert into classes (task_id, worker_id) values (4, 2);
insert into classes (task_id, worker_id) values (5, 4);
insert into classes (task_id, worker_id) values (5, 3);