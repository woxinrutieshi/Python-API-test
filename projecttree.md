# Python-API-test
```
pythonproject/                                  # 项目根目录
├─ .agents/                                     # Claude skills生成目录
│  └─ qa-project-context.md
├─ base/                                        # 底层基类功能封装
│  ├─ apiutil.py                                # 通用接口请求基类
│  ├─ apiutil_business.py                       # 业务接口请求封装
│  ├─ generateId.py                             # 自动生成业务唯一ID工具
│  ├─ new_testcase_tools.py                     # 新测试用例生成工具
│  ├─ new_tools.ui
│  ├─ removefile.py                             # 文件清理工具
│  ├─ __init__.py                               # 标识base为Python可导入包
├─ common/                                      # 全局公共功能层
│  ├─ assertions.py                             # 自定义断言库
│  ├─ connection.py                             # 数据库连接封装
│  ├─ debugtalk.py                              # 调试函数库
│  ├─ dingRobot.py                              # 钉钉机器人
│  ├─ handleExcel.py                            
│  ├─ operationcsv.py                           # csv数据处理
│  ├─ operxml.py                                # xml文件解析
│  ├─ Pjenkins.py                               # jenkins API封装
│  ├─ readyaml.py                               # yaml读写工具
│  ├─ recordlog.py                              # 日志封装
│  ├─ semail.py                                 # 邮件推送
│  ├─ sendrequest.py                            # 简易请求封装    
│  ├─ two_dimension_data.py
├─ conf/                                        # 全局环境配置层
│  ├─ config.ini                                # 环境配置文件
│  ├─ operationConfig.py                        # 配置读取工具    
│  ├─ setting.py                                # 项目全局常量    
├─ data/                                        # 测试数据
│  ├─ loginName.yaml                            # 登录账号参数化数据
│  ├─ login_data.csv                            # 登录接口批量测试数据
│  ├─ sql/                                      # SQL脚本存储目录
│  │  ├─ homePage.xml
│  │  └─ newVehicleAddShare.xml
│  ├─ vehicleNo.csv
│  └─ 测试数据.xls                               
├─ logs/                                        # 日志文件目录
│  └─ test.20260627.log                         # 每日运行日志，记录请求报文、响应、报错堆栈
├─ report/                                      # 测试报告文件
│  ├─ allureReport/                             # Allure交互式可视化测试报告
│  ├─ temp/                                     # 临时缓存目录
│  ├─ results.xml                               # pytest原生执行结果xml文件
│  └─ tmreport/
│     └─ testReport.html
├─ testcase/                                    # 测试用例目录
│  ├─ Business interface/                       # 业务流程用例
│  │  ├─ BusinessScenario.yml                   # 业务场景流程定义文件
│  │  ├─ test_business_scenario.py              # 业务场景自动化执行脚本
│  ├─ ProductManager/                           # 商品管理模块用例包
│  │  ├─ apiType.yaml                           # 商品模块接口分类配置
│  │  ├─ commitOrder.yaml                       # 提交订单接口测试参数
│  │  ├─ getProductList.yaml                    # 商品列表查询接口测试数据
│  │  ├─ login_dw.yaml
│  │  ├─ orderPay.yaml
│  │  ├─ productDetail.yaml
│  │  ├─ test_productList.py
│  ├─ Single interface/                         # 单接口独立测试用例
│  │  ├─ addUser.yaml                           # 新增用户接口测试数据
│  │  ├─ deleteUser.yaml                        # 删除用户接口测试数据
│  │  ├─ queryUser.yaml                         # 查询用户接口测试数据
│  │  ├─ test_debug_api.py                      # 单接口调试专用脚本
│  │  ├─ updateUser.yaml                        # 修改用户接口测试数据
│  ├─ conftest.py                               # 模块级pytest固件
├─ venv/                                        # 项目虚拟环境
├─ conftest.py                                  # 全局pytest钩子文件   
├─ environment.xml                              # 多环境切换配置
├─ extract.yaml                                 # 接口响应提取参数
├─ pytest.ini                                   # pytest全局配置
├─ projecttree.md                               # 项目目录结构说明文档
├─ requirements.txt                             # 项目依赖清单
├─ run.py                                       # 项目统一启动入口 

```