Linux安装步骤
方法一：命令行部署
1、复制并在终端执行以下命令：
	wget --no-check-certificate https://管理平台IP:端口/download_installer_linux.php -O linux_aes_installer.tar.gz && tar -xzvf linux_aes_installer.tar.gz && ./agent_installer.sh -c
附录：端口默认是4430
2、执行完成，终端的agent程序将自动连接aES管理中心

方法二：下载器部署
1、点击下载安装包
2、将安装包拷贝至终端
3、在终端解压安装包 tar -xzvf linux_aes_installer.tar.gz
4、执行命令 ./agent_installer.sh
	a、无参安装（在同一目录中有manager_info.txt时使用）
		./agent_installer.sh
	b、自定义安装（安装域名、端口、路径均可选，可任意自由组合）
		./agent_installer.sh -f
		./agent_installer.sh -h www.mgr.com
		./agent_installer.sh -h www.mgr.com -p 443 -d /root/edr/ -f
		参数列表：
			-h host       自定义域名、IP
			-p port       自定义端口
			-d dir        自定义安装路径（绝对路径）
			-f            强制安装
			-o            全量安装包离线安装（全量安装时必须同时指定 域名和端口）
			-u            客户ID， SASE aES全量包安装需要用到此参数，本地aES全量包安装不需要此参数。
			--help        显示帮助文档
5、执行完成，终端的agent程序将自动连接aES管理中心