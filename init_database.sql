-- 图书馆管理系统数据库初始化脚本
-- 在MySQL中执行此脚本创建数据库

CREATE DATABASE IF NOT EXISTS library_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE library_db;

-- 显示创建成功信息
SELECT '数据库 library_db 创建成功！' AS message;
