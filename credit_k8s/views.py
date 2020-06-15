from django.shortcuts import render
# from django.shortcuts import redirect
from django.http import JsonResponse
# from django.template import RequestContext, Context
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
# from script.pymysql import ConnectionPool
from credit_k8s import downfile, install_k8s
import logging
logger = logging.getLogger('sourceDns.webdns.views')


def index(request, template='index.html'):
    return render(request, template)


def init(request, template='init.html'):
    packet = [
        # {'packet_name': 'cni_plugins',
        #  'packet_url': 'https://github.com/containernetworking/plugins/releases/download/v0.8.5/cni-plugins-linux-amd64-v0.8.5.tgz',
        #  'version': '0'},
        {'packet_name': 'cfssl',
         'packet_url': 'https://pkg.cfssl.org/R1.2/cfssl_linux-amd64',
         'version': '1.2.0'},
        {'packet_name': 'cfssljson',
         'packet_url': 'https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64',
         'version': '1.2.0'}
        # {'packet_name': 'crictl',
        #  'packet_url': 'https://github.com/kubernetes-sigs/cri-tools/releases/download/v1.18.0/crictl-v1.18.0-linux-amd64.tar.gz',
        #  'version': '1.18.0'
        #  }
        ]
    # pool = ConnectionPool()
    # packet_install = pool.execute("select * from packet_install")

    context = {
        'packet': packet
    }
    return render(request, template, context)


def init_2(request, template='init_2.html'):
    packet_install = ['ca', 'etcd', 'docker', 'kube_master', 'kube_master_join', 'kube_node']
    logger.error(packet_install)
    context = {
        'packet': packet_install
    }
    return render(request, template, context)


@csrf_exempt
def init_api(request):
    pk_version = json.loads(request.body)
    name = pk_version['name']
    version = pk_version['version']

    try:
        getattr(downfile, name)(version)
        context = {
            'status': 1,
            'name': name
        }
        logger.error('%s文件下载完成' % name)
    except Exception as e:
        logger.error(e)
        context = {
            'status': 2,
            'name': name
        }
        logger.error('%s文件下载失败' % name)

    return JsonResponse(context)


# 项目安装
@csrf_exempt
def install_packet(request):
    pk_version = json.loads(request.body)
    name = pk_version['name']
    logger.error(name)
    a = getattr(install_k8s, name)()
    if a == "1":
        context = {
         'msg': '发布失败',
         'status': 2,
         'name': name
        }
    else:
        context = {
         'status': 1,
         'name': name
        }
    return JsonResponse(context)


# 插件安装页面
def init_publ(request, template='init_publ.html'):
    packet_install = ['helm', 'traefik_ingress', 'efk', 'prometheus_operator']
    logger.error(packet_install)
    context = {
        'packet': packet_install
    }
    return render(request, template, context)


# 插件安装
@csrf_exempt
def init_publ_api(request):
    pk_version = json.loads(request.body)
    name = pk_version['name']
    logger.error(name)
    a = getattr(install_k8s, name)()
    if a == "1":
        context = {
         'msg': '发布失败',
         'status': 2,
         'name': name
        }
    else:
        context = {
         'status': 1,
         'name': name
        }
    return JsonResponse(context)


# ceph安装页面
def init_ceph(request, template='init_ceph.html'):
    packet_install = ['ceph','add_cephsc']
    logger.error(packet_install)
    context = {
        'packet': packet_install
    }
    return render(request, template, context)


# ceph安装
@csrf_exempt
def init_ceph_api(request):
    pk_version = json.loads(request.body)
    name = pk_version['name']
    logger.error(name)
    a = getattr(install_k8s, name)()
    if a == "1":
        context = {
         'msg': '发布失败',
         'status': 2,
         'name': name
        }
    else:
        context = {
         'status': 1,
         'name': name
        }
    return JsonResponse(context)