### 功能介绍

本项目的主要功能是动态获取cf优选ip，并将域名实时解析到这些优选IP上，以达到网站使用cloudflare CDN并使用国内访问速度更快的CDN节点。

★ 动态获取cf优选ip的接口由vps789.com提供

★ 网站使用CF优选IP的教程参考：https://www.vpsjxw.com/vps_use/cloudflare_select_ip/

★ 本工具主要是将网站域名动态解析到获取到的优选ip上，目前支持阿里云DNS、DNSPod、华为云DNS、NameSilo

### VPS789.com提供CF优选IP接口
1、支持对CF优选IP的三网实时监测延迟、丢包率，支持查看24小时、一个月的监测数据。

2、支持对CF优选IP的下载速度进行测试

3、基于CloudFlareST工具生成一个优选IP池，vps789的优选IP每天定时淘汰1/3网络不好的IP，从优选IP池补充到vps789中继续监测。通过持续补充优选IP和IP优胜略汰机制，保证vps789上的IP都是优中选优。

4、vps789优选IP监控页面地址：https://vps789.com/cfip

### 使用方法

0.  需要python3、pip环境

1.  安装运行脚本所需依赖

```python
pip install -r requirements.txt
```

1.  登录DNS解析平台,获取 SecretId、SecretKey。
   如果使用阿里云DNS，注意需要添加DNS控制权限**AliyunDNSFullAccess**
   如果使用NameSilo只用填SecretKey即可。

2.  将脚本下载到本地修改start.py中的SecretId、SecretKey

3.  修改脚本中域名配置信息，可配置多个域名和多个子域名，注意选择DNS服务商


4.  运行程序，如果能够正常运行可以选择cron定时执行(建议1个小时执行一次)

```python
python start.py
```

### 鸣谢
感谢以下项目提供技术支撑与实现思路

[cf2dns](https://github.com/ddgth/cf2dns)@ddgth

[CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest)@XIU2
