CREATE TABLE `packet_install` (
  `packet_name` varchar(255) NOT NULL,
  `packet_url` varchar(255) NOT NULL,
  `version` varchar(255) NOT NULL,
  `install_id` int(3),
  PRIMARY KEY (`packet_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT  INTO `packet_install` (
	packet_name,
	packet_url,
	install_id
)
VALUES
	(
		'docker',
		'https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/static/stable/x86_64/docker-18.09.9.tgz',
	  '18.09.9'
		1
	),
  (
		'kubeneter',
		'https://storage.googleapis.com/kubernetes-release/release/v1.17.0/kubernetes-server-linux-amd64.tar.gz',
    'v1.17.0'
		1
	),
  (
   'etcd',
   'https://storage.googleapis.com/etcd/v3.3.18/etcd-v3.3.18-linux-amd64.tar.gz',
   'v3.3.18'
   1
)
