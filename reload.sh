#逐个启动MyWeb每个端口进程，不中断服务

/usr/local/bin/supervisorctl  -c /root/works/spide_script/supervisor_spide.conf restart baidu_search;

#重新加载nginx的配置
/usr/local/nginx/sbin/nginx -s reload;