import allure
import pytest
import requests

from common.readyaml import get_testcase_yaml
from base.apiutil import RequestBase
from base.generateId import m_id, c_id
from common import dingRobot

#Allure常用装饰器及作用
@allure.feature(next(m_id) + '用户管理模块（单接口）')
class TestUserManager:

    # 场景，allure报告的目录结构
    @allure.story(next(c_id) + "新增用户")
    # 测试用例执行顺序设置
    @pytest.mark.run(order=1)
    # 参数化，yaml数据驱动
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/Single interface/addUser.yaml"))
    def test_add_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    # # 所有可选参数统一放到 kwargs 字典
    # kwargs = {
    #     "headers": {"Content-Type": "application/json", "token": "abc123"},
    #     "json": {"user_id": 1001, "name": "测试"},
    #     "timeout": 10,
    #     "verify": False,
    #     "allow_redirects": True
    # }
    # #挂载
    # #requests模块发送请求的三层架构，get，session，request
    # requests.Session().request(
    #     method="None" ,
    #     url="None" ,
    #     # 解包运算符解包字典。
    #     **kwargs
    # )


    #dingRobot.send_dd_msg("测试消息")

    @allure.story(next(c_id) + "修改用户")
    @pytest.mark.run(order=2)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/Single interface/updateUser.yaml"))
    def test_update_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "删除用户")
    @pytest.mark.run(order=3)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/Single interface/deleteUser.yaml"))
    def test_delete_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)

    @allure.story(next(c_id) + "查询用户")
    @pytest.mark.run(order=4)
    @pytest.mark.parametrize('base_info,testcase', get_testcase_yaml("./testcase/Single interface/queryUser.yaml"))
    def test_query_user(self, base_info, testcase):
        allure.dynamic.title(testcase['case_name'])
        RequestBase().specification_yaml(base_info, testcase)



