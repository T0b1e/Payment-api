CREATE TABLE "wallet" (
	"id"	INTEGER,
	"name"	TEXT,
	"deposit"	REAL,
	"cash"	REAL,
	PRIMARY KEY("id" AUTOINCREMENT)
)

CREATE TABLE "transactions" (
	"id"	INTEGER,
	"date"	INTEGER DEFAULT CURRENT_DATE,
	"time"	INTEGER DEFAULT CURRENT_TIME,
	"action"	TEXT,
	"types"	TEXT,
	"amount"	REAL DEFAULT 0.0,
	"origin_wallet_name"	TEXT,
	"origin_wallet_value"	REAL DEFAULT 0.0,
	"destination_wallet_name"	TEXT,
	"destination_wallet_value"	REAL DEFAULT 0.0,
	"tag_id"	INTEGER,
	"description"	TEXT,
	PRIMARY KEY("id")
)

CREATE TABLE "income" (
	"id"	INTEGER NOT NULL,
	"date"	DATE,
	"time"	TIME,
	"category"	VARCHAR,
	"wallet_id"	INTEGER NOT NULL,
	"amount"	FLOAT,
	"tag_id"	INTEGER,
	"description"	VARCHAR,
	PRIMARY KEY("id")
)

CREATE TABLE "expense" (
	"id"	INTEGER NOT NULL,
	"date"	DATE,
	"time"	TIME,
	"category"	VARCHAR,
	"wallet_id"	INTEGER NOT NULL,
	"amount"	FLOAT,
	"tag_id"	INTEGER,
	"description"	VARCHAR,
	PRIMARY KEY("id")
)

CREATE TABLE "transfer" (
	"transfer_id"	INTEGER NOT NULL,
	"date"	DATE,
	"time"	TIME,
	"origin_wallet_name"	TEXT,
	"origin_wallet_value"	REAL,
	"destination_wallet_name"	TEXT,
	"destination_wallet_value"	REAL,
	"description"	TEXT,
	PRIMARY KEY("transfer_id" AUTOINCREMENT)
)

CREATE TABLE "categories" (
	"id"	INTEGER,
	"name"	TEXT,
	"type"	TEXT,
	PRIMARY KEY("id")
)

CREATE TABLE "log" (
	"id"	INTEGER NOT NULL,
	"date"	DATE,
	"time"	TIME,
	"category"	VARCHAR,
	"wallet_id"	INTEGER NOT NULL,
	"amount"	FLOAT,
	"tag_id"	INTEGER,
	"description"	VARCHAR,
	PRIMARY KEY("id")
)

