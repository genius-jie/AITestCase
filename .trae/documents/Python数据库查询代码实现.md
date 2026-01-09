# Python数据库查询代码实现

## 1. 需求分析
- 连接Redis和PostgreSQL数据库
- 根据user_id='3c:0f:02:db:bf:5c'查询所有相关信息
- 以清晰格式输出，方便分析

## 2. 数据库配置提取
### Redis配置
- 主机: redis-shzles67xmx2vg9oz.redis.volces.com
- 端口: 6379
- 用户名: zhanglijie
- 密码: patchx_dev_redis%$$1
- 数据库: 0

### PostgreSQL配置
- 主机: postgres-460bae9aa91b-public.rds-pg.volces.com
- 端口: 5432
- 用户名: zhanglijie
- 密码: MdXMPkaAwsJavi8q
- 数据库: patchx_emomo

## 3. 实现步骤
1. **导入依赖库**：redis、psycopg2、json
2. **Redis查询功能**：
   - 连接Redis数据库
   - 查询指定user_id的所有key
   - 根据key类型获取对应值
   - 支持通配符查询
3. **PostgreSQL查询功能**：
   - 连接PostgreSQL数据库
   - 查询4张用户相关表：
     - user_memories
     - user_long_memories
     - user_long_profile_insights
     - user_long_personas
4. **结果整合与输出**：
   - 结构化输出Redis数据
   - 结构化输出PostgreSQL数据
   - 格式化输出，方便阅读
5. **异常处理**：
   - 数据库连接异常处理
   - 查询异常处理
   - 资源清理

## 4. 代码结构
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import redis
import psycopg2
import json
from typing import Dict, List, Any

class DatabaseQuery:
    def __init__(self):
        # 初始化数据库连接
        self.redis_client = None
        self.pg_conn = None
        self.pg_cursor = None
    
    def connect_redis(self):
        # 连接Redis
        pass
    
    def connect_postgresql(self):
        # 连接PostgreSQL
        pass
    
    def query_redis_data(self, user_id: str) -> Dict[str, Any]:
        # 查询Redis中的用户数据
        pass
    
    def query_postgresql_data(self, user_id: str) -> Dict[str, List[Dict[str, Any]]]:
        # 查询PostgreSQL中的用户数据
        pass
    
    def run_query(self, user_id: str):
        # 执行完整查询流程
        pass
    
    def close_connections(self):
        # 关闭数据库连接
        pass

if __name__ == "__main__":
    # 主函数
    user_id = "3c:0f:02:db:bf:5c"
    query = DatabaseQuery()
    query.run_query(user_id)
```

## 5. 预期输出
- Redis数据：按key分类输出，包括对话历史、会话摘要、用户偏好等
- PostgreSQL数据：按表分类输出，包括短期记忆、长期记忆、分类洞察、用户画像等
- 所有数据以结构化格式输出，方便后续分析

## 6. 注意事项
- 确保安装必要依赖：`pip install redis psycopg2-binary`
- 处理好密码等敏感信息，建议使用环境变量
- 处理大文本数据时的输出格式
- 确保数据库连接安全关闭