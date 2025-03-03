CREATE TABLE IF NOT EXISTS "Personne" (
	"id" serial NOT NULL UNIQUE,
	"nom" varchar(255) NOT NULL,
	"prenom" varchar(255) NOT NULL,
	"id_mere" bigint,
	"id_pere" bigint,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Acte" (
	"id" serial NOT NULL UNIQUE,
	"id_personneA" bigint NOT NULL,
	"id_personneB" bigint,
	"id_commune" bigint NOT NULL,
	"type" varchar(255) NOT NULL,
	"date" date NOT NULL,
	"num_vue" bigint,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Commune" (
	"id" serial NOT NULL UNIQUE,
	"nom" varchar(255) NOT NULL,
	"departement" bigint NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "Departement" (
	"num" serial NOT NULL UNIQUE,
	PRIMARY KEY ("num")
);

CREATE TABLE IF NOT EXISTS "TypeActe" (
	"nom" varchar(255) NOT NULL UNIQUE,
	PRIMARY KEY ("nom")
);

ALTER TABLE "Personne" ADD CONSTRAINT "Personne_fk3" FOREIGN KEY ("id_mere") REFERENCES "Personne"("id");

ALTER TABLE "Personne" ADD CONSTRAINT "Personne_fk4" FOREIGN KEY ("id_pere") REFERENCES "Personne"("id");
ALTER TABLE "Acte" ADD CONSTRAINT "Acte_fk1" FOREIGN KEY ("id_personneA") REFERENCES "Personne"("id");

ALTER TABLE "Acte" ADD CONSTRAINT "Acte_fk2" FOREIGN KEY ("id_personneB") REFERENCES "Personne"("id");

ALTER TABLE "Acte" ADD CONSTRAINT "Acte_fk3" FOREIGN KEY ("id_commune") REFERENCES "Commune"("id");

ALTER TABLE "Acte" ADD CONSTRAINT "Acte_fk4" FOREIGN KEY ("type") REFERENCES "TypeActe"("nom");
ALTER TABLE "Commune" ADD CONSTRAINT "Commune_fk2" FOREIGN KEY ("departement") REFERENCES "Departement"("num");

