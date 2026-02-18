-- ==================== user_account.sql (用户账号密码数据库脚本) ====================
-- 注释：该脚本用于初始化用户账号密码数据库的表结构、插入基础数据，以及常用的维护操作
-- 适用数据库：SQLite
-- 安全提示：生产环境中密码务必存储哈希值（如bcrypt/SHA256），切勿存储明文！

-- 1. 创建用户账号表（核心表）
-- 作用：存储用户账号的核心信息，包含必要字段和约束，保障账号唯一性和数据完整性
CREATE TABLE IF NOT EXISTS user_accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 用户唯一ID（自增主键）
    username VARCHAR(50) NOT NULL UNIQUE,  -- 用户名（非空+唯一约束，避免重复账号）
    password_hash TEXT NOT NULL,           -- 密码哈希值（非空，存储加密后的密码，禁止明文）
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 账号创建时间（默认当前时间）
    last_login_time DATETIME,              -- 最后登录时间（首次登录前为NULL）
    status INTEGER DEFAULT 1,              -- 账号状态：0=禁用，1=正常，2=锁定（默认正常）
    email VARCHAR(100) UNIQUE,             -- 邮箱（可选，唯一，用于找回密码/验证）
    phone VARCHAR(20) UNIQUE,              -- 手机号（可选，唯一，用于找回密码/验证）
    remark TEXT                            -- 备注信息（如账号用途、所属部门等）
);

-- 2. 创建索引（提升查询速度）
-- 作用：针对常用查询条件创建索引，避免大数据量时查询卡顿
CREATE INDEX IF NOT EXISTS idx_user_username ON user_accounts(username);  -- 用户名索引（高频查询）
CREATE INDEX IF NOT EXISTS idx_user_status ON user_accounts(status);      -- 账号状态索引（筛选正常/禁用账号）
CREATE INDEX IF NOT EXISTS idx_user_last_login ON user_accounts(last_login_time);  -- 最后登录时间索引（清理久未登录账号）

-- 3. 插入初始基础数据（可选）
-- 作用：预置基础账号（如管理员账号），注意：生产环境需修改默认密码！
-- 示例：admin账号的密码哈希（原始密码：Admin@123456，使用bcrypt加密）
INSERT OR IGNORE INTO user_accounts (username, password_hash, email, remark)
VALUES
    ('admin', '$2a$10$8H9w4z7e8s9d8f7g6h5j4k3l2m1n0b9v8c7x6s5d4f3g2h1j0k', 'admin@example.com', '系统管理员账号'),
    ('test_user', '$2a$10$1a2b3c4d5e6f7g8h9i0j1k2l3m4n5b6v7c8x9s0d1f2g3h4j', 'test@example.com', '测试用户账号');

-- 4. 常用维护语句（注释掉，需要时取消注释执行）
-- 作用：日常账号管理操作，如重置密码、禁用账号、清理久未登录账号等

-- -- 重置指定用户的密码（示例：重置admin的密码哈希，新密码：NewAdmin@654321）
-- UPDATE user_accounts
-- SET password_hash = '$2a$10$9z8y7x6w5v4u3t2s1r0q9p8o7n6m5l4k3j2i1h0g9f8e7d6c5b'
-- WHERE username = 'admin';

-- -- 禁用指定账号（示例：禁用test_user账号）
-- UPDATE user_accounts
-- SET status = 0
-- WHERE username = 'test_user';

-- -- 锁定连续失败登录的账号（示例：锁定last_login_time为空且创建超30天的账号）
-- UPDATE user_accounts
-- SET status = 2
-- WHERE last_login_time IS NULL AND create_time < DATETIME('now', '-30 days');

-- -- 清理长期未登录且已禁用的账号（示例：删除90天未登录的禁用账号）
-- DELETE FROM user_accounts
-- WHERE status = 0 AND last_login_time < DATETIME('now', '-90 days');

-- -- 查询所有正常状态的账号
-- SELECT id, username, email, last_login_time FROM user_accounts WHERE status = 1;

--===============================================================================================
-- 1. 创建邀请码表（核心表）
-- 作用：存储用户账号的核心信息，包含必要字段和约束，保障账号唯一性和数据完整性
CREATE TABLE IF NOT EXISTS invite_number (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL UNIQUE,
    invite_num INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

--===============================================================================================
-- 1. 创建麻将分数表（核心表）
-- 作用：存储用户账号的核心信息，包含必要字段和约束，保障账号唯一性和数据完整性
CREATE TABLE IF NOT EXISTS majiang (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    socre INTEGER NOT NULL
);