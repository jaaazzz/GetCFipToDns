### 功能介绍

本项目的主要功能是动态获取cf优选ip，并将域名实时解析到这些优选IP上，以达到网站使用cloudflare CDN并使用国内访问速度更快的CDN节点。

★ 动态获取cf优选ip的接口由vps789.com提供

★ 网站使用CF优选IP的教程参考：https://www.vpsjxw.com/vps_use/cloudflare_select_ip/

★ 本工具主要是将网站域名动态解析到获取到的优选ip上，目前支持阿里云DNS、DNSPod、华为云DNS、NameSilo

<br>

### CF优选IP接口(VPS789.com提供)

**CF优选IP机制说明：**

基于CloudFlareST工具生成一个[初选IP池]，vps789固定24小时监测200-500个IP。每天根据网络情况综合评估，淘汰1/3网络较差的IP，然后从[初选IP池]补充到vps789中继续监测。**通过持续补充优选IP和IP优胜略汰机制，保证vps789上的IP都是优中选优。**

★ 支持对cloudFlare IP进行延迟、丢包率、下载速度、晚高峰网络状态等多个维度的筛选

★ vps789优选IP监控页面地址：https://vps789.com/cfip

★ VPS789优选IP动态获取接口：https://vps789.com/public/sum/cfIpApi

<br>

### 使用方法

0.  需要python3、pip环境

1.  安装运行脚本所需依赖

      pip install -r requirements.txt


2.  登录DNS解析平台，获取 SecretId、SecretKey。如果使用NameSilo只用填SecretKey即可。

3.  将脚本下载到本地，修改启动文件runXXX.py中的SecretId、SecretKey

4.  修改脚本中域名配置信息，可配置多个域名和多个子域名，注意选择DNS服务商


5.  运行程序，如果能够正常运行可以选择cron定时执行(建议1个小时执行一次)

```python
#域名解析在阿里云DNS
python runAliDns.py
#域名解析在DnsPod
python runDnsPod.py
#域名解析在华为云DNS
python runHwDns.py
#域名解析在NameSilo
python runNameSilo.py
```
<br>

### 鸣谢
感谢以下项目提供技术支撑与实现思路

[cf2dns](https://github.com/ddgth/cf2dns)@ddgth

[CloudflareSpeedTest](https://github.com/XIU2/CloudflareSpeedTest)@XIU2
