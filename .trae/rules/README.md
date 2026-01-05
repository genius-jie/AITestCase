# 规则文件说明

## 📁 文件结构

```
.trae/rules/
├── project_rules.md     # 主规则文件（Trae 指定的唯一规则文件）
├── identity.md          # 身份定义
├── 错题本规则.md        # 错题本自动调用规则
├── 6A工作流.md          # 测试用例生成工作流
├── 交互约定.md          # 交互规范
├── OPML规范.md          # OPML文件格式规范
└── 错题本.md            # 错题本内容（实际记录）
```

## 🔄 规则更新流程

### 修改规则时：
1. 编辑对应的拆分文件（如 `identity.md`、`6A工作流.md` 等）
2. 运行合并脚本，将所有拆分文件合并到 `project_rules.md`
3. Trae 会自动读取更新后的 `project_rules.md`

### 合并命令：
```bash
# 在 PowerShell 中运行
cd "e:\AI测试用例\.trae\rules"
python merge_rules.py
```

## 📋 拆分文件说明

- **identity.md**: 身份定义和角色定位
- **错题本规则.md**: 错题本自动调用规则
- **6A工作流.md**: 测试用例生成的6个阶段
- **交互约定.md**: 与用户的交互规范
- **OPML规范.md**: OPML文件格式要求
- **错题本.md**: 实际记录的问题和解决方案

## ⚠️ 重要提示

- Trae 只会读取 `project_rules.md`
- 修改拆分文件后，必须运行合并脚本更新 `project_rules.md`
- 不要直接编辑 `project_rules.md`，否则下次合并会被覆盖
