import json
import re
from json.decoder import JSONDecodeError

import allure
import jsonpath

from common.assertions import Assertions
from common.debugtalk import DebugTalk
from common.readyaml import get_testcase_yaml, ReadYamlData
from common.recordlog import logs
from common.sendrequest import SendRequest
from conf.operationConfig import OperationConfig
from conf.setting import FILE_PATH


class RequestBase:

    def __init__(self):
        self.run = SendRequest()
        self.conf = OperationConfig()
        self.read = ReadYamlData()
        self.asserts = Assertions()

    def replace_load(self, data):
        """yaml数据参数占位符替换解析"""
        str_data = data
        if not isinstance(data, str):
            str_data = json.dumps(data, ensure_ascii=False)
            # print('从yaml文件获取的原始数据：', str_data)
        for i in range(str_data.count('${')):
            if '${' in str_data and '}' in str_data:
                start_index = str_data.index('$')
                end_index = str_data.index('}', start_index)
                ref_all_params = str_data[start_index:end_index + 1]
                # 取出yaml文件的函数名
                func_name = ref_all_params[2:ref_all_params.index("(")]
                # 取出函数里面的参数
                func_params = ref_all_params[ref_all_params.index("(") + 1:ref_all_params.index(")")]
                # 传入替换的参数获取对应的值,类的反射----getattr,setattr,del....
                extract_data = getattr(DebugTalk(), func_name)(*func_params.split(',') if func_params else "")

                if extract_data and isinstance(extract_data, list):
                    extract_data = ','.join(e for e in extract_data)
                str_data = str_data.replace(ref_all_params, str(extract_data))
                # print('通过解析后替换的数据：', str_data)

        # 还原数据
        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data
        return data

    #specification_yaml中包含了数据驱动接口测试全流程操作的封装。很有必要。
    def specification_yaml(self, base_info, test_case):
        """
        接口请求处理基本方法
        :param base_info: yaml文件里面的baseInfo
        :param test_case: yaml文件里面的testCase
        :return:
        """

        #base_info、test_case表示yaml文件中的基础信息和数据已经传入。在编写用例时形参作为字典列表的结构传入。

        try:
            params_type = ['data', 'json', 'params']
            url_host = self.conf.get_section_for_data('api_envi', 'host')
            api_name = base_info['api_name']
            # 进行报告埋点
            allure.attach(api_name, f'接口名称：{api_name}', allure.attachment_type.TEXT)
            url = url_host + base_info['url']
            allure.attach(api_name, f'接口地址：{url}', allure.attachment_type.TEXT)
            method = base_info['method']
            allure.attach(api_name, f'请求方法：{method}', allure.attachment_type.TEXT)
            header = self.replace_load(base_info['header'])
            allure.attach(api_name, f'请求头：{header}', allure.attachment_type.TEXT)
            # 提取接口元信息解析，url、method、Header；

            cookie = None
            if base_info.get('cookies') is not None:
                cookie = eval(self.replace_load(base_info['cookies']))
            # 请求参数解析，特殊参数单独封装额外转换处理，cookie

            # 请求数据test_case的提取与参数替换，将case_name弹出来。
            case_name = test_case.pop('case_name')
            allure.attach(api_name, f'测试用例名称：{case_name}', allure.attachment_type.TEXT)
            # 调用replace_load方法对数据动态变量替换，将原始的断言表达式替换为全局缓存、上一步接口的真实数据
            val = self.replace_load(test_case.get('validation'))
            test_case['validation'] = val
            validation = eval(test_case.pop('validation'))

            extract = test_case.pop('extract', None)
            extract_list = test_case.pop('extract_list', None)
            # 提取用例基本信息

            # 循环动态参数替换处理
            for key, value in test_case.items():
                if key in params_type:
                    test_case[key] = self.replace_load(value)
            file, files = test_case.pop('files', None), None
            if file is not None:
                for fk, fv in file.items():
                    allure.attach(json.dumps(file), '导入文件')
                    files = {fk: open(fv, mode='rb')}
            # 处理文件上传接口

            # 解包运算符解包字典，不过不是kwargs，是另一个字典。
            # 组合完整请求并执行
            res = self.run.run_main(name=api_name, url=url, case_name=case_name, header=header, method=method,
                                    file=files, cookies=cookie, **test_case)

            status_code = res.status_code
            allure.attach(self.allure_attach_response(res.json()), '接口响应信息', allure.attachment_type.TEXT)
            # 请求方法封装到common.sendrequest.SendRequest

            # 请求之后，获取到响应结果，后置阶段，将Json格式转为字典类型操作
            try:
                res_json = json.loads(res.text)  # 把json格式转换成字典字典
                if extract is not None:
                    self.extract_data(extract, res.text) # extract接口依赖提取、持久化
                if extract_list is not None:
                    self.extract_data_list(extract_list, res.text)
                # 处理断言
                self.asserts.assert_result(validation, res_json, status_code)
            except JSONDecodeError as js:
                logs.error('系统异常或接口未请求！')
                raise js
            except Exception as e:
                logs.error(e)
                raise e

        except Exception as e:
            raise e


    @classmethod
    def allure_attach_response(cls, response):
        if isinstance(response, dict):
            allure_response = json.dumps(response, ensure_ascii=False, indent=4)
        else:
            allure_response = response
        return allure_response

    def extract_data(self, testcase_extarct, response):
        """
        提取接口的返回值，支持正则表达式和json提取器
        :param testcase_extarct: testcase文件yaml中的extract值
        :param response: 接口的实际返回值
        :return:
        """
        try:
            pattern_lst = ['(.*?)', '(.+?)', r'(\d)', r'(\d*)']
            for key, value in testcase_extarct.items():

                # 处理正则表达式提取
                for pat in pattern_lst:
                    if pat in value:
                        ext_lst = re.search(value, response)
                        if pat in [r'(\d+)', r'(\d*)']:
                            extract_data = {key: int(ext_lst.group(1))}
                        else:
                            extract_data = {key: ext_lst.group(1)}
                        self.read.write_yaml_data(extract_data)
                # 处理json提取参数
                if '$' in value:
                    ext_json = jsonpath.jsonpath(json.loads(response), value)[0]
                    if ext_json:
                        extarct_data = {key: ext_json}
                        logs.info('提取接口的返回值：', extarct_data)
                    else:
                        extarct_data = {key: '未提取到数据，请检查接口返回值是否为空！'}
                    self.read.write_yaml_data(extarct_data)
        except Exception as e:
            logs.error(e)

    def extract_data_list(self, testcase_extract_list, response):
        """
        提取多个参数，支持正则表达式和json提取，提取结果以列表形式返回
        :param testcase_extract_list: yaml文件中的extract_list信息
        :param response: 接口的实际返回值,str类型
        :return:
        """
        try:
            for key, value in testcase_extract_list.items():
                if "(.+?)" in value or "(.*?)" in value:
                    ext_list = re.findall(value, response, re.S)
                    if ext_list:
                        extract_date = {key: ext_list}
                        logs.info('正则提取到的参数：%s' % extract_date)
                        self.read.write_yaml_data(extract_date)
                if "$" in value:
                    # 增加提取判断，有些返回结果为空提取不到，给一个默认值
                    ext_json = jsonpath.jsonpath(json.loads(response), value)
                    if ext_json:
                        extract_date = {key: ext_json}
                    else:
                        extract_date = {key: "未提取到数据，该接口返回结果可能为空"}
                    logs.info('json提取到参数：%s' % extract_date)
                    self.read.write_yaml_data(extract_date)
        except:
            logs.error('接口返回值提取异常，请检查yaml文件extract_list表达式是否正确！')


if __name__ == '__main__':
    case_info = get_testcase_yaml(FILE_PATH['YAML'] + '/LoginAPI/login.yaml')[0]
    # print(case_info)
    req = RequestBase()
    # res = req.specification_yaml(case_info)
    res = req.specification_yaml(case_info)
    print(res)
