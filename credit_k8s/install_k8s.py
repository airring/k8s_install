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
        extra_vars = {}
        extra_vars['hostname'] = 'docker'
        playbook_action(filedir + '/initsys.yml', extra_vars)
        logger.error('docker初始化完成')

        extra_vars = {}
        extra_vars['hostname'] = 'docker'
        a = playbook_action(filedir + '/docker.yml', extra_vars)
        logger.error(a['failed'])
        if not a['failed']:
            logger.error('docker安装完成')
        else:
            logger.error('docker安装失败')
            logger.error(a['failed'])
            return "1"
    except Exception as e:
        logger.error(e)
        return "1"


def kube_master():
    try:
        extra_vars = {}
        extra_vars['hostname'] = 'kube-master'
        extra_vars['base_dir'] = filedir
        a = playbook_action(filedir + '/kube-master.yml', extra_vars)
        if not a['failed']:
            logger.error('kube-master安装完成')
        else:
            logger.error('kube-master安装失败')
            logger.error(a['failed'])
            return "1"
    except Exception as e:
        logger.error(e)
        return "1"


def kube_master_join():
    try:
        extra_vars = {}
        extra_vars['hostname'] = 'kube-master'
        extra_vars['base_dir'] = filedir
        a = playbook_action(filedir + '/kube-masterjoin.yml', extra_vars)
        if not a['failed']:
            logger.error('kube-master节点添加完成')
        else:
            logger.error('kube-master节点添加失败')
            logger.error(a['failed'])
            return "1"
    except Exception as e:
        logger.error(e)
        return "1"


def kube_node():
    extra_vars = {}
    extra_vars['hostname'] = 'kube-node'
    extra_vars['base_dir'] = filedir
    a = playbook_action(filedir + '/kube-node.yml', extra_vars)
    if not a['failed']:
        logger.error('kube-node安装完成')
    else:
        logger.error('kube-node安装失败')
        logger.error(a['failed'])
        return "1"


def kubeneter():
    pass


# plug
def helm():
    extra_vars = {}
    extra_vars['hostname'] = 'kube-master'
    extra_vars['base_dir'] = filedir
    a = playbook_action(filedir + '/helm.yml', extra_vars)
    if not a['failed']:
        logger.error('helm安装完成')
    else:
        logger.error('helm安装失败')
        logger.error(a['failed'])
        return "1"


def traefik_ingress():
    extra_vars = {}
    extra_vars['hostname'] = 'kube-master'
    extra_vars['base_dir'] = filedir
    a = playbook_action(filedir + '/traefik-ingress.yml', extra_vars)
    if not a['failed']:
        logger.error('traefik-ingress安装完成')
    else:
        logger.error('traefik-ingress安装失败')
        logger.error(a['failed'])
        return "1"


def efk():
    extra_vars = {}
    extra_vars['hostname'] = 'kube-master'
    extra_vars['base_dir'] = filedir
    a = playbook_action(filedir + '/efk.yml', extra_vars)
    if not a['failed']:
        logger.error('efk安装完成')
    else:
        logger.error('efk安装失败')
        logger.error(a['failed'])
        return "1"


def prometheus_operator():
    extra_vars = {}
    extra_vars['hostname'] = 'kube-master'
    extra_vars['base_dir'] = filedir
    a = playbook_action(filedir + '/prometheus-operator.yml', extra_vars)
    if not a['failed']:
        logger.error('prometheus-operator安装完成')
    else:
        logger.error('prometheus-operator安装失败')
        logger.error(a['failed'])
        return "1"


def ceph():
    extra_vars = {}
    extra_vars['hostname'] = 'ceph'
    extra_vars['base_dir'] = filedir
    a = playbook_action(filedir + '/ceph.yml', extra_vars)
    if not a['failed']:
        logger.error('ceph安装完成')
    else:
        logger.error('ceph安装失败')
        logger.error(a['failed'])
        return "1"


def add_cephsc():
    extra_vars = {}
    extra_vars['hostname'] = 'ceph'
    extra_vars['base_dir'] = filedir
    a = playbook_action(filedir + '/add_cephsc.yml', extra_vars)
    if not a['failed']:
        logger.error('add_cephsc安装完成')
    else:
        logger.error('add_cephsc安装失败')
        logger.error(a['failed'])
        return "1"
