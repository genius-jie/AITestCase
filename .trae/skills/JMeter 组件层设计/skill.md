@skill_name: JMeter 组件层设计
@skill_level: L2
@skill_type: 组件设计
@domain: 接口测试 / JMeter / 性能测试
@input_contract:
  - 接口定义文档: ${resources_dir}/docs/接口定义.md
  - 测试类型: ${test_type}
  - 环境配置: ${env_config}
  - 数据策略: ${data_strategy}
  - 错题本参考: ${mistakes_ref}
@output_artifact:
  - jmx_skeleton: ${resources_dir}/scripts/jmx_skeleton.jmx
  - component_templates: ${resources_dir}/templates/components/
  - assertion_config: ${resources_dir}/config/assertion_config.yaml
  - extraction_rules: ${resources_dir}/config/extraction_rules.yaml
  - component_assets: ${resources_dir}/assets/components/
  - validation_report: ${resources_dir}/reports/validation_report.json
@enforcement: 必须遵循JMeter组件规范，保证GUI与CLI兼容
@on_missing_input: 返回错误，要求提供完整接口定义或测试类型

---

# Skill 目标
- 为JMeter测试提供标准化的组件层设计能力
- 支持生成符合规范的JMX骨架和公共组件
- 确保GUI模式与CLI模式兼容
- 提供可复用的组件资产
- 支持基于错题本的闭环优化
- 保证组件配置的一致性和可维护性
- 输出可直接使用的组件资产

# 输入说明
- **接口定义文档**：接口路径、方法、参数、响应结构
- **测试类型**：function | performance
- **环境配置**：dev/test/prod环境信息
- **数据策略**：CSV使用决策、动态参数策略
- **错题本参考**（可选）：历史错误和优化建议
- **业务规则**（可选）：特殊业务约束和规则

# 输出说明
- **jmx_skeleton.jmx**：标准JMX脚本骨架，包含完整组件结构
- **component_templates**：可复用的组件模板库，保存到A5阶段的组件层资产/组件库目录
- **assertion_config.yaml**：断言配置规则,保存到A5阶段的组件层资产/断言配置目录
- **extraction_rules.yaml**：变量提取规则，保存到A5阶段的组件层资产/变量提取目录
- **component_assets**：可直接使用的组件资产，保存到A5阶段的组件层资产/组件资产目录
- **validation_report.json**：组件验证报告，保存到A5阶段的组件层资产/验证报告目录
- **闭环优化反馈**（可选）：基于错题本的优化建议

## 输出格式示例

### JMX骨架结构
```xml
<jmeterTestPlan>
  <hashTree>
    <TestPlan>
      <!-- 用户定义变量 -->
    </TestPlan>
    <hashTree>
      <ThreadGroup>
        <!-- 线程组配置 -->
      </ThreadGroup>
      <hashTree>
        <ConfigTestElement>
          <!-- HTTP Request Defaults -->
        </ConfigTestElement>
        <!-- 其他组件 -->
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

### 组件模板示例
```yaml
# HTTP Request Defaults 模板
http_request_defaults:
  name: "HTTP 请求默认值"
  server: "${base_url}"
  port: "${port}"
  protocol: "${protocol}"
  contentEncoding: "UTF-8"
```

# 执行约束
- 严格遵循JMeter组件语法规范
- 保证GUI与CLI模式兼容
- 公共组件集中管理，避免重复配置
- 组件配置必须可追溯、可复用
- 闭环优化必须**用户驱动**，Agent 不得自动执行
- 输入缺失或格式错误 → 返回错误，不执行生成
- 严格执行已批准的数据策略，不得自行决策
- 生成的组件配置必须符合A5三件套规范

# 核心功能

## 1. JMX 骨架生成
- **标准组件顺序**：Test Plan → 用户定义变量 → Thread Group → HTTP Request Defaults → CSV Data Set Config → JSR223 PreProcessor → 登录接口 → 全局请求头管理器 → 后续接口
- **环境变量配置**：支持动态环境切换（dev/test/prod）
- **测试类型适配**：根据function/performance生成对应配置
- **GUI兼容性**：确保所有组件使用正确的guiclass属性
- **测试类型前置声明**：强制声明test_type = function | performance

## 2. 公共组件配置
- **HTTP Request Defaults**：集中管理服务器配置、全局请求头
- **CSV Data Set Config**：根据数据策略配置数据源
- **JSR223组件**：动态参数生成、变量提取、断言（使用guiclass="TestBeanGUI"）
- **请求头管理**：登录前/登录后差异化配置
- **文件上传配置**：标准Files Upload配置模板（DO_MULTIPART_POST=true）
- **配置优先级管理**：单个请求的配置 > HTTP Request Defaults > Test Plan级别配置

## 3. 组件资产库
- **通用组件**：HTTP请求、JSR223组件、断言、监听器
- **专用组件**：文件上传、WebSocket、数据库
- **配置模板**：环境变量、全局请求头、服务器配置
- **最佳实践**：基于错题本的组件配置最佳实践
- **版本兼容**：支持多个JMeter版本的组件定义

## 4. 闭环优化能力

### 触发条件
- 组件配置存在GUI兼容性问题
- JSON字段提取路径错误
- 公共组件配置冗余
- 组件层次结构不合理
- 版本兼容性问题
- 业务规则变更影响

### 更新流程
1. **检测阶段**：分析组件配置，识别需要优化的内容
2. **提示阶段**：向用户展示需要优化的具体内容和建议
3. **确认阶段**：等待用户明确的优化确认指令
4. **执行阶段**：根据用户指令执行组件优化
5. **验证阶段**：验证优化后的组件配置格式正确、功能完整
6. **反馈阶段**：向用户反馈优化结果及组件状态

### 更新规则
- **禁止自动更新**：Agent 不得自动执行优化操作
- **用户驱动**：优化必须由用户明确触发或确认
- **可追溯性**：优化过程需记录变更历史
- **状态反馈**：优化完成后提供详细的状态报告

### 变更历史记录
```yaml
change_history:
  - timestamp: <时间戳>
    change_type: <优化类型>
    changed_components:
      - <组件名称>
    changes:
      - <变更内容>
    requested_by: user
    executed_by: agent
    validation_result: <验证结果>
```

### 反馈机制
- 优化成功：返回优化后的组件配置、变更内容摘要
- 优化失败：返回失败原因、错误信息、回退建议
- 部分优化：返回成功优化的部分和失败的部分

## 5. 兼容性保证
- **GUI模式兼容**：确保所有组件可在JMeter GUI中正常打开
- **CLI模式兼容**：确保组件配置在命令行模式下正常执行
- **版本兼容性**：支持JMeter 5.0+版本
- **结构验证**：生成的JMX文件结构完整、格式正确
- **双重验证**：先在非GUI模式验证，再在GUI模式打开

## 6. 验证机制
- **XML结构验证**：确保XML格式良好，元素嵌套正确
- **组件参数验证**：验证组件参数符合JMeter规范
- **版本兼容性验证**：测试多个JMeter版本的兼容性
- **执行验证**：运行基本执行测试，确保组件正常工作
- **依赖关系验证**：验证组件间依赖关系正确

## 7. 错误处理能力
- **配置错误处理**：提供详细的错误信息和修复建议
- **生成错误处理**：捕获XML生成错误并提供具体位置
- **验证错误处理**：分析验证失败原因并提供解决方案
- **有限自愈能力**：单阶段重试 ≤3次，超过阈值请求人工介入

# 执行流程
1. **分析输入**：接口定义、测试类型、环境配置
2. **测试类型声明**：强制声明test_type = function | performance
3. **生成骨架**：创建标准JMX脚本结构
4. **配置组件**：根据测试类型和数据策略配置组件
5. **资产生成**：创建可复用的组件模板和资产
6. **优化分析**：基于错题本分析优化空间
7. **兼容性验证**：确保GUI与CLI模式兼容
8. **输出交付**：生成可直接使用的组件资产和验证报告

# 失败处理

## 配置错误
- 接口定义缺失 → 返回错误并提示补充
- 测试类型未指定 → 返回错误并要求指定测试类型
- 环境配置无效 → 返回错误并提供修复建议
- 数据策略冲突 → 返回错误并提示调整

## 生成错误
- XML结构错误 → 返回错误并提供具体位置
- 组件参数错误 → 返回错误并建议正确值
- GUI兼容性问题 → 返回错误并提示修复guiclass属性
- 版本兼容性错误 → 返回错误并建议版本调整

## 优化错误
- 错题本分析失败 → 返回错误并提示检查错题本格式
- 优化执行失败 → 返回错误并提供回退建议
- 验证失败 → 返回错误并提示具体验证失败原因
- 部分优化成功 → 返回成功和失败的详细信息

# 最佳实践

## 组件设计最佳实践
- **HTTP Request Defaults集中管理**：服务器配置、全局请求头统一管理
- **JSR223组件配置**：使用guiclass="TestBeanGUI"确保GUI兼容性
- **请求头管理策略**：登录前只设置Content-Type，登录后使用全局HeaderManager
- **文件上传配置**：必须放在Files Upload中，设置DO_MULTIPART_POST=true
- **组件命名规范**：使用清晰、描述性的组件名称
- **配置优先级遵循**：单个请求的配置 > HTTP Request Defaults > Test Plan级别配置

## XML生成最佳实践
- **正确的XML结构**：确保元素嵌套正确，属性格式规范
- **变量使用**：避免硬编码，使用${变量名}格式
- **特殊字符处理**：使用XML实体处理特殊字符
- **缩进格式**：保持一致的缩进，提高可读性

## 验证最佳实践
- **双重验证**：先在非GUI模式验证，再在GUI模式打开
- **版本测试**：使用多个JMeter版本测试兼容性
- **结构检查**：验证JMX文件结构完整性
- **执行测试**：运行基本执行测试，确保组件正常工作

## 闭环优化最佳实践
- **错题本分析**：定期分析错题本，提取优化模式
- **用户驱动**：所有优化操作必须获得用户确认
- **变更记录**：详细记录所有优化变更
- **验证反馈**：优化后提供完整的验证报告

## 资产管理最佳实践
- **组件分类**：按功能和类型分类管理组件
- **版本控制**：为组件资产添加版本信息
- **使用说明**：为每个组件提供详细的使用说明
- **依赖管理**：记录组件间的依赖关系

# 参考规范

## A5三件套参考
- **mistakes.md**：基于历史错误和优化建议进行组件配置
- **role.prompt.md**：参考核心能力和行为准则
- **workflow.md**：遵循阶段化执行和宪法级约束

## 关键参考点
1. **GUI兼容性**：JSR223组件必须使用guiclass="TestBeanGUI"
2. **JSON字段提取**：基于实际响应体结构动态推理正确的字段访问路径
3. **公共组件配置**：使用HTTP Request Defaults集中管理
4. **测试类型前置**：强制声明test_type = function | performance
5. **数据策略执行**：严格执行已批准的数据策略，不得自行决策
6. **有限自愈**：单阶段重试 ≤3次，超过阈值请求人工介入
7. **Baseline样本**：基于真实成功响应分析和设计