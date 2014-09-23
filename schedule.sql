CREATE TABLE gateway (
       id SERIAL PRIMARY KEY,
       identifier text NOT NULL UNIQUE,
       hwid text NOT NULL
);
CREATE UNIQUE INDEX gateway_hwid ON gateway USING btree (hwid);

CREATE TABLE badge (
       id SERIAL PRIMARY KEY,
       hwid text NOT NULL,
       date timestamp(0) without time zone,
       gwid integer NOT NULL REFERENCES gateway(id) ON DELETE RESTRICT
);
CREATE UNIQUE INDEX hwid_uniq ON badge USING btree (hwid);

CREATE TABLE "user" (
       name text,
       nickname text,
       badgeid text NOT NULL
);
CREATE UNIQUE INDEX badgeid_uniq ON "user" USING btree (badgeid);
