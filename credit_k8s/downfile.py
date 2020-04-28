import urllib
import logging
logger = logging.getLogger('sourceDns.webdns.views')


def docker(version):

    url = 'https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/static/stable/x86_64/docker-%s.tgz' % version
    logger.error('开始下载docker,url:%s' % url)
    urllib.request.urlretrieve(url, "/opt/docker.tgz")


def kubeneter(version):
    url = 'https://storage.googleapis.com/kubernetes-release/release/%s/kubernetes-server-linux-amd64.tar.gz' % version
    logger.error('开始下载k8s,url:%s' % url)
    urllib.request.urlretrieve(url, "/opt/kubernet.tar.gz")


def etcd(version):
    url = 'https://storage.googleapis.com/etcd/{version}/etcd-{version}-linux-amd64.tar.gz'.format(version=version)
    logger.error('开始下载etcd,url:%s' % url)
    urllib.request.urlretrieve(url, "/opt/etcd.tar.gz")


def down_cfssl():
    url = 'https://pkg.cfssl.org/R1.2/cfssl_linux-amd64'
    url2 = 'https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64'
    url3 = 'https://pkg.cfssl.org/R1.2/cfssl-certinfo_linux-amd64'
    urllib.request.urlretrieve(url, "/opt/cfssl")
    urllib.request.urlretrieve(url2, "/opt/cfssljson")
    urllib.request.urlretrieve(url3, "/opt/cfssl-certinfo")
