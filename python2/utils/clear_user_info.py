#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户信息清除脚本
功能：一键清除指定用户ID在Redis和PostgreSQL中的所有信息
"""

import redis
import psycopg2
import json
from typing import Dict, List, Any
from datetime import datetime
import os
import argparse
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

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

# 用户信息清除类
class UserInfoClear:
    """用户信息清除工具类"""
    
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
    
    def clear_redis_data(self, user_id: str) -> Dict[str, Any]:
        """清除Redis中的用户数据"""
        print(f"\n📋 开始清除Redis中用户 {user_id} 的数据...")
        
        # 定义要清除的key模式
        known_key_patterns = [
            f"sprite:history:raw:{user_id}",
            f"sprite:session:summary:{user_id}",
            f"sprite:user:memory:{user_id}",
            f"sprite:lock:summary:{user_id}",
            f"persona:{user_id}",
            f"persona:queued:{user_id}",
        ]
        
        deleted_keys = []
        
        # 先删除已知的精确匹配key
        for key_pattern in known_key_patterns:
            try:
                if self.redis_client.exists(key_pattern):
                    self.redis_client.delete(key_pattern)
                    deleted_keys.append(key_pattern)
                    print(f"🗑️  已删除Key: {key_pattern}")
            except Exception as e:
                print(f"⚠️  删除Key {key_pattern} 失败: {e}")
        
        # 使用SCAN命令删除insight相关的key
        try:
            insight_cursor = 0
            while True:
                insight_cursor, keys = self.redis_client.scan(
                    cursor=insight_cursor,
                    match=f"insight:*{user_id}*",
                    count=100
                )
                
                if keys:
                    deleted_count = self.redis_client.delete(*keys)
                    deleted_keys.extend(keys)
                    for key in keys:
                        print(f"🗑️  已删除Key: {key}")
                
                if insight_cursor == 0:
                    break
        except Exception as e:
            print(f"⚠️  删除insight相关Key失败: {e}")
        
        print(f"\n✅ Redis数据清除完成，共删除 {len(deleted_keys)} 个Key")
        return {
            "deleted_keys": deleted_keys,
            "count": len(deleted_keys)
        }
    
    def clear_postgresql_data(self, user_id: str) -> Dict[str, Any]:
        """清除PostgreSQL中的用户数据"""
        print(f"\n📋 开始清除PostgreSQL中用户 {user_id} 的数据...")
        
        deleted_records = {}
        
        # 定义要清除的表和对应的清除语句
        tables = {
            "user_long_profile_insights": "DELETE FROM public.user_long_profile_insights WHERE user_id = %s",
            "user_long_memories": "DELETE FROM public.user_long_memories WHERE user_id = %s",
            "user_memories": "DELETE FROM public.user_memories WHERE user_id = %s",
            "user_long_personas": "DELETE FROM public.user_long_personas WHERE user_id = %s"
        }
        
        try:
            # 开始事务
            self.pg_conn.autocommit = False
            
            for table_name, query in tables.items():
                try:
                    # 先查询记录数
                    self.pg_cursor.execute(f"SELECT COUNT(*) FROM public.{table_name} WHERE user_id = %s", (user_id,))
                    count_before = self.pg_cursor.fetchone()[0]
                    
                    if count_before > 0:
                        # 执行删除
                        self.pg_cursor.execute(query, (user_id,))
                        deleted_count = self.pg_cursor.rowcount
                        deleted_records[table_name] = deleted_count
                        print(f"🗑️  表 {table_name}: 已删除 {deleted_count} 条记录")
                    else:
                        deleted_records[table_name] = 0
                        print(f"ℹ️  表 {table_name}: 无匹配记录")
                except Exception as e:
                    print(f"⚠️  删除表 {table_name} 数据失败: {e}")
                    self.pg_conn.rollback()
                    raise
            
            # 提交事务
            self.pg_conn.commit()
            print(f"\n✅ PostgreSQL数据清除完成")
            
        except Exception as e:
            self.pg_conn.rollback()
            print(f"❌ PostgreSQL数据清除失败，事务已回滚: {e}")
            raise
        finally:
            # 恢复自动提交
            self.pg_conn.autocommit = True
        
        return deleted_records
    
    def save_clear_log(self, user_id: str, redis_result: Dict[str, Any], pg_result: Dict[str, Any]):
        """保存清除日志到文件"""
        # 创建日志目录
        log_dir = "e:\\AI测试用例\\logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # 生成时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 替换user_id中的冒号，因为Windows文件名不允许包含冒号
        safe_user_id = user_id.replace(':', '_')
        
        # 保存日志
        log_file = os.path.join(log_dir, f"clear_log_{safe_user_id}_{timestamp}.json")
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "redis_result": redis_result,
            "postgresql_result": pg_result,
            "total_deleted": redis_result["count"] + sum(pg_result.values())
        }
        
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 清除日志已保存到: {log_file}")
        return log_file
    
    def close_connections(self):
        """关闭数据库连接"""
        if self.pg_cursor:
            self.pg_cursor.close()
        if self.pg_conn:
            self.pg_conn.close()
        if self.redis_client:
            self.redis_client.close()
        print("\n🔌 数据库连接已关闭")
    
    def run_clear(self, user_id: str, confirm: bool = False):
        """执行完整清除流程"""
        print("🚀 开始执行用户信息清除操作")
        print("=" * 60)
        
        # 确认机制
        if not confirm:
            print(f"⚠️  警告：此操作将永久删除用户 {user_id} 的所有数据")
            print(f"⚠️  操作不可恢复，请谨慎执行！")
            user_confirm = input("\n请输入 'YES' 确认执行清除操作：").strip().upper()
            if user_confirm != "YES":
                print("\n✅ 清除操作已取消")
                return
        
        redis_result = {"deleted_keys": [], "count": 0}
        pg_result = {}
        
        try:
            # 连接数据库
            self.connect_redis()
            self.connect_postgresql()
            
            # 执行清除
            redis_result = self.clear_redis_data(user_id)
            pg_result = self.clear_postgresql_data(user_id)
            
            # 保存日志
            self.save_clear_log(user_id, redis_result, pg_result)
            
            # 输出清除结果
            print("\n📊 清除结果统计")
            print("=" * 60)
            print(f"Redis清除：{redis_result['count']} 个Key")
            for table, count in pg_result.items():
                print(f"PostgreSQL-{table}：{count} 条记录")
            print(f"总计清除：{redis_result['count'] + sum(pg_result.values())} 条数据")
            
            print("\n🎉 清除操作完成！")
            return redis_result, pg_result
            
        except Exception as e:
            print(f"\n❌ 清除操作失败: {e}")
            import traceback
            traceback.print_exc()
            raise
        finally:
            # 关闭连接
            self.close_connections()

# 主函数
if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="用户信息清除脚本")
    parser.add_argument("--user-id", type=str, required=True, help="要清除信息的用户ID")
    parser.add_argument("--confirm", action="store_true", help="跳过确认提示，直接执行清除操作")
    
    args = parser.parse_args()
    
    # 创建清除实例
    clearer = UserInfoClear()
    
    # 执行清除
    clearer.run_clear(args.user_id, args.confirm)
