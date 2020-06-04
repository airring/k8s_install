from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
import manage_k8s.update_k8s as update_k8s
logger = logging.getLogger('sourceDns.webdns.views')


# Create your views here.
def update(request, template='update.html'):
    packet = [{
        'packet_name': 'docker',
        'packet_url': 'https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/static/stable/x86_64/docker-18.09.9.tgz',
        'version': '18.09.9'},
        {'packet_name': 'etcd',
         'packet_url': 'https://storage.googleapis.com/etcd/v3.3.18/etcd-v3.3.18-linux-amd64.tar.gz',
         'version': 'v3.3.18'},
        {'packet_name': 'kubeneter',
         'packet_url': 'https://storage.googleapis.com/kubernetes-release/release/v1.18.2/kubernetes-server-linux-amd64.tar.gz',
         'version': 'v1.18.2'},
        {'packet_name': 'cni_plugins',
         'packet_url': 'https://github.com/containernetworking/plugins/releases/download/v0.8.5/cni-plugins-linux-amd64-v0.8.5.tgz',
         'version': '0'},
        {'packet_name': 'cfssl',
         'packet_url': 'https://pkg.cfssl.org/R1.2/cfssl_linux-amd64',
         'version': '1.2.0'},
        {'packet_name': 'cfssljson',
         'packet_url': 'https://pkg.cfssl.org/R1.2/cfssljson_linux-amd64',
         'version': '1.2.0'}]
    # pool = ConnectionPool()
    # packet_install = pool.execute("select * from packet_install")

    context = {
        'packet': packet
    }
    return render(request, template, context)


@csrf_exempt
def update_api(request):
    logger.error('进入更新方法')
    pk_version = json.loads(request.body)
    pk_name = pk_version['name']
    try:
        getattr(update_k8s, pk_name)()
        context = {
                'status': 1,
                'name': pk_name
            }
    except Exception as e:
        logger.error(e)
        context = {
                'status': 2,
                'name': pk_name
            }
    return JsonResponse(context)


def add_node(request, template='add_node.html'):

    return render(request, template)


def add_master(request, template='add_master.html'):

    return render(request, template)


@csrf_exempt
def add_node_api(request):
    logger.error('进入添加节点方法')
    pk_version = json.loads(request.body)
    ip = pk_version.get('ip')
    hostname = pk_version.get('hostname')
    username = pk_version.get('username')
    port = pk_version.get('port')
    nopass = pk_version.get('nopass')
    addhost = 'addhost_node'
    if nopass:
        password = ''
    else:
        password = pk_version.get('password')
    logger.error(pk_version)
    logger.error('====')
    try:
        getattr(update_k8s, 'add_kubnode')(ip, hostname, username, password, port, addhost)
        context = {
                'status': 1,
                'name': ip
            }
    except Exception as e:
        logger.error(e)
        context = {
                'status': 2,
                'name': ip
            }
    return JsonResponse(context)


@csrf_exempt
def add_master_api(request):
    logger.error('进入添加节点方法')
    pk_version = json.loads(request.body)
    ip = pk_version.get('ip')
    hostname = pk_version.get('hostname')
    username = pk_version.get('username')
    port = pk_version.get('port')
    nopass = pk_version.get('nopass')
    addhost = 'addhost_master'
    if nopass:
        password = ''
    else:
        password = pk_version.get('password')
    logger.error(pk_version)
    logger.error('====')
    try:
        getattr(update_k8s, 'add_kubnode')(ip, hostname, username, password, port, addhost)
        context = {
                'status': 1,
                'name': ip
            }
    except Exception as e:
        logger.error(e)
        context = {
                'status': 2,
                'name': ip
            }
    return JsonResponse(context)