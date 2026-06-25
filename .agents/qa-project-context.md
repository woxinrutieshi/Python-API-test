# QA Project Context

> 自动生成于 2026-06-14 | 基于代码检测 + 用户确认

## Product

- **产品名称：** 某物联网车辆监控平台 API 后端
- **产品类型：** 内部工具 / API 服务
- **一句话描述：** 提供车辆轨迹查询、报警管理、用户管理、订单/产品管理等功能的 RESTful API 后端服务
- **生产环境：** （待补充）
- **测试环境：** `http://127.0.0.1:8787`（本地开发环境，配置于 `conf/config.ini`）
- **预发布环境：** （待补充）

### 关键业务场景（优先级从高到低）

1. **用户登录认证** — 获取 token/cookie，所有后续接口依赖
2. **车辆轨迹查询** — 核心业务，根据车牌号 + 时间段查询车辆行驶轨迹
3. **订单创建与支付** — 产品下单、支付流程
4. **产品列表与详情查询** — 产品管理模块
5. **车辆报警管理** — 围栏报警、疲劳驾驶报警、区域报警
6. **用户管理（CRUD）** — 新增/修改/删除/查询用户
7. **文件导入** — 批量导入黑名单等数据

## Tech Stack

### 被测试系统
- **后端框架：** 未知（通过 RESTful API 交互）
- **API 风格：** RESTful JSON API
- **认证方式：** Token + Cookie（`access_token_cookie`、`token` header）
- **数据库：** MySQL（`zqsjfx` 库）、ClickHouse、Redis、MongoDB

### 测试框架技术栈
- **语言：** Python 3
- **测试框架：** pytest（配置于 `pytest.ini`）
- **数据驱动：** YAML 文件（通过 `common/readyaml.py` 的 `get_testcase_yaml()` 加载）
- **HTTP 客户端：** requests 库（通过 `common/sendrequest.py` 封装）
- **测试报告：** Allure（`allure_python_commons`），报告生成于 `report/allureReport/`
- **辅助库：** PyYAML、jsonpath、pandas、SQLAlchemy、PyMySQL、paramiko、faker

## Test Stack

### API / 接口测试
- **框架：** pytest + YAML 数据驱动（自研封装）
- **配置位置：** `pytest.ini`、`conf/setting.py`、`conf/config.ini`
- **测试用例目录：** `testcase/`（按模块分三个子目录）
  - `testcase/Single interface/` — 单接口测试（用户 CRUD）
  - `testcase/Business interface/` — 业务场景测试（多接口串联）
  - `testcase/ProductManager/` — 产品管理模块测试
- **测试数据目录：** `data/`（YAML、CSV、Excel、XML）
- **全局夹具：** `conftest.py`（根目录）+ `testcase/conftest.py`
- **测试发现规则：** `test_*.py` 文件、`Test*` 类、`test*` 函数

### 断言类型
| 断言方式 | YAML 关键字 | 说明 |
|----------|-------------|------|
| 字符串包含 | `contains` | 验证响应中是否包含预期字符串，支持 `status_code` 特殊处理 |
| 相等断言 | `eq` | 验证响应字段值是否等于预期值 |
| 不相等断言 | `ne` | 验证响应字段值是否不等于预期值 |
| 任意值断言 | `rv` | 验证响应中任意字段的值 |
| 数据库断言 | `db` | 直接写 SQL 验证数据库中的数据 |

### 单元测试
- **无**

### E2E 测试
- **无** — 本项目为纯 API 接口测试框架，不涉及 UI/E2E

### 性能测试
- **无**

## CI/CD

- **平台：** Jenkins（通过 `common/Pjenkins.py` 集成 python-jenkins 库）
- **Jenkins 地址：** `http://192.168.105.36:8088/job/hbjjapi/`
- **触发方式：** 手动执行 `run.py` 或通过 Jenkins Job 触发
- **测试报告：** allure 报告 + JUnit XML（`report/results.xml`）
- **通知方式：** 钉钉机器人（`common/dingRobot.py`，在 `conf/setting.py` 中通过 `dd_msg` 开关控制）
- **无 Git 仓库：** 当前项目未纳入 Git 版本管理
- **无 GitHub Actions / GitLab CI**

## Environments

- **开发环境：** `http://127.0.0.1:8787`（本地）
- **环境配置：** 所有环境连接信息集中管理在 `conf/config.ini`
- **多环境切换：** 通过修改 `config.ini` 中 `api_envi` section 的 `host` 值切换
- **数据库环境：**
  - MySQL：远程数据库（`zqsjfx`）
  - ClickHouse：远程（端口 8123）
  - Redis：远程（端口 7005）
  - MongoDB：远程（端口 27017）
- **环境差异：** 仅有一套配置，无 staging/production 分离

## Quality Goals

> 当前无明确的量化质量目标，以下为建议初始目标：

| 指标 | 建议目标 | 当前状态 |
|------|---------|---------|
| API 接口覆盖率 | 覆盖所有关键业务场景的接口 | 已覆盖主要模块 |
| 测试通过率 | > 95% | 待度量 |
| 构建稳定性 | 无假失败（flake < 2%） | 待度量 |
| 执行时长 | 全量回归 < 15 分钟 | 待度量 |
| 报告留存 | 每次构建保留 allure 报告 | 已实现（`report/allureReport/`） |

## Risk Areas

| 风险区域 | 风险等级 | 业务影响 | 说明 |
|----------|---------|---------|------|
| 登录认证失效 | **Critical** | 高影响 × 高概率 | Token/Cookie 过期会导致所有后续接口失败。`extract.yaml` 中的 token 是硬编码的，过期后需手动更新 |
| 接口参数依赖链 | **Critical** | 高影响 × 高概率 | 接口间通过 `extract.yaml` 传递参数，提取表达式（jsonpath/正则）写错会导致下游接口全部失败 |
| 数据库断言失效 | **Important** | 高影响 × 低概率 | `db` 断言依赖远程数据库连接，网络波动或数据变更可能导致断言误报 |
| 测试数据污染 | **Important** | 中影响 × 高概率 | 测试执行可能在数据库中产生脏数据，`conftest.py` 中的数据清理逻辑当前被注释掉了 |
| 多环境配置漂移 | **Monitor** | 低影响 × 高概率 | `config.ini` 中的数据库密码等敏感信息硬编码，切换环境容易出错 |
| YAML 格式错误 | **Monitor** | 低影响 × 中概率 | YAML 文件编码或缩进错误会导致测试用例加载失败，且错误信息不直观 |
| 第三方依赖版本冲突 | **Monitor** | 低影响 × 中概率 | `requirements.txt` 未固定版本号，新版本可能引入兼容性问题（README 中也提到了这点） |

## Team

- **QA 工程师：** 1 人（你）
- **开发:QA 比例：** 未知（推测为高比例，QA 资源稀缺）
- **测试方法论：** 未明确
- **QA 介入时机：** 推测为开发完成后（接口文档提供后编写 YAML 测试数据）
- **自动化归属：** QA 独立负责接口自动化测试框架的维护和用例编写

## Conventions

### 测试文件命名
- **测试 Python 文件：** `test_*.py`（pytest 发现规则）
- **测试类：** `Test*` 开头
- **测试函数：** `test*` 开头
- **测试数据文件：** `*.yaml`，与对应的 Python 测试文件同目录

### 测试数据规范
- **YAML 结构：** 每个 YAML 文件包含 `baseInfo`（接口信息）+ `testCase`（用例列表）
- **参数传递：** 使用 `${函数名(参数)}` 语法引用 `common/debugtalk.py` 中的函数
- **接口依赖：** 通过 `extract.yaml` 实现接口间的参数传递
- **测试数据文件：** CSV（无表头，纯数据行）、Excel（默认读第一个 sheet）

### 选择器策略
- **不适用** — 本项目是纯 API 测试，无 UI 选择器

### 分支策略
- **无 Git 版本管理** — 建议尽快初始化 Git 仓库

### 代码规范
- 注释语言：中文
- 文件编码：UTF-8（YAML 文件必须为 UTF-8）
- 日志语言：中文（通过 `common/recordlog.py` 统一管理）
