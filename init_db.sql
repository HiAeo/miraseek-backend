-- MiraSeek 数据库初始化脚本
-- 在 Supabase Dashboard > SQL Editor 中执行

-- 1. 品牌配置表
CREATE TABLE IF NOT EXISTS miraseek_brands (
    id SERIAL PRIMARY KEY,
    brand_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    website VARCHAR(255),
    core_technicals TEXT[],
    competitors INTEGER[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 2. 监控任务配置表
CREATE TABLE IF NOT EXISTS miraseek_tasks (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES miraseek_brands(id) ON DELETE CASCADE,
    prompt_text TEXT NOT NULL,
    prompt_type VARCHAR(20) DEFAULT 'custom',
    ai_models TEXT[] NOT NULL DEFAULT ARRAY['deepseek'],
    frequency VARCHAR(10) DEFAULT '1d',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- 3. 监控结果表
CREATE TABLE IF NOT EXISTS miraseek_results (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES miraseek_tasks(id) ON DELETE CASCADE,
    brand_id INTEGER REFERENCES miraseek_brands(id),
    ai_model VARCHAR(20),
    query_timestamp TIMESTAMP DEFAULT NOW(),
    rank SMALLINT,
    answer_text TEXT,
    sentiment_score NUMERIC(3,2),
    decision_stage VARCHAR(20),
    official_citation BOOLEAN DEFAULT FALSE,
    extracted_params JSONB,
    citations TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- 4. 预警规则表
CREATE TABLE IF NOT EXISTS miraseek_alert_rules (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES miraseek_brands(id),
    rule_type VARCHAR(20),
    threshold_value NUMERIC,
    is_active BOOLEAN DEFAULT TRUE,
    notify_emails TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

-- 5. 预警记录表
CREATE TABLE IF NOT EXISTS miraseek_alerts (
    id SERIAL PRIMARY KEY,
    rule_id INTEGER REFERENCES miraseek_alert_rules(id),
    brand_id INTEGER,
    alert_type VARCHAR(20),
    level VARCHAR(20) DEFAULT 'info',
    title VARCHAR(200),
    message TEXT,
    triggered_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'unread',
    is_resolved BOOLEAN DEFAULT FALSE
);

-- 6. 报告表
CREATE TABLE IF NOT EXISTS miraseek_reports (
    id VARCHAR(50) PRIMARY KEY,
    brand_id INTEGER REFERENCES miraseek_brands(id),
    report_type VARCHAR(20),
    date_start DATE,
    date_end DATE,
    status VARCHAR(20) DEFAULT 'processing',
    download_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- 7. 品牌快照表（每日聚合）
CREATE TABLE IF NOT EXISTS miraseek_brand_snapshots (
    id SERIAL PRIMARY KEY,
    brand_id INTEGER REFERENCES miraseek_brands(id),
    snapshot_date DATE NOT NULL,
    visibility_index NUMERIC(5,2),
    avg_sentiment NUMERIC(3,2),
    total_mentions INTEGER,
    avg_rank NUMERIC(4,2),
    top_citations TEXT[],
    UNIQUE(brand_id, snapshot_date)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_miraseek_results_task ON miraseek_results(task_id);
CREATE INDEX IF NOT EXISTS idx_miraseek_results_brand ON miraseek_results(brand_id);
CREATE INDEX IF NOT EXISTS idx_miraseek_results_time ON miraseek_results(query_timestamp);
CREATE INDEX IF NOT EXISTS idx_miraseek_alerts_status ON miraseek_alerts(status);
CREATE INDEX IF NOT EXISTS idx_miraseek_tasks_active ON miraseek_tasks(is_active);

-- 插入测试数据
INSERT INTO miraseek_brands (brand_name, industry, core_technicals) 
VALUES ('MiraSeek', 'industrial_automation', ARRAY['重复定位精度', '防护等级', '通讯协议'])
ON CONFLICT DO NOTHING;

INSERT INTO miraseek_tasks (brand_id, prompt_text, ai_models, frequency) 
VALUES (1, '国产工业机器人品牌排名', ARRAY['deepseek', 'kimi'], '1d')
ON CONFLICT DO NOTHING;

-- 启用 Row Level Security (可选)
-- ALTER TABLE miraseek_brands ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE miraseek_tasks ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE miraseek_results ENABLE ROW LEVEL SECURITY;

-- 完成
SELECT 'MiraSeek tables created successfully!' as message;
