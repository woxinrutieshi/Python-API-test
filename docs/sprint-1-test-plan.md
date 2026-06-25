# Sprint 1 Test Plan — API 测试框架基础设施建设 + 核心风险覆盖
**Sprint dates:** Week 1 - Week 6（对应 Strategy Phase 1 + Phase 2）
**Test lead:** QA Team（单人）
**Last updated:** 2026-06-14

---

## Scope

| # | Feature / Task | Risk | Test Types | Source | Status |
|---|---------------|------|-----------|--------|--------|
| 1 | Git 初始化 + .gitignore + 首次提交 | HIGH | 验证 | Strategy §11 Phase 1 | Not Started |
| 2 | 依赖版本锁定（requirements_lock.txt） | HIGH | 验证 | Strategy §11 Phase 1 | Not Started |
| 3 | 恢复数据清理 fixture（conftest.py） | HIGH | 框架单元测试 | Strategy §11 Phase 1 | Not Started |
| 4 | YAML 用例模板 + 编写规范文档 | MED | 文档 | Strategy §11 Phase 1 | Not Started |
| 5 | 登录 token 自动刷新机制 | CRIT | 框架单元测试 + 单接口测试 | Strategy §11 Phase 2 | Not Started |
| 6 | 订单支付全链路场景测试 | CRIT | 业务场景测试 + DB 断言 | Strategy §11 Phase 2 | Not Started |
| 7 | 车辆报警全部 alarmType 用例补齐 | HIGH | 单接口测试（参数化） | Strategy §11 Phase 2 | Not Started |
| 8 | 框架核心函数单元测试 | HIGH | 框架单元测试 | Strategy §11 Phase 2 | Not Started |
| 9 | extract 提取失败时的空值校验 | HIGH | 框架单元测试 | Strategy Risk #2 | Not Started |

---

## Coverage Summary

这是基础设施 + 测试用例补充的混合 Sprint，按类型分解：

| 类型 | 计划数 | 说明 |
|------|--------|------|
| 框架单元测试 | 10+ | 覆盖 replace_load、extract_data、extract_data_list、5 种断言方法 |
| 新增 YAML 单接口用例 | 8+ | 报警模块全部 alarmType（围栏6种 + 疲劳3种 + 区域7种） |
| 新增 YAML 业务场景 | 2 | 订单支付全链路、登录→下单→查询 |
| YAML 文件模板 | 1 | 带注释的模板文件 |
| 框架改进 | 3 | Git 初始化、依赖锁定、数据清理恢复 |
| **Gaps identified:** | 2 | 性能测试（defer）、安全扫描（defer）— 见策略文档 out of scope |

---

## Effort Budget

采用 6 周 Sprint，单人 QA，每周可用 20 小时（兼职或并行其他任务估算）：

```
New automated tests to write:
  框架单元测试:    10 tests × 1.0 hrs = 10 hrs  (框架代码测试比业务测试更复杂)
  单接口 YAML:      8 tests × 0.5 hrs =  4 hrs  (YAML 编写非常快)
  业务场景 YAML:    2 tests × 1.0 hrs =  2 hrs  (多接口串联需调试)

Framework improvement:
  Git 初始化:           1 × 0.5 hrs  =  0.5 hrs
  依赖版本锁定:         1 × 0.5 hrs  =  0.5 hrs
  数据清理恢复:          1 × 1.0 hrs  =  1 hr
  Token 自动刷新开发:    1 × 4.0 hrs  =  4 hrs  (核心改进，需设计)
  extract 空值校验:      1 × 1.0 hrs  =  1 hr

Documentation:
  YAML 模板 + 编写规范:  1 × 2.0 hrs  =  2 hrs

Setup & test data:
  测试数据准备:          1 × 2.0 hrs  =  2 hrs

Bug verification buffer (20%):          6 hrs
Re-test after fixes buffer (10%):       3 hrs

Total estimated effort:                36 hrs
Available tester hours (6 weeks × 20h): 120 hrs → 实际可用约 80 hrs（预留学习/沟通）
Capacity utilization:                   45%   (远低于 70-80% 上限，留有充分缓冲)
```

---

## Environment & Data

| Item | Detail |
|------|--------|
| 测试环境 URL | `http://127.0.0.1:8787`（本地）/ 测试服务器（待确认） |
| 配置文件 | `conf/config.ini` — 需确认 test/staging 的 host 地址 |
| extract.yaml | 每次执行前自动清空（conftest.py clear_extract fixture） |
| 测试账号 | `data/loginName.yaml` 中的登录信息 |
| 测试数据文件 | `data/vehicleNo.csv`（车牌号）、`data/测试数据.xls`（Excel 数据源） |
| 数据库连接 | MySQL `zqsjfx` — 需确认测试环境数据库可访问 |

---

## Entry Criteria

- [ ] 测试环境 API 可访问（`curl http://127.0.0.1:8787` 返回响应）
- [ ] 数据库连接正常（MySQL、ClickHouse、Redis）
- [ ] `pip install -r requirements_lock.txt` 无报错
- [ ] `python run.py` 现有用例全部通过（或已知失败项已记录）
- [ ] Git 仓库已初始化并完成首次提交

---

## Exit Criteria

- [ ] Git 仓库包含完整提交历史 + .gitignore
- [ ] `requirements_lock.txt` 存在且可重现安装
- [ ] 数据清理 fixture 已恢复并通过框架单元测试验证
- [ ] Token 自动刷新机制已实现，`extract.yaml` 中不再有硬编码 token
- [ ] 订单支付全链路场景测试通过（含 DB 断言）
- [ ] 车辆报警全部 alarmType 参数化用例通过
- [ ] 框架核心函数单元测试 ≥ 10 个，全部通过
- [ ] YAML 模板文件和编写规范文档已交付
- [ ] 无 CRITICAL 或 HIGH 风险项的未处理 GAP

---

## Feature Decomposition（关键任务分解）

### Feature 1: Token 自动刷新机制
```
Source: Strategy Risk #1 (登录认证失效)
Priority: CRITICAL

Testable Scenarios:
  1. 系统登录成功 → token 写入 extract.yaml，格式正确
  2. 后续接口引用 ${get_extract_data(token)} → 成功获取最新 token
  3. Token 即将过期 → 自动重新登录刷新（过期检测逻辑）
  4. 登录接口本身失败 → 所有依赖用例 SKIP 而非 FAIL（避免误报）
  5. 并发执行 → extract.yaml 读写无竞争条件
```

### Feature 2: 订单支付全链路场景
```
Source: Strategy Risk #3 (订单支付)
Priority: CRITICAL

Testable Scenarios:
  1. 登录 → 浏览产品列表 → 查看产品详情 → 创建订单 → 支付 → 查询订单状态
  2. 订单金额校验：DB 断言验证订单金额与产品价格一致
  3. 支付失败场景：余额不足/支付超时 → 订单状态正确回滚
  4. 重复支付：同一订单号二次支付 → 接口拒绝
```

### Feature 3: 车辆报警全类型覆盖
```
Source: Strategy Risk #5 (报警管理)
Priority: HIGH

Testable Scenarios:
  1. 围栏报警 (alarmType: 1,3,8,2,5,6) → 每种类型单独参数化用例
  2. 疲劳驾驶报警 (alarmType: 1,3,8) → 参数化
  3. 区域报警 (alarmType: 1,3,8,2,5,6,9) → 参数化
  4. 无效 alarmType → 接口返回错误码
  5. 无报警数据时 → 返回空列表而非报错
```

### Feature 4: 框架核心函数单元测试
```
Source: Strategy §4 (Test Pyramid - 缺失底层)
Priority: HIGH

Testable Functions:
  1. replace_load() — ${get_extract_data(token)} 正常替换
  2. replace_load() — 嵌套表达式 ${md5_encryption(${timestamp()})}
  3. replace_load() — 无效函数名 → 预期异常处理
  4. extract_data() — jsonpath $.data.id 提取
  5. extract_data() — 正则 '"status":"(.*?)"' 提取
  6. extract_data_list() — jsonpath 提取多个值返回列表
  7. contains_assert() — status_code 断言 + 文本包含断言
  8. equal_assert() — 字段相等断言
  9. db 断言 — SQL 查询返回预期结果
  10. DebugTalk.get_extract_data() — randoms 参数各取值 (0/-1/-2/1/2)
```

---

## Prioritization Matrix (Risk × Effort)

```
                    EFFORT
                    Low (< 1 hr)       Medium (1-3 hrs)     High (> 3 hrs)
                 +------------------+---------------------+------------------+
  CRITICAL       | extract 空值校验 | 订单支付全链路场景   | Token 自动刷新   |
                 | → DO FIRST       | → DO SECOND          | → DO SECOND      |
R                +------------------+---------------------+------------------+
  HIGH           | Git 初始化       | 框架单元测试(10个)   |                  |
                 | 依赖版本锁定     | 报警全类型用例(8个)  |                  |
  I              | → DO FIRST       | → DO SECOND          |                  |
  S              +------------------+---------------------+------------------+
  K MEDIUM       | 数据清理恢复     | YAML 模板 + 规范文档 |                  |
                 | → DO FIRST       | → DO THIRD           |                  |
                 +------------------+---------------------+------------------+
  LOW            |                  |                      |                  |
                 |                  |                      |                  |
                 +------------------+---------------------+------------------+
```

---

## Resource Allocation

| Tester | Available (6 wks) | Assigned Work | Hours | Utilization |
|--------|-------------------|---------------|-------|-------------|
| QA (单人) | 80 hrs | DO FIRST 任务 (Git+依赖+数据清理+空值校验) | 3 | — |
| | | DO SECOND 任务 (Token刷新+支付场景+单元测试+报警用例) | 24 | — |
| | | DO THIRD 任务 (YAML模板文档) | 2 | — |
| | | Setup & 测试数据准备 | 2 | — |
| | | Bug verification buffer | 6 | — |
| | | Re-test buffer | 3 | — |
| | | **Total allocated** | **40 hrs** | **50%** |

---

## Schedule (6-Week Timeline)

```
Week 1: 基础设施
  Day 1-2: Git 初始化 → .gitignore → 首次提交 → requirements_lock.txt
  Day 3-4: 恢复数据清理 fixture → 框架单元测试环境搭建 (pytest + conftest)
  Day 5:   extract 空值校验实现 + 测试

Week 2: Token + 框架测试
  Day 1-3: Token 自动刷新机制设计与实现
  Day 4-5: 框架核心函数单元测试（replace_load, extract_data, 断言方法）

Week 3: 订单支付场景
  Day 1-3: 订单支付全链路 YAML 场景编写 + 调试
  Day 4-5: DB 断言验证 + 失败场景补充

Week 4: 报警用例 + 参数化
  Day 1-3: 围栏报警 6 种 alarmType 参数化 YAML
  Day 4-5: 疲劳报警 3 种 + 区域报警 7 种

Week 5: 补齐 + 回归
  Day 1-2: YAML 模板文件 + 编写规范文档
  Day 3-5: 全量回归测试 + 修复失败用例

Week 6: 收尾
  Day 1-2: Bug 修复验证 + 最终回归
  Day 3:   覆盖率检查（7 大场景是否全部覆盖）
  Day 4:   文档交付、策略回顾准备
  Day 5:   Sprint 回顾 + 下一 Sprint 计划输入

Buffer: 20% 时间（约 1 天/周）为未计划工作预留
```

---

## Risks to the Plan

| Risk | Mitigation |
|------|-----------|
| 测试环境 API 不可用 | 优先完成框架单元测试（不依赖外部 API），场景测试延期到环境恢复 |
| Token 自动刷新方案设计超预期 | Week 2 时间盒硬限制；若超时则先用半自动方案（脚本辅助刷新） |
| 订单支付接口未开发完成 | 先写 YAML 骨架 + Mock 返回，等接口就绪后接入 |
| 数据库测试环境不可访问 | DB 断言用例标记 SKIP，优先完成不依赖 DB 的测试 |
| 单人瓶颈 — 生病/请假 | 关键任务（Git、依赖锁定）集中在 Week 1 完成；YAML 用例可低门槛交接给开发 |
| extract.yaml 并发读写问题 | 当前为单线程执行（pytest 默认），暂不引入并行；加文件锁预留扩展 |

---

## Daily Tracking (模板)

```
Day: ___ | Date: ___
Completed today:   ___________
Blocked:           ___________
Bugs found:        ___________
Tomorrow's plan:   ___________
Coverage:          __/9 tasks complete
Buffer consumed:   ___/6 hrs
```
