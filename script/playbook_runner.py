#!/usr/bin/env python
# coding:utf8

# coding: utf-8
# import os
# import sys
import time
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.executor.playbook_executor import PlaybookExecutor
# from ansible.playbook.play import Play
# from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import logging
logger = logging.getLogger('sourceDns.webdns.views')

# 存放yml的目录
# YML_DIR = ''

#  class ansible_Runner(object):
#     """
#     This is a General object for parallel execute modules.
#     """

#     def __init__(self,  *args, **kwargs):
#         self.resource = '/etc/ansible/hosts'
#         self.inventory = None
#         self.variable_manager = None
#         self.loader = None
#         self.options = None
#         self.passwords = None
#         self.callback = None
#         self.__initializeData()
#         self.results_raw = {}

#     def __initializeData(self):
#         """
#         初始化ansible配置
#         """
#         Options = namedtuple('Options',
#                              ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks',
#                               'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
#                               'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check', 'diff'])


#         self.loader = DataLoader()
#         self.options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
#                           module_path=None, forks=100, remote_user='root', private_key_file=None,
#                           ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None,
#                           become=True, become_method='sudo', become_user='root', verbosity=None, check=False,
#                           diff=False)
#         self.passwords = dict(vault_pass='secret')
#         self.inventory = InventoryManager(loader=self.loader, sources=self.resource)
#         self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

#     def run(self, host_list, module_name, module_args, ):
#         """
#         run module from andible ad-hoc.
#         module_name: ansible module_name
#         module_args: ansible module args
#         """
#         play_source = dict(
#             name="Ansible Ad-hoc Command",
#             hosts=host_list,
#             gather_facts='no',
#             tasks=[dict(action=dict(module=module_name, args=module_args))]
#         )
#         play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)

#         tqm = None
#         self.callback = ResultsCollector()
#         try:
#             tqm = TaskQueueManager(
#                 inventory=self.inventory,
#                 variable_manager=self.variable_manager,
#                 loader=self.loader,
#                 options=self.options,
#                 passwords=self.passwords,
#                 stdout_callback='default',
#             )
#             tqm._stdout_callback = self.callback
#             result = tqm.run(play)
#         # print self.callback
#         finally:
#             if tqm is not None:
#                 tqm.cleanup()

#     def run_playbook(self, playbook_name,vars):
#         try:
#             self.callback = ResultsCollector()
#             playbook_file = [YML_DIR + playbook_name]

#             # template_file = BASE_DIR + "roles/"+ role_name + "/templates"
#             if not os.path.exists(playbook_name):
#                 logger.error('%s 路径不存在 ' % playbook_file)
#             self.variable_manager.vars= vars

#             executor = PlaybookExecutor(
#                 playbooks=playbook_file, inventory=self.inventory, variable_manager=self.variable_manager,
#                 loader=self.loader,options=self.options, passwords=self.passwords
#             )
#             executor._tqm._stdout_callback = self.callback
#             executor.run()
#         except Exception as e:
#             logger.error("Failure in run_playbook:%s"%e)
#             pass

#     def get_result(self):
#         self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
#         for host, result in self.callback.host_ok.items():
#             self.results_raw['success'][host] = result._result

#         for host, result in self.callback.host_failed.items():
#             self.results_raw['failed'][host] = result._result

#         for host, result in self.callback.host_unreachable.items():
#             self.results_raw['unreachable'][host] = result._result['msg']

#         return self.results_raw


def playbook_action(playbook, vars):
    resource = '/etc/ansible/hosts'
    variable_manager = VariableManager()
    loader = DataLoader()
    inventory = InventoryManager(loader=loader, sources=resource)
    inventory.clear_pattern_cache()
    Options = namedtuple('Options',
                         ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks',
                          'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                          'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check', 'diff'])
    options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                      module_path=None, forks=100, remote_user='root', private_key_file=None,
                      ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None,
                      become=True, become_method='sudo', become_user='root', verbosity=None, check=False,
                      diff=False)
    variable_manager = VariableManager(loader=loader, inventory=inventory)
    variable_manager.extra_vars = vars
    passwords = {}
    callback = ResultsCollector()
    pbex = PlaybookExecutor(playbooks=[playbook], inventory=inventory, variable_manager=variable_manager, loader=loader, options=options, passwords=passwords)
    pbex._tqm._stdout_callback = callback
    start_time = time.time()
    result = pbex.run()
    end_time = time.time()
    logger.error('ansible执行时间为: %s' % (end_time - start_time))
    results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
    # for host, result in callback.host_ok.items():
    #     results_raw['success'][host] = result._result

    for host, result in callback.host_failed.items():
        results_raw['failed'][host] = result._result

    for host, result in callback.host_unreachable.items():
        results_raw['unreachable'][host] = result._result['msg']
    logger.error(results_raw)

    # return results_raw


class ResultsCollector(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.host_failed[result._host.get_name()] = result
        # logger.error(json.dumps({host.name: result._result}, indent=4))
