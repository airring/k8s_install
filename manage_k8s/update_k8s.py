# coding=utf-8
import os
import logging
from script.playbook_runner import playbook_action
logger = logging.getLogger('sourceDns.webdns.views')

filedir = os.path.split(os.path.realpath(__file__))[0]


def ca():
    logger.error('进入证书方法')
    extra_vars = {}
    extra_vars['hostname'] = 'localhost'
    playbook_action(filedir + '/ca.yml', extra_vars)
    logger.error('ca证书生成完毕')


def etcd():
    # try:
    #     os.chdir('/opt')
    #     os.system('tar zxvf ./etc.tar.gz')
    #     os.system('find ./etcd* -name etcdctl -exec cp {} /opt/kube/bin \\;')
    #     os.system('find ./etcd* -name etcd -exec cp {} /opt/kube/bin \\;')
    #     logger.error('etcd文件解压完成')
    # except Exception as e:
    #     logger.error(e)
    extra_vars = {}
    extra_vars['hostname'] = 'etcd'
    playbook_action(filedir + '/initsys.yml', extra_vars)
    logger.error('etcd初始化完成')

    extra_vars = {}
    extra_vars['base_dir'] = '/opt/kube'
    playbook_action(filedir + '/etcd.yml', extra_vars)
    logger.error('etcd安装完成')


def docker():
    try:
        os.chdir('/opt')
        os.system('tar zxvf ./docker.tgz --strip-components=1 -C /opt/kube/bin')
        logger.error('docker文件解压完成')
    except Exception as e:
        logger.error(e)

    extra_vars = {}
    extra_vars['hostname'] = 'docker'
    playbook_action(filedir + '/initsys.yml', extra_vars)
    logger.error('docker初始化完成')

    extra_vars = {}
    extra_vars['hostname'] = 'docker'
    playbook_action(filedir + '/docker.yml', extra_vars)
    logger.error('docker安装完成')


def kubeneter():
    logger.error('进入k8s升级方法')
    try:
        os.chdir('/opt')
        os.system('tar zxvf ./kubernet.tar.gz ')
        os.system('find ./kubernetes -name kube-apiserver -exec cp {} /opt/kube/bin \\;')
        os.system('find ./kubernetes -name kube-controller-manager -exec cp {} /opt/kube/bin \\;')
        os.system('find ./kubernetes -name kube-scheduler -exec cp {} /opt/kube/bin \\;')
        os.system('find ./kubernetes -name kubectl -exec cp {} /opt/kube/bin \\;')
        os.system('find ./kubernetes -name kubelet -exec cp {} /opt/kube/bin \\;')
        os.system('find ./kubernetes -name kube-proxy -exec cp {} /opt/kube/bin \\;')
        logger.error('k8s文件解压完成')
    except Exception as e:
        logger.error(e)
    extra_vars = {}
    extra_vars['hostname'] = 'kubelet'
    extra_vars['base_dir'] = filedir
    playbook_action(filedir + '/update_kube.yml', extra_vars)
    logger.error('kubelet更新完成')


def add_kubnode(ip, hostname, username, password, port):
    # 添加配置到/etc/ansibe/hosts
    extra_vars = {}
    extra_vars['ip'] = ip
    extra_vars['hostname'] = 'localhost'
    extra_vars['node_name'] = hostname
    extra_vars['username'] = username
    extra_vars['password'] = password
    extra_vars['port'] = port
    a = playbook_action(filedir + '/addhost_node.yml', extra_vars)
    if not a['failed']:
        logger.error('hosts节点添加完成')
    else:
        logger.error('hosts节点添加失败')
        logger.error(a['failed'])
        return "1"
    # master节点读取token相关数据
    # 通过账号密码添加用户需要关闭ssh host认证
    # vi /etc/ansible/ansible.cfg
    # host_key_checking = False
    logger.error('====1============')
    extra_vars = {}
    a = playbook_action(filedir + '/kube-node-token.yml', extra_vars)
    if not a['failed']:
        logger.error('获取token成功')
    else:
        logger.error('获取token失败')
        logger.error(a['failed'])
        return "1"
    # 安装kube_node
    logger.error('=========2=======')
    extra_vars = {}
    extra_vars['hostname'] = ip
    a = playbook_action(filedir + '/add_node.yml', extra_vars)
    if not a['failed']:
        logger.error('kube-node添加完成')
    else:
        logger.error('kube-node添加失败')
        logger.error(a['failed'])
        return "1"
