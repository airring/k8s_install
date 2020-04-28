# k8s_install
### python版本说明
因为python的ansible-playbook在python2和python3上使用方法上存在差异,所以统一使用python3

### hosts文件说明
hosts文件中因为分组名称在使用ansible安装时会通过分组名来获取服务ip,所以group名称最好不做修改,分组调用的文件会统一在defaults/main.yml下定义变量.
默认运行文件保存位置 /opt/kube/bin
默认证书文件保存位置 /opt/ssl

### 启动命令
'''
git clone https://github.com/airring/k8s_install
cd k8s_install
pip3 install -r ./requirements.txt
cp ./hosts /etc/ansible/hosts
python3 manage.py runserver 0.0.0.0:8080
'''
### 证书说明
因为证书文件不为统一生成,分别放置位置为:
ca : credit_k8s/roles/ca/templates
etcd : credit_k8s/roles/etcd/templates
admin : credit_k8s/roles/{kube-master,kube-node}/templates
kubelet : credit_k8s/roles/{kube-master,kube-node}/templates
aggregator-proxy : credit_k8s/roles/{kube-master,kube-node}/templates
kube-proxy : credit_k8s/roles/kube-node/templates
kubernetes : credit_k8s/roles/kube-master/templates
因为证书需要读取主机ip,所以分布存放,有些修改需要修改多处,后期修改.

### 二进制包安装问题
