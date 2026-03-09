-- ==================== notification.sql (通知系统数据库脚本) ====================
-- 注释：该脚本用于初始化通知数据库的表结构、插入基础数据，以及常用的维护操作
-- 适用数据库：SQLite

-- 1. 创建通知表（核心表）
-- 作用：存储所有通知的核心信息，包含必要字段和约束
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 通知唯一ID（自增主键）
    content TEXT NOT NULL,                 -- 通知内容（不能为空）
    send_time DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 发送时间（默认当前时间）
    status INTEGER DEFAULT 0,              -- 通知状态：0=未读，1=已读，2=已删除
    user_id INTEGER NOT NULL,              -- 接收通知的用户ID（关联用户表，此处简化）
    notify_type VARCHAR(20) DEFAULT 'system'  -- 通知类型：system=系统通知，user=用户通知
);

-- 2. 创建索引（提升查询速度）
-- 作用：针对常用的查询条件（如user_id、status）创建索引，避免大数据量时查询卡顿
CREATE INDEX IF NOT EXISTS idx_notify_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notify_status ON notifications(status);
CREATE INDEX IF NOT EXISTS idx_notify_time ON notifications(send_time);

