# coding=utf-8
# @Time    : 2019/7/2 17:13
# @Author  : zwa
# coding:utf-8

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase


class ResultsCollector(CallbackBase):
    """重构执行结果"""
    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result, *args, **kwargs):
        """不可达"""
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        """执行成功"""
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        """执行失败"""
        self.host_failed[result._host.get_name()] = result


def run_ansible(module_name,module_args,host_list,option_dict):
    # 初始化需要的对象
    Options = namedtuple('Options',
                         ['connection', 'module_path', 'forks', 'become',
                          'become_method', 'private_key_file','become_user',
                          'remote_user', 'check', 'diff']
                         )
    #负责查找和读取yaml、json和ini文件
    loader = DataLoader()

    options = Options(connection='ssh', module_path=None, forks=5, become=option_dict['become'],
                      become_method='sudo',private_key_file="/root/.ssh/id_rsa",
                      become_user='root', remote_user=option_dict['remote_user'], check=False, diff=False
                      )

    passwords = dict(vault_pass='secret')

    # 实例化ResultCallback来处理结果
    callback = ResultsCollector()

    # 创建库存(inventory)并传递给VariableManager
    inventory = InventoryManager(loader=loader, sources=['/etc/ansible/hosts'])
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    # 创建任务
    host = ",".join(host_list)
    play_source = dict(
        name="Ansible Play",
        hosts=host,
        gather_facts='no',
        tasks=[
            dict(action=dict(module=module_name, args=module_args), register='shell_out'),
        ]
    )
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    # 开始执行
    tqm = None

    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        options=options,
        passwords=passwords,
        stdout_callback=callback,
    )
    result = tqm.run(play)

    result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}

    for host, result in callback.host_ok.items():
        result_raw['success'][host] = result._result['stdout_lines']

    for host, result in callback.host_failed.items():
        result_raw['failed'][host] = result._result['stderr_lines']

    for host, result in callback.host_unreachable.items():
        result_raw['unreachable'][host] = result._result["msg"]

    return json.dumps(result_raw, indent=4)


if __name__ == "__main__":
    option_dict={"become":True,"remote_user":"root"}
    module_name = 'shell'
    module_args = "ls /root"
    host_list = ['192.168.3.16']
    ret = run_ansible(module_name,module_args,host_list,option_dict)
    print(ret)
    print(eval(ret))
    print(ret)
    
