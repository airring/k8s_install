from django.shortcuts import render
# from django.shortcuts import redirect
from django.http import JsonResponse
# from django.template import RequestContext, Context
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
import json
from script.pymysql import ConnectionPool
from credit_k8s import downfile, install_k8s
import logging
logger = logging.getLogger('sourceDns.webdns.views')


def index(request, template='index.html'):
    return render(request, template)


def init(request, template='init.html'):
    pool = ConnectionPool()
    packet_install = pool.execute("select * from packet_install")
    context = {
        'packet': packet_install
    }
    return render(request, template, context)


def init_2(request, template='init_2.html'):
    packet_install = ['ca', 'etcd', 'docker', 'kube_init', 'kube_master', 'kube_node']
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
    except Exception as e:
        logger.error(e)
        context = {
            'status': 2,
            'name': name
        }

    logger.error('%s文件下载完成' % name)
    return JsonResponse(context)


# 项目安装
@csrf_exempt
def install_packet(request):
    pk_version = json.loads(request.body)
    name = pk_version['name']
    logger.error(name)
    try:
        getattr(install_k8s, name)()
        context = {
            'status': 1,
            'name': name
        }
    except Exception as e:
        logger.error(e)
        context = {
            'status': 2,
            'name': name
        }

    return JsonResponse(context)
