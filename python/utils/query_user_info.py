#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户信息查询脚本
功能：连接Redis和PostgreSQL数据库，查询指定user_id的所有信息并进行分析总结
"""

import redis
import psycopg2
import json
from typing import Dict, List, Any
from datetime import datetime
import os
import argparse

# 配置类
class Config:
    """数据库配置信息"""
    # Redis配置
    # 环境变量名：REDIS_HOST
    REDIS_HOST = os.environ.get("REDIS_HOST", "redis-shzles67xmx2vg9oz.redis.volces.com")
    # 环境变量名：REDIS_PORT
    REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
    # 环境变量名：REDIS_USERNAME
    REDIS_USERNAME = os.environ.get("REDIS_USERNAME", "zhanglijie")
    # 环境变量名：REDIS_PASSWORD
    REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "YOUR_REDIS_PASSWORD")
    # 环境变量名：REDIS_DB
    REDIS_DB = int(os.environ.get("REDIS_DB", "0"))
    
    # PostgreSQL配置
    # 环境变量名：PG_HOST
    PG_HOST = os.environ.get("PG_HOST", "postgres-460bae9aa91b-public.rds-pg.volces.com")
    # 环境变量名：PG_PORT
    PG_PORT = int(os.environ.get("PG_PORT", "5432"))
    # 环境变量名：PG_USER
    PG_USER = os.environ.get("PG_USER", "zhanglijie")
    # 环境变量名：PG_PASSWORD
    PG_PASSWORD = os.environ.get("PG_PASSWORD", "YOUR_PG_PASSWORD")
    # 环境变量名：PG_DATABASE
    PG_DATABASE = os.environ.get("PG_DATABASE", "patchx_emomo")

# 数据库查询类
class DatabaseQuery:
    """数据库查询工具类"""
    
    def __init__(self):
        """初始化数据库连接"""
        self.redis_client = None
        self.pg_conn = None
        self.pg_cursor = None
    
    def connect_redis(self):
        """连接Redis数据库"""
        try:
            self.redis_client = redis.Redis(
                host=Config.REDIS_HOST,
                port=Config.REDIS_PORT,
                username=Config.REDIS_USERNAME,
                password=Config.REDIS_PASSWORD,
                db=Config.REDIS_DB,
                decode_responses=True
            )
            # 测试连接
            self.redis_client.ping()
            print("✅ Redis连接成功")
        except Exception as e:
            print(f"❌ Redis连接失败: {e}")
            raise
    
    def connect_postgresql(self):
        """连接PostgreSQL数据库"""
        try:
            self.pg_conn = psycopg2.connect(
                host=Config.PG_HOST,
                port=Config.PG_PORT,
                user=Config.PG_USER,
                password=Config.PG_PASSWORD,
                database=Config.PG_DATABASE
            )
            self.pg_cursor = self.pg_conn.cursor()
            print("✅ PostgreSQL连接成功")
        except Exception as e:
            print(f"❌ PostgreSQL连接失败: {e}")
            raise
    
    def query_redis_data(self, user_id: str) -> Dict[str, Any]:
        """查询Redis中的用户数据"""
        print(f"\n📋 查询Redis中用户 {user_id} 的数据...")
        redis_data = {}
        
        # 根据文档中已知的key模式直接查询，避免使用KEYS命令
        known_key_patterns = [
            f"sprite:history:raw:{user_id}",
            f"sprite:session:summary:{user_id}",
            f"sprite:user:memory:{user_id}",
            f"sprite:lock:summary:{user_id}",
            f"persona:{user_id}",
            f"persona:queued:{user_id}",
            # 注意：insight相关的key需要特殊处理，因为它们有category后缀
        ]
        
        found_keys = []
        
        # 先检查已知的精确匹配key
        for key_pattern in known_key_patterns:
            try:
                # 检查key是否存在
                if self.redis_client.exists(key_pattern):
                    found_keys.append(key_pattern)
            except Exception as e:
                print(f"⚠️  检查Key {key_pattern} 失败: {e}")
        
        # 处理insight相关的key（使用SCAN命令替代KEYS）
        try:
            # 使用SCAN命令查询insight相关的key
            insight_cursor = 0
            while True:
                insight_cursor, keys = self.redis_client.scan(
                    cursor=insight_cursor,
                    match=f"insight:*{user_id}*",
                    count=100
                )
                found_keys.extend(keys)
                if insight_cursor == 0:
                    break
        except Exception as e:
            print(f"⚠️  查询insight相关Key失败: {e}")
        
        print(f"找到 {len(found_keys)} 个相关Key")
        
        for key in found_keys:
            # 获取key类型
            try:
                key_type = self.redis_client.type(key)
                
                if key_type == "string":
                    # 字符串类型
                    value = self.redis_client.get(key)
                    # 尝试解析JSON
                    try:
                        value = json.loads(value)
                    except:
                        pass
                    redis_data[key] = value
                
                elif key_type == "hash":
                    # Hash类型
                    redis_data[key] = self.redis_client.hgetall(key)
                
                elif key_type == "list":
                    # List类型
                    redis_data[key] = self.redis_client.lrange(key, 0, -1)
                    # 尝试解析每个元素为JSON
                    for i, item in enumerate(redis_data[key]):
                        try:
                            redis_data[key][i] = json.loads(item)
                        except:
                            pass
            except Exception as e:
                print(f"⚠️  读取Key {key} 失败: {e}")
        
        return redis_data
    
    def query_postgresql_data(self, user_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """查询PostgreSQL中的用户数据"""
        print(f"\n📋 查询PostgreSQL中用户 {user_id} 的数据...")
        pg_data = {}
        
        # 定义要查询的表和对应的查询语句
        tables = {
            "user_memories": "SELECT * FROM public.user_memories WHERE user_id = %s",
            "user_long_memories": "SELECT * FROM public.user_long_memories WHERE user_id = %s",
            "user_long_profile_insights": "SELECT * FROM public.user_long_profile_insights WHERE user_id = %s",
            "user_long_personas": "SELECT * FROM public.user_long_personas WHERE user_id = %s"
        }
        
        for table_name, query in tables.items():
            try:
                self.pg_cursor.execute(query, (user_id,))
                rows = self.pg_cursor.fetchall()
                columns = [desc[0] for desc in self.pg_cursor.description]
                
                # 将查询结果转换为字典列表
                table_data = []
                for row in rows:
                    row_dict = {}
                    for i, col in enumerate(columns):
                        value = row[i]
                        # 处理JSONB类型
                        if isinstance(value, (bytes, memoryview)):
                            try:
                                value = json.loads(value.decode('utf-8'))
                            except:
                                value = value.decode('utf-8')
                        row_dict[col] = value
                    table_data.append(row_dict)
                
                pg_data[table_name] = table_data
                print(f"📄 {table_name}: 找到 {len(table_data)} 条记录")
                
            except Exception as e:
                print(f"⚠️  查询表 {table_name} 失败: {e}")
        
        return pg_data
    
    def analyze_data(self, user_id: str, redis_data: Dict[str, Any], pg_data: Dict[str, List[Dict[str, Any]]]):
        """分析查询到的数据"""
        print(f"\n📊 用户 {user_id} 数据分析总结")
        print("=" * 60)
        
        # Redis数据分析
        print("\n1. Redis数据统计:")
        print("-" * 30)
        print(f"   总Key数: {len(redis_data)}")
        
        # 统计各类型key数量
        key_types = {}
        for key in redis_data:
            if isinstance(redis_data[key], dict):
                key_types["hash"] = key_types.get("hash", 0) + 1
            elif isinstance(redis_data[key], list):
                key_types["list"] = key_types.get("list", 0) + 1
            else:
                key_types["string"] = key_types.get("string", 0) + 1
        
        for key_type, count in key_types.items():
            print(f"   {key_type}类型Key数: {count}")
        
        # 显示Redis中的所有Key
        print(f"\n   Redis Key列表:")
        for key in redis_data:
            print(f"   - {key}")
        
        # PostgreSQL数据分析
        print("\n2. PostgreSQL数据统计:")
        print("-" * 30)
        total_records = 0
        for table_name, data in pg_data.items():
            count = len(data)
            total_records += count
            print(f"   {table_name}: {count} 条记录")
        print(f"   总记录数: {total_records}")
        
        # 详细分析
        print("\n3. 详细数据内容:")
        print("-" * 30)
        
        # 检查对话历史
        history_key = f"sprite:history:raw:{user_id}"
        if history_key in redis_data:
            history_items = redis_data[history_key]
            print(f"\n   🔹 对话历史 ({len(history_items)} 条记录):")
            for i, item in enumerate(history_items[:5]):  # 最多显示5条
                if isinstance(item, dict):
                    # 提取关键信息
                    msg_type = item.get("type", "unknown")
                    msg_time = item.get("timestamp", "unknown")
                    msg_content = ""
                    
                    if msg_type == "user" and "text" in item:
                        msg_content = item["text"]
                    elif msg_type == "system" and "text" in item:
                        msg_content = item["text"]
                    elif msg_type == "audio" and "audio_duration" in item:
                        msg_content = f"[音频消息，时长: {item['audio_duration']}s]"
                    elif msg_type == "tts" and "text" in item:
                        msg_content = item["text"]
                    
                    print(f"     {i+1}. [{msg_type}] [{msg_time}] {msg_content[:50]}{'...' if len(str(msg_content)) > 50 else ''}")
                else:
                    print(f"     {i+1}. 未知格式: {str(item)[:50]}...")
            
            if len(history_items) > 5:
                print(f"     ... 还有 {len(history_items) - 5} 条记录未显示")
        
        # 检查用户画像
        persona_key = f"persona:{user_id}"
        if persona_key in redis_data:
            persona = redis_data[persona_key]
            print(f"\n   🔹 用户画像:")
            if isinstance(persona, dict):
                for key, value in persona.items():
                    print(f"     {key}: {value}")
            else:
                print(f"     {persona}")
        
        # 检查会话摘要
        session_key = f"sprite:session:summary:{user_id}"
        if session_key in redis_data:
            session = redis_data[session_key]
            print(f"\n   🔹 会话摘要:")
            if isinstance(session, dict):
                for key, value in session.items():
                    print(f"     {key}: {value}")
            else:
                print(f"     {session}")
        
        # 检查用户记忆
        if pg_data.get("user_memories") and pg_data["user_memories"]:
            memories = pg_data["user_memories"]
            print(f"\n   🔹 用户短期记忆 ({len(memories)} 条):")
            for i, memory in enumerate(memories):
                print(f"     {i+1}. 记忆内容: {memory.get('memory_content', 'N/A')}")
                print(f"        创建时间: {memory.get('created_at', 'N/A')}")
                print(f"        更新时间: {memory.get('updated_at', 'N/A')}")
                print(f"        类型: {memory.get('memory_type', 'N/A')}")
        
        if pg_data.get("user_long_memories") and pg_data["user_long_memories"]:
            long_memories = pg_data["user_long_memories"]
            print(f"\n   🔹 用户长期记忆 ({len(long_memories)} 条):")
            for i, memory in enumerate(long_memories):
                print(f"     {i+1}. 记忆内容: {memory.get('content', 'N/A')[:100]}{'...' if len(str(memory.get('content', ''))) > 100 else ''}")
                print(f"        分类: {memory.get('category', 'unknown')}")
                print(f"        创建时间: {memory.get('created_at', 'N/A')}")
        
        if pg_data.get("user_long_profile_insights") and pg_data["user_long_profile_insights"]:
            insights = pg_data["user_long_profile_insights"]
            print(f"\n   🔹 用户分类洞察 ({len(insights)} 条):")
            for i, insight in enumerate(insights):
                print(f"     {i+1}. 洞察内容: {insight.get('insight_content', 'N/A')}")
                print(f"        类型: {insight.get('insight_type', 'unknown')}")
                print(f"        创建时间: {insight.get('created_at', 'N/A')}")
        
        if pg_data.get("user_long_personas") and pg_data["user_long_personas"]:
            personas = pg_data["user_long_personas"]
            print(f"\n   🔹 完整用户画像 ({len(personas)} 条):")
            for i, persona in enumerate(personas):
                print(f"     {i+1}. 画像类型: {persona.get('persona_type', 'unknown')}")
                print(f"        画像内容: {persona.get('persona_content', 'N/A')[:100]}{'...' if len(str(persona.get('persona_content', ''))) > 100 else ''}")
                print(f"        创建时间: {persona.get('created_at', 'N/A')}")
        
        print("\n📝 分析完成")
        print("=" * 60)
    
    def _json_serializer(self, obj):
        """自定义JSON序列化器，处理datetime类型"""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
    
    def save_results(self, user_id: str, redis_data: Dict[str, Any], pg_data: Dict[str, List[Dict[str, Any]]]):
        """保存查询结果到文件"""
        # 创建结果目录 - 使用双反斜杠确保Windows路径正确
        result_dir = "e:\\AI测试用例\\results"
        os.makedirs(result_dir, exist_ok=True)
        
        # 生成时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 替换user_id中的冒号，因为Windows文件名不允许包含冒号
        safe_user_id = user_id.replace(':', '_')
        
        # 保存Redis数据
        redis_file = os.path.join(result_dir, f"redis_data_{safe_user_id}_{timestamp}.json")
        with open(redis_file, 'w', encoding='utf-8') as f:
            json.dump(redis_data, f, ensure_ascii=False, indent=2, default=self._json_serializer)
        print(f"\n💾 Redis数据已保存到: {redis_file}")
        
        # 保存PostgreSQL数据
        pg_file = os.path.join(result_dir, f"pg_data_{safe_user_id}_{timestamp}.json")
        with open(pg_file, 'w', encoding='utf-8') as f:
            json.dump(pg_data, f, ensure_ascii=False, indent=2, default=self._json_serializer)
        print(f"💾 PostgreSQL数据已保存到: {pg_file}")
        
        return redis_file, pg_file
    
    def close_connections(self):
        """关闭数据库连接"""
        if self.pg_cursor:
            self.pg_cursor.close()
        if self.pg_conn:
            self.pg_conn.close()
        if self.redis_client:
            self.redis_client.close()
        print("\n🔌 数据库连接已关闭")
    
    def run_query(self, user_id: str):
        """执行完整查询流程"""
        print("🚀 开始执行用户信息查询")
        print("=" * 60)
        
        # 清理历史结果目录
        print("\n🧹 清理历史结果目录...")
        result_dir = "e:\\AI测试用例\\results"
        if os.path.exists(result_dir):
            for file in os.listdir(result_dir):
                file_path = os.path.join(result_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"   删除文件: {file_path}")
                    elif os.path.isdir(file_path):
                        # 如果有子目录，递归删除
                        import shutil
                        shutil.rmtree(file_path)
                        print(f"   删除目录: {file_path}")
                except Exception as e:
                    print(f"   删除 {file_path} 失败: {e}")
        else:
            # 如果目录不存在，创建它
            os.makedirs(result_dir, exist_ok=True)
            print(f"   创建结果目录: {result_dir}")
        
        print("   清理完成")
        
        redis_data = {}
        pg_data = {}
        
        try:
            # 连接数据库
            self.connect_redis()
            self.connect_postgresql()
            
            # 查询数据
            redis_data = self.query_redis_data(user_id)
            pg_data = self.query_postgresql_data(user_id)
            
            # 分析数据
            self.analyze_data(user_id, redis_data, pg_data)
            
            # 保存结果
            self.save_results(user_id, redis_data, pg_data)
            
        except Exception as e:
            print(f"\n❌ 查询执行失败: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # 关闭连接
            self.close_connections()

# 主函数
if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='用户信息查询脚本')
    parser.add_argument('user_id', type=str, nargs='?', default='3c:0f:02:db:bf:5c', 
                       help='要查询的用户ID，默认值: 3c:0f:02:db:bf:5c')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 创建查询实例
    query = DatabaseQuery()
    
    # 执行查询
    query.run_query(args.user_id)
