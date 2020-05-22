import urllib
import logging
logger = logging.getLogger('sourceDns.webdns.views')


def docker(url):
    logger.error('开始下载docker,url:%s' % url)
    urllib.request.urlretrieve(url, "/opt/docker.tgz")


def kubeneter(url):
    logger.error('开始下载k8s,url:%s' % url)
    urllib.request.urlretrieve(url, "/opt/kubernet.tar.gz")


def etcd(url):
    logger.error('开始下载etcd,url:%s' % url)
    urllib.request.urlretrieve(url, "/opt/etcd.tar.gz")


def cni_plugins(url):
    logger.error('开始下载cni-plugins,url:%s' % url)
    urllib.request.urlretrieve(url, "/opt/cni-plugins.tgz")


def cfssl(url):
    urllib.request.urlretrieve(url, "/opt/cfssl")


def cfssljson(url):
    urllib.request.urlretrieve(url, "/opt/cfssljson")
