/*
 Navicat Premium Data Transfer

 Source Server         : 本地pg
 Source Server Type    : PostgreSQL
 Source Server Version : 130000
 Source Host           : localhost:5432
 Source Catalog        : django_web
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 130000
 File Encoding         : 65001

 Date: 27/10/2020 16:12:31
*/


-- ----------------------------
-- Table structure for chart_mapping
-- ----------------------------
DROP TABLE IF EXISTS "public"."chart_mapping";
CREATE TABLE "public"."chart_mapping" (
  "module_code" varchar COLLATE "pg_catalog"."default",
  "url_code" varchar COLLATE "pg_catalog"."default",
  "chart_body" jsonb
)
;

-- ----------------------------
-- Records of chart_mapping
-- ----------------------------
INSERT INTO "public"."chart_mapping" VALUES ('dashboard', '/apis/dashboard/indicator', '{"title": "KPI", "option": [{"key": "all_users", "name": "总用户数", "value": null, "serial": 1}]}');
