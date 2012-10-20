#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""通过 ping 命令找出响应时间最快的 ip 或域名
只支持 windows
"""

import subprocess


def ping(host):
    """返回 ping 结果
    host 参数应为字符串类型的 ip 或域名
        '192.168.1.1' or 'www.baidu.com'
    返回 host, ip, time, lost
        host：域名，字符串类型
        ip：字符串类型，默认值为'0.0.0.0'
        time：平均响应时间（ms），int 类型，默认值为0
        lost：平均丢包率（%），int 类型，默认值为0
    返回值示例：
        ('www.baidu.com', '0.0.0.0', 0, 0)
    """
    import re
    cmd = 'ping ' + host
    # 执行 ping 命令，并获取命令执行结果
    sub = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out = sub.communicate()[0]
    # 替换换行符，因为在正则表达式中
    # 'a$' 匹配 'a\r\n' 中的 'a\r'
    text = out.replace('\r\n', '\n')
    ip = '0.0.0.0'
    lost, time = 0, 0
    try:
        # 使用正则表达式提取信息
        ip = re.search(r'^\d+\.\d+\.\d+\.\d+\b', text, re.M).group()
        time = int(re.search(r'\d+(?=ms$)', text).group())
        lost = int(re.search(r'\d+(?=%)', text).group())
    except:
        pass
    return host, ip, time, lost


def get_hosts(filename):
    """从文件中读取 ip/域名
    """
    hosts = list()
    with open(filename) as f:
        for line in f:
            line = line.strip().strip('.,/')
            if line:
                hosts.append(line)
    return hosts

if __name__ == '__main__':
    import sys
    import os
    import re
    # 处理命令行参数
    argvs = sys.argv
    leng = len(argvs)
    hosts = list()
    filename = 'hosts.txt'
    add = False
    ips = list()
    if leng >= 2:
        name = argvs[1]
        if os.path.isfile(name):
            filename = name
            if leng > 2:
                if argvs[2] == '+':
                    add = True
                    ips = argvs[3:]
                else:
                    ips = argvs[2:]
        else:
            if name == '+':
                add = True
                ips = argvs[2:]
            else:
                ips = argvs[1:]
        if ips:
            for s in ips:
                name = s.strip('.,/')
                name = re.sub(r'https?://', '', name)
                hosts.append(name)
    if not hosts and not os.path.isfile(filename):
        sys.exit('No ip or the file("%s") not existed!' % (filename))
    if not hosts:
        hosts = get_hosts(filename)
    if add:
        hosts = list(set(get_hosts(filename) + hosts))
    if not hosts:
        sys.exit('Not find ip/host')
    result_time = dict()
    print '#' * 50
    print 'host(ip)'.rjust(33), 'time    lost'.rjust(14)
    for x in hosts:
        host, ip, time, lost = ping(x)
        result_time.update({host: time})
        print ('%s(%s): ' % (host, ip)).rjust(35), ('% 3sms   % 2s%%'
                                                    ) % (time, lost)
    times = sorted(result_time.itervalues())
    times = [i for i in times[:] if i]
    print '#' * 50
    if times:
        for k, v in result_time.iteritems():
            if v == times[0]:
                print '%s has the min ping time: %s ms' % (k, v)
    # else:
        # print 'The ping result are timeout'
    raw_input('>')
