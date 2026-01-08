import os
import traceback

def merge_rules():
    try:
        rules_dir = r"e:\AI测试用例\.trae\rules"
        output_file = os.path.join(rules_dir, "project_rules.md")
        
        print(f"📂 规则目录: {rules_dir}")
        print(f"📄 输出文件: {output_file}")
        
        # 定义合并顺序
        rule_files = [
            "身份定义.md",
            "错题本规则.md",
            "6A工作流.md",
            "交互约定.md",
            "OPML规范.md",
            "Markdown规范.md",
            "jmeter_plugin_rules.md",
            "文件修改规则.md"  # 新增：文件修改规则
        ]
        
        # 读取并合并所有规则文件
        merged_content = ""
        
        for rule_file in rule_files:
            file_path = os.path.join(rules_dir, rule_file)
            
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        merged_content += content + "\n\n"
                        print(f"✅ 已合并: {rule_file}")
                except Exception as e:
                    print(f"❌ 读取文件失败 {rule_file}: {e}")
            else:
                print(f"⚠️  文件不存在: {rule_file}")
        
        # 写入到 project_rules.md
        print(f"📝 开始写入文件...")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(merged_content)
        
        print(f"\n🎉 合并完成！已生成 {output_file}")
        print(f"📊 合并内容长度: {len(merged_content)} 字符")
        
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    merge_rules()
