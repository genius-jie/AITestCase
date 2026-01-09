Patchx AIserver小精灵服务端
小精灵Redis账号

| JSON
Redis:
host: "redis-shzles67xmx2vg9oz.redis.volces.com"
port: 6379
username: zhanglijie
password: "patchx_dev_redis%$$1"
db: 0 |
| --- |

小精灵用户关联清除Key
小精灵user_id：3c:0f:02:db:bf:5c
查询脚本

| Markdown
# 连接 Redis（替换为实际的 host/port/password）
redis-cli -h <host> -p 6379 -a <password>

# 查询所有相关 Key（通配符匹配）
KEYS *3c:0f:02:db:bf:5c*

# 逐个查看具体值
# Hash 类型
HGETALL sprite:config:3c:0f:02:db:bf:5c
HGETALL sprite:session:summary:3c:0f:02:db:bf:5c

# List 类型
LRANGE sprite:history:raw:3c:0f:02:db:bf:5c 0 -1

# String 类型
GET sprite:lock:summary:3c:0f:02:db:bf:5c
GET sprite:user:memory:3c:0f:02:db:bf:5c
GET persona:3c:0f:02:db:bf:5c
GET persona:queued:3c:0f:02:db:bf:5c

# 洞察相关（需要指定 category，如 hobbies、preferences 等）
KEYS insight:3c:0f:02:db:bf:5c:*
KEYS insight:queued:3c:0f:02:db:bf:5c:* |
| --- |

删除脚本

| Markdown
# 方法1：先查出所有 key，再批量删除
redis-cli -h <host> -p 6379 -a <password> KEYS "*3c:0f:02:db:bf:5c*" | xargs redis-cli -h <host> -p 6379 -a <password> DEL

# 方法2：逐个删除（更安全）
DEL sprite:config:3c:0f:02:db:bf:5c
DEL sprite:history:raw:3c:0f:02:db:bf:5c
DEL sprite:session:summary:3c:0f:02:db:bf:5c
DEL sprite:lock:summary:3c:0f:02:db:bf:5c
DEL sprite:user:memory:3c:0f:02:db:bf:5c
DEL persona:3c:0f:02:db:bf:5c
DEL persona:queued:3c:0f:02:db:bf:5c

# 洞察相关需要通配符删除（在 redis-cli 中）
EVAL "return redis.call('del', unpack(redis.call('keys', 'insight:3c:0f:02:db:bf:5c:*')))" 0
EVAL "return redis.call('del', unpack(redis.call('keys', 'insight:queued:3c:0f:02:db:bf:5c:*')))" 0 |
| --- |

一键脚本

| Bash
#!/bin/bash
# 删除指定用户的所有 Redis 数据
USER_ID="3c:0f:02:db:bf:5c"
REDIS_HOST="your-redis-host"
REDIS_PORT="6379"
REDIS_PASS="your-password"

# 查询
echo "=== 查询 Key ==="
redis-cli -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASS KEYS "*$USER_ID*"

# 删除（取消注释执行）
# echo "=== 删除 Key ==="
# redis-cli -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASS KEYS "*$USER_ID*" | xargs redis-cli -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASS DEL |
| --- |

对话历史（若有 sprite:history:raw）

| JSON
Key: sprite:history:raw:{user_id}
Type: List
TTL: 7天
保留: 最后 50 条

Value (JSON):
{
  "role": "user|assistant",
  "content": "消息内容",
  "ts": 1700000001
} |
| --- |

摘要状态（若有sprite:session:summary）

| JSON
Key: sprite:session:summary:{user_id}
Type: Hash
TTL: 24小时

Fields:
├── status: generating | completed | failed
├── content: 摘要内容
├── has_pending: 0 | 1
├── pending_content: 待应用的摘要内容
├── pending_index: 待应用的摘要索引
├── summary_index: 当前摘要索引
├── message_count: 消息总数
├── trigger_type: 触发类型
└── generated_at: Unix 时间戳 |
| --- |

用户偏好（若有sprite:user:memory）

| JSON
Key: sprite:user:memory:{user_id}
Type: String
TTL: 24小时

Value (String):
{
  "meta_info": {
    "user_id": "", 
    "update_timestamp": "",
    "session_status": "NEW_USER",
    "interaction_count": 0
  },
  "identity_core": {
    "nickname": "新朋友",
    "persona_tags": [],
    "personality_vibe": "尚无足够数据。待观察。",
    "emotional_needs": "待探索。"
  },
  "social_graph": {
    "real_world": [],
    "virtual_world": []
  },
  "preferences_matrix": {
    "likes": {
      "food": [],
      "content": [],
      "style": []
    },
    "dislikes": {
      "food": [],
      "topic": [],
      "behavior": [],
      "vocabulary": []
    }
  },
  "interaction_strategy": {
    "communication_style": "适度高冷。保持'搭子'的边界感，拒绝自来熟。先以观察者视角互动，根据用户的有趣程度动态调整热情值。",
    "correction_log": [],
    "active_hooks": []
  },
  "dynamic_context": {
    "gossip_entities": [],
    "current_life_focus": "正在互相认识阶段。",
    "event_timeline": [],
    "last_session_meta": {
      "last_topic": "",
      "last_sentiment": "平静"
    }
  }
} |
| --- |


小精灵PostgreSQL账号

| YAML

PostgreSQL:
host: "postgres-460bae9aa91b-public.rds-pg.volces.com"
port: 5432
user: "zhanglijie"
password: "MdXMPkaAwsJavi8q"
database: "patchx_emomo" |
| --- |

小精灵用户关联表
小精灵user_id：3c:0f:02:db:bf:5c
表关系

| JSON
用户记忆体系
├── user_memories          (短期/偏好记忆，每用户一条)
├── user_long_memories     (长期记忆，每用户多条，按category分类)
├── user_long_profile_insights (分类洞察，每用户+category唯一)
└── user_long_personas     (整合画像，每用户一条) |
| --- |

查询删除脚本

| Bash
#!/bin/bash
# PostgreSQL 查询/删除指定用户数据脚本

# 配置（替换为实际值）
PG_HOST="postgres460bae9aa91b.rds-pg.ivolces.com"
PG_PORT="5432"
PG_USER="your_username"
PG_PASS="your_password"
PG_DB="patchx_emomo"
USER_ID="3c:0f:02:db:bf:5c"

# 设置密码环境变量（避免交互输入）
export PGPASSWORD="$PG_PASS"

# ==================== 查询 ====================
echo "=== 查询 user_memories ==="
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c \
  "SELECT * FROM public.user_memories WHERE user_id = '$USER_ID';"

echo "=== 查询 user_long_memories ==="
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c \
  "SELECT id, memory_uuid, user_id, category, LEFT(memory_content, 50) as content_preview, created_at FROM public.user_long_memories WHERE user_id = '$USER_ID';"

echo "=== 查询 user_long_profile_insights ==="
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c \
  "SELECT * FROM public.user_long_profile_insights WHERE user_id = '$USER_ID';"

echo "=== 查询 user_long_personas ==="
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c \
  "SELECT * FROM public.user_long_personas WHERE user_id = '$USER_ID';"

# ==================== 统计 ====================
echo "=== 统计各表记录数 ==="
psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
SELECT 'user_memories' as table_name, COUNT(*) as count FROM public.user_memories WHERE user_id = '$USER_ID'
UNION ALL
SELECT 'user_long_memories', COUNT(*) FROM public.user_long_memories WHERE user_id = '$USER_ID'
UNION ALL
SELECT 'user_long_profile_insights', COUNT(*) FROM public.user_long_profile_insights WHERE user_id = '$USER_ID'
UNION ALL
SELECT 'user_long_personas', COUNT(*) FROM public.user_long_personas WHERE user_id = '$USER_ID';
"

# ==================== 删除（取消注释执行） ====================
# echo "=== 删除数据 ==="
# psql -h $PG_HOST -p $PG_PORT -U $PG_USER -d $PG_DB -c "
# BEGIN;
# DELETE FROM public.user_memories WHERE user_id = '$USER_ID';
# DELETE FROM public.user_long_memories WHERE user_id = '$USER_ID';
# DELETE FROM public.user_long_profile_insights WHERE user_id = '$USER_ID';
# DELETE FROM public.user_long_personas WHERE user_id = '$USER_ID';
# COMMIT;
# "
# echo "=== 删除完成 ==="

unset PGPASSWORD |
| --- |

一键脚本

| JSON
# 查询统计
PGPASSWORD='your_password' psql -h postgres460bae9aa91b.rds-pg.ivolces.com -U your_username -d patchx_emomo -c "
SELECT 'user_memories' as tbl, COUNT(*) FROM public.user_memories WHERE user_id = '3c:0f:02:db:bf:5c'
UNION ALL SELECT 'user_long_memories', COUNT(*) FROM public.user_long_memories WHERE user_id = '3c:0f:02:db:bf:5c'
UNION ALL SELECT 'user_long_profile_insights', COUNT(*) FROM public.user_long_profile_insights WHERE user_id = '3c:0f:02:db:bf:5c'
UNION ALL SELECT 'user_long_personas', COUNT(*) FROM public.user_long_personas WHERE user_id = '3c:0f:02:db:bf:5c';
"

# 删除（谨慎执行）
PGPASSWORD='your_password' psql -h postgres460bae9aa91b.rds-pg.ivolces.com -U your_username -d patchx_emomo -c "
DELETE FROM public.user_memories WHERE user_id = '3c:0f:02:db:bf:5c';
DELETE FROM public.user_long_memories WHERE user_id = '3c:0f:02:db:bf:5c';
DELETE FROM public.user_long_profile_insights WHERE user_id = '3c:0f:02:db:bf:5c';
DELETE FROM public.user_long_personas WHERE user_id = '3c:0f:02:db:bf:5c';
" |
| --- |

用户偏好表（user_memories）

| JSON
用途: 存储用户的文本记忆数据（短期/偏好记忆）

id
SERIALPRIMARY KEY主键ID
user_id
VARCHAR(255)NOT NULL UNIQUE用户唯一标识符
memory_data
TEXTNOT NULL文本格式的记忆数据
updated_at
TIMESTAMPTZNOT NULL DEFAULT now()最后更新时间
created_at
TIMESTAMPTZNOT NULL DEFAULT now()创建时间
metadata
JSONBDEFAULT '{}'扩展元数据 |
| --- |

用户长期记忆表（user_long_memories）

| JSON
用途: LLM抽取→embedding→去重/合并→存入的长期记忆

id
BIGSERIALPRIMARY KEY主键ID
memory_uuid
UUIDNOT NULL UNIQUE应用侧生成的UUID（用于外部追踪）
user_id
VARCHAR(255)NOT NULL用户ID
device_id
VARCHAR(255)NOT NULL设备ID
session_id
VARCHAR(255)会话ID
category
TEXTNOT NULL记忆分类
memory_content
TEXTNOT NULL记忆文本内容
embedding
vector(768)归一化后的文本向量（pgvector）
metadata
JSONBDEFAULT '{}'附加元数据（llm_model、prompt_version等）
source_history
JSONBDEFAULT '[]'本轮用户+助手的原始对话片段
mcp_info
JSONBDEFAULT '{}'本轮是否触发MCP工具与工具明细
created_at
TIMESTAMPTZNOT NULL DEFAULT now()创建时间
updated_at
TIMESTAMPTZNOT NULL DEFAULT now()更新时间 |
| --- |

用户长期分类记忆总结表（user_long_profile_insights）

| JSON
唯一约束: UNIQUE (user_id, category)- 每个用户每个分类只有一条洞察
用途: 按分类生成的用户画像总结洞察

id
BIGSERIALPRIMARY KEY主键ID
user_id
TEXTNOT NULL用户ID
category
TEXTNOT NULL洞察分类
insight_content
TEXTNOT NULL洞察内容
source_memory_uuids
JSONBDEFAULT '[]'用于生成本次洞察的记忆UUID数组
metadata
JSONBDEFAULT '{}'元数据（模型/版本/条数/时延/tokens等）
created_at
TIMESTAMPTZNOT NULL DEFAULT now()创建时间
updated_at
TIMESTAMPTZNOT NULL DEFAULT now()更新时间
last_updated_at
TIMESTAMPTZNOT NULL DEFAULT now()最后更新时间 |
| --- |

用户长期记忆画像总结表（user_long_personas）

| JSON
用途: 最终的、整合后的完整用户画像（每用户唯一）

user_id
VARCHAR(255)PRIMARY KEY用户ID（主键）
last_used_device_id
VARCHAR(255)最后使用的设备ID
persona_profile
JSONBNOT NULL, CHECK(是object)整合后的完整用户画像JSON对象
schema_version
INTNOT NULL DEFAULT 1画像结构版本号
created_at
TIMESTAMPTZNOT NULL DEFAULT now()创建时间
last_updated_at
TIMESTAMPTZNOT NULL DEFAULT now()最后更新时间 |
| --- |

