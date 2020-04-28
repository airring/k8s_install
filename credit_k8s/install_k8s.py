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


def kube_init():
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


def kube_master():
    extra_vars = {}
    extra_vars['hostname'] = 'kube-master'
    extra_vars['base_dir'] = filedir
    playbook_action(filedir + '/kube-master.yml', extra_vars)
    logger.error('kube-master安装完成')


def kube_node():
    extra_vars = {}
    extra_vars['hostname'] = 'kube-node'
    extra_vars['base_dir'] = filedir
    playbook_action(filedir + '/kube-node.yml', extra_vars)
    logger.error('kube-node安装完成')


def kubeneter():
    pass
