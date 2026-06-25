# QA Strategy: 车辆监控平台 API 接口自动化测试
## Version 1.0 | Last Updated: 2026-06-14 | Owner: QA Team

---

### 1. Executive Summary

本策略服务于某物联网车辆监控平台的 API 后端测试。平台核心业务包括车辆轨迹查询、报警管理、订单支付和用户管理。当前已有一套基于 pytest + YAML 数据驱动的接口自动化测试框架，覆盖了主要业务模块的单接口和场景测试。策略目标是在未来两个季度内：将关键接口覆盖率提升至 100%、建立测试数据管理规范、引入 Git 版本控制、并实现 CI 流水线的自动化触发。

---

### 2. Scope & Objectives

**In scope:**
- 所有 RESTful API 端点的功能正确性验证
- 接口间参数依赖和业务场景串联测试
- 数据库断言（MySQL、ClickHouse、Redis）
- 认证与授权流程（Token + Cookie）
- 测试报告生成与通知（Allure + 钉钉）

**Out of scope:**
- 前端 UI 测试（本项目为纯 API 测试框架）
- 性能/压力测试（当前框架不支持，后续可引入 k6 或 locust）
- 安全测试（OWASP 扫描由安全团队另行负责）
- 第三方服务的真实调用（以 Mock 或合同测试代替）

**Objectives:**

| # | 目标 | 当前状态 | 目标时间 |
|---|------|---------|---------|
| 1 | 7 大关键业务场景 API 覆盖率达到 100% | 约 70%，缺订单支付全链路和部分报警场景 | Q3 2026 |
| 2 | 消除 extract.yaml 中硬编码的 token/cookie | 全部硬编码，需手动替换 | Q2 2026 |
| 3 | CI 流水线实现代码推送自动触发 | 仅手动执行 run.py | Q3 2026 |
| 4 | 引入 Git 版本管理 | 无 | Q2 2026 |
| 5 | 测试数据清理机制恢复并自动化 | 数据清理代码被注释 | Q2 2026 |
| 6 | 建立框架代码自身的单元测试 | 无 | Q3 2026 |

---

### 3. Test Levels & Types

由于本项目是 **API 测试框架**（非传统全栈应用），测试层级定义与传统金字塔有所不同：

| Level | What It Validates | Owner | Framework | Current Count | Target Count |
|-------|-------------------|-------|-----------|---------------|-------------|
| **框架单元测试** | base/apiutil.py、common/ 中的核心逻辑 | QA | pytest | 0 | 15+ |
| **单接口测试** | 单个 API 的功能正确性、参数校验、错误码 | QA | pytest + YAML | ~20 cases | 覆盖全部端点 |
| **业务场景测试** | 多接口串联的完整业务流程 | QA | pytest + YAML | ~5 scenarios | 10+ scenarios |
| **数据库验证** | SQL 断言验证数据写入正确性 | QA | pytest + YAML (db 断言) | 少量 | 关键写操作全覆盖 |
| **YAML 测试数据** | 数据驱动：CSV/Excel 批量参数化 | QA | YAML + CSV + Excel | 4 个数据文件 | 按需扩展 |

**"测试金字塔"在此项目中的理解：**

```
       /  业务场景测试  \        ← 少而精：核心全链路场景（登录→下单→支付→查订单）
      /   ~15%           \
     /   单接口测试        \      ← 主体：每个 API 端点的功能验证
    /    ~70%              \
   +-----------------------+
   |  框架自身单元测试 ~15% |      ← 新补充：核心函数逻辑验证
   +-----------------------+
```

---

### 4. Test Pyramid Analysis

**Current state:**

| 层级 | 数量 | 占比 |
|------|------|------|
| 框架单元测试 | 0 | 0% |
| 单接口测试 | ~20 | 80% |
| 业务场景测试 | ~5 | 20% |

**当前形状：倒金字塔（缺失底层）** — 框架核心代码（`base/apiutil.py` 中 200+ 行的 `specification_yaml`、`replace_load`、`extract_data` 方法）没有任何单元测试保护。

**Target state:**

| 层级 | 数量 | 占比 |
|------|------|------|
| 框架单元测试 | 15+ | 15% |
| 单接口测试 | 40+ | 70% |
| 业务场景测试 | 10+ | 15% |

**Action plan:**
1. **补充框架单元测试** — 优先覆盖 `replace_load()`（YAML 动态表达式替换）、`extract_data()`（jsonpath/正则提取）、断言模块
2. **补齐缺失的单接口用例** — 按风险矩阵优先级，先覆盖订单支付和报警模块
3. **扩展业务场景** — 登录→创建订单→支付→查询订单 的完整链路

---

### 5. Risk Assessment

基于 `.agents/qa-project-context.md` 中已识别的风险，加上 Impact × Likelihood 评分：

| # | Feature Area | Impact (1-5) | Likelihood (1-5) | Score | Level | Testing Approach |
|---|-------------|-------------|-------------------|-------|-------|-----------------|
| 1 | 登录认证失效（token/cookie 过期） | 5 | 4 | **20 CRIT** | 自动刷新 token 机制 + 登录前置 fixture 监控 |
| 2 | 接口参数依赖链（extract 提取错误） | 5 | 3 | **15 CRIT** | 每个 extract 添加空值校验 + 失败即停 |
| 3 | 订单支付流程 | 5 | 3 | **15 CRIT** | 全链路场景测试 + 数据库断言验证金额 |
| 4 | 车辆轨迹查询（核心业务） | 4 | 3 | **12 HIGH** | 参数化多车牌 + 多时间段组合 |
| 5 | 车辆报警管理 | 4 | 3 | **12 HIGH** | 覆盖全部 alarmType（围栏/疲劳/区域） |
| 6 | 数据库断言失效（连接波动） | 4 | 2 | **8 MED** | 增加重试机制 + 连接健康检查 |
| 7 | 测试数据污染 | 3 | 4 | **12 HIGH** | 恢复 conftest.py 中的数据清理 fixture |
| 8 | 配置漂移（多环境切换） | 2 | 4 | **8 MED** | 环境配置模板化 + 敏感信息外置 |
| 9 | YAML 格式错误 | 2 | 3 | **6 MED** | YAML schema 预校验 + IDE 模板 |
| 10 | 依赖版本冲突 | 2 | 3 | **6 MED** | 固定 requirements.txt 版本号 |
| 11 | 文件上传接口 | 3 | 2 | **6 MED** | 各文件类型（xlsx/csv）边界测试 |

**测试优先级顺序：** #1 登录认证 → #3 订单支付 → #2 参数依赖 → #4 轨迹查询 → #5 报警管理 → #7 数据清理

---

### 6. Environment Strategy

| Environment | Purpose | Config | Data | Trigger |
|-------------|---------|--------|------|---------|
| **Local（本地开发）** | 日常编写和调试用例 | `[api_envi] host = http://127.0.0.1:8787` | 本地 extract.yaml | 手动 `python run.py` |
| **Test（测试环境）** | 正式测试执行 | 修改 host 为测试服务器地址 | 独立 extract.yaml | Jenkins Job 触发 |
| **Staging（预发布）** | 上线前回归 | 修改 host 为预发布地址 | 预发布专用数据 | 手动 + Jenkins |

**环境改进建议：**
- 将 `config.ini` 拆分为 `config.dev.ini` / `config.test.ini` / `config.staging.ini`
- 通过环境变量 `TEST_ENV=test` 自动选择配置，而非手动修改文件
- 敏感信息（密码、token）迁移到环境变量或 `.env` 文件

---

### 7. Tool Selection Rationale

当前工具栈全部为项目自带，以下为保留/新增的决策依据：

| Tool | Decision | Rationale |
|------|----------|-----------|
| **pytest** | ✅ 保留 | 已深度定制（conftest fixture、YAML parametrize），团队熟悉 |
| **YAML 数据驱动** | ✅ 保留 | 降低用例编写门槛，非开发人员也能写测试数据 |
| **Allure 报告** | ✅ 保留 | 已集成完整，支持中文，报告美观 |
| **requests** | ✅ 保留 | Python HTTP 客户端标准选择 |
| **Jenkins** | ✅ 保留 | 已配置 Job，团队有运维支持 |
| **钉钉通知** | ✅ 保留 | 已集成，符合团队沟通习惯 |
| **jsonpath** | ✅ 保留 | 响应提取核心依赖 |
| **Git** | 🆕 引入 | 当前无版本管理，需紧急引入 |
| **pytest-xdist** | 🆕 考虑 | 用例增多后用于并行执行加速 |
| **pytest-env** | 🆕 考虑 | 管理多环境配置 |
| **k6 / locust** | 🔮 远期 | 性能测试需求出现后评估 |

**工具总拥有成本评估：**
- 当前工具栈全部为开源免费，无许可证成本
- 学习曲线：新成员需 1-2 周熟悉 YAML 数据驱动模式
- 维护成本：`debugtalk.py` 中的自定义函数是唯一需要持续扩展的地方

---

### 8. Entry/Exit Criteria

**单接口测试：**
- **Entry:** YAML 文件已通过格式校验；接口地址在对应环境中可访问；extract.yaml 中的依赖参数已就绪
- **Exit:** 所有 validation 断言通过；如有 extract 配置，提取的参数已写入 extract.yaml；Allure 报告无 FAILED

**业务场景测试：**
- **Entry:** 场景涉及的全部单接口已通过测试；前置接口的 extract 参数已确认可用；测试数据已准备
- **Exit:** 全链路通过；数据库断言验证数据一致性；场景总耗时在可接受范围内

**回归测试（执行 run.py）：**
- **Entry:** 环境配置已确认（host 指向正确）；extract.yaml 已清空（自动）；Jenkins Job 参数正确
- **Exit:** 通过率 > 95%；Allure 报告成功生成；钉钉通知已发送（如开启）

---

### 9. Quality Gates

| Gate | Checks | Enforced By |
|------|--------|-------------|
| **用例编写** | YAML 格式正确（`yaml.safe_load` 无报错）；必需字段齐全（baseInfo + case_name） | 框架自动校验 + IDE YAML 插件 |
| **本地执行** | `python run.py` 全部通过；无 extract 残留数据 | pre-commit hook（待建立） |
| **Jenkins 构建** | 全量回归通过率 > 95%；无 CRITICAL 用例失败 | Jenkins Job 配置 |
| **上线前** | 关键业务场景（登录、轨迹查询、订单支付）100% 通过；无未处理的 extract 数据 | 手动确认清单 |

---

### 10. Metrics & KPIs

| Metric | Definition | Current | Target (Q3) | Cadence |
|--------|-----------|---------|-------------|---------|
| 关键场景覆盖率 | 7 大业务场景中有自动化测试的比例 | ~70% | 100% | Monthly |
| 测试通过率 | 通过用例数 / 总用例数 | 待度量 | > 95% | Per Run |
| 失败用例 MTTR | 从发现失败到修复的平均时间 | 未跟踪 | < 4h (工作时间) | Per Incident |
| 框架可用性 | run.py 一键执行成功率 | 待度量 | > 98% | Weekly |
| 新增用例速度 | 每人天新增 YAML 用例数 | 未跟踪 | > 3 cases/day | Monthly |
| 假失败率 | 非代码缺陷导致的测试失败 | 待度量 | < 5% | Weekly |
| 参数提取成功率 | extract 操作成功的比例 | 待度量 | > 99% | Per Run |

---

### 11. Timeline & Milestones

**Phase 1 — 基础设施补全（Week 1-2）**
- [ ] `git init` + 创建 `.gitignore`（排除 venv/、__pycache__/、logs/、report/）
- [ ] 固定 `requirements.txt` 版本号（`pip freeze > requirements_lock.txt`）
- [ ] 恢复 `conftest.py` 中数据清理 fixture
- [ ] 建立 YAML 文件模板和编写规范文档
- *Exit: 项目纳入 Git 管理，可重现安装*

**Phase 2 — 核心风险覆盖（Week 3-6）**
- [ ] 编写登录 token 自动刷新机制（替换 extract.yaml 硬编码）
- [ ] 补齐订单支付全链路场景测试
- [ ] 补齐车辆报警全部 alarmType 用例
- [ ] 为 `replace_load()` 和 `extract_data()` 编写框架单元测试
- *Exit: 7 大关键场景 100% 覆盖，token 不再硬编码*

**Phase 3 — 质量门禁（Week 7-8）**
- [ ] 配置多环境切换（环境变量方案）
- [ ] Jenkins Job 配置 Git 轮询自动触发
- [ ] 建立 Pre-commit Hook（YAML 格式校验）
- [ ] 度量基线数据（通过率、执行时长、假失败率）
- *Exit: CI 自动触发，质量门禁生效*

**Phase 4 — 持续优化（Week 9+）**
- [ ] 探索 pytest-xdist 并行执行
- [ ] 评估 k6 性能测试集成
- [ ] 第一次策略回顾（v1.1）
- *Exit: 策略文档更新至 v1.1*

---

### 12. Risks to the Strategy Itself

| Risk | Mitigation |
|------|------------|
| **单人 QA 瓶颈** — 所有测试工作依赖一人，休假/离职导致停滞 | 编写完善的框架使用文档；将 YAML 用例编写能力传递给开发团队 |
| **被测试 API 频繁变更** — 接口字段改动导致大量 YAML 用例失效 | 与开发团队建立 API 变更通知机制；在 YAML 中多用 jsonpath 相对路径 |
| **远程数据库不稳定** — db 断言频繁失败导致对测试失去信心 | db 断言增加重试逻辑；区分"网络错误"和"数据错误" |
| **无 Git 历史导致回滚困难** — 改坏框架代码无法恢复 | Phase 1 立即初始化 Git |
| **token/cookie 维护负担** — 每次过期需手动更新多个 YAML 文件 | Phase 2 实现自动登录刷新 |

---

### 13. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-06-14 | Initial strategy document based on project analysis | QA Team |
