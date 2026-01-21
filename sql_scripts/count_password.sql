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

-- 3. 插入初始基础数据（可选）
-- 作用：给数据库预置一些默认数据，比如系统欢迎通知
INSERT OR IGNORE INTO notifications (content, user_id, notify_type)
VALUES
    ('欢迎使用通知系统，你可以在这里接收所有重要提醒！', 1, 'system'),
    ('你的账户已完成注册，请注意保管个人信息', 1, 'system');

-- 4. 常用维护语句（注释掉，需要时取消注释执行）
-- 作用：批量清理/更新数据，比如删除过期通知、批量标记已读
-- -- 批量标记3天前的未读通知为已读
-- UPDATE notifications
-- SET status = 1
-- WHERE status = 0 AND send_time < DATETIME('now', '-3 days');

-- -- 删除30天前的已删除通知（清理垃圾数据）
-- DELETE FROM notifications
-- WHERE status = 2 AND send_time < DATETIME('now', '-30 days');