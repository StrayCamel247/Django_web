 CREATE SEQUENCE public."page_permission_page_id_seq" 
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 99999999
    CACHE 1;
/*
 Navicat Premium Data Transfer

 Source Server         : 10.7.115.20
 Source Server Type    : PostgreSQL
 Source Server Version : 100007
 Source Host           : 10.7.115.20:5432
 Source Catalog        : linezone
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 100007
 File Encoding         : 65001

 Date: 27/10/2020 16:03:19
*/


-- ----------------------------
-- Table structure for page_permission
-- ----------------------------
DROP TABLE IF EXISTS "public"."page_permission";
CREATE TABLE "public"."page_permission" (
  "create_time" timestamp(6) NOT NULL DEFAULT now(),
  "update_time" timestamp(6) NOT NULL DEFAULT now(),
  "is_active" bool NOT NULL DEFAULT true,
  "remark" text COLLATE "pg_catalog"."default",
  "extra1" varchar COLLATE "pg_catalog"."default",
  "extra2" varchar COLLATE "pg_catalog"."default",
  "page_id" int4 NOT NULL DEFAULT nextval('page_permission_page_id_seq'::regclass),
  "page_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "page_route" varchar(64) COLLATE "pg_catalog"."default",
  "parent_id" int4,
  "weight" int4,
  "icon" varchar COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Uniques structure for table page_permission
-- ----------------------------
ALTER TABLE "public"."page_permission" ADD CONSTRAINT "page_permission_page_name_key" UNIQUE ("page_name");

-- ----------------------------
-- Primary Key structure for table page_permission
-- ----------------------------
ALTER TABLE "public"."page_permission" ADD CONSTRAINT "page_permission_pkey" PRIMARY KEY ("page_id");
