create database buildfh;
use buildfh;
create table if not exists accounts (id int(11) NOT NULL AUTO_INCREMENT,username varchar(50) NOT NULL, password varchar(255) NOT NULL,email varchar(100) NOT NULL,semester varchar(50) NOT NULL,branch varchar(50) NOT NULL,PRIMARY KEY(id))ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;


create table if not exists eventstable (id int(11) NOT NULL AUTO_INCREMENT,eventtitle varchar(50) NOT NULL,eventdatetime DATETIME NOT NULL,eventlocation varchar(100) NOT NULL,maxpart int NOT NULL,eventdesc varchar(255) NOT NULL,PRIMARY KEY(id))ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

create table if not exists eventregister (username varchar(50) NOT NULL, eventtitle varchar(50) NOT NULL)ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table if not exists confirm(confirm varchar(50),email varchar(50),username varchar(50),eventtitle varchar(50));
insert into eventstable values(null,"UTSAV","2021-07-10 10.0.0","COLLEGE OF ENGINEERING CHENGANNUR","150","ARTS FESTIVAL");
insert into eventstable values(null,"TATHVA","2021-05-10 10.0.0","COLLEGE OF ENGINEERING CHENGANNUR","150","TECH FESTIVAL");
insert into eventstable values(null,"ATHENA 21","2021-12-05 10.0.0","TKM COLLEGE OF ENGINEERING","200","TECH FESTIVAL");
insert into eventstable values(null,"INFINITY","2022-01-10 10.0.0","TKM COLLEGE OF ENGINEERING","1","TECH COMPETITION");
insert into eventstable values(null,"DYUKSHA","2021-09-10 10.0.0","NSS COLLEGE OF ENGINEERING","50","SPORTS EVENT");

insert into accounts values(null,"user","user","user@gmail.com","S5","CSE");
insert into eventregister values("user","TATHVA");
insert into confirm values("yes","user@gmail.com","user","TATHVA");
insert into eventregister values("user","DYUKSHA");
