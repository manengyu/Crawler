# -*- coding: utf8 -*-

import MySQLdb
import pandas as pd
import threading
import requests
import urllib
import re
import traceback
import random
import datetime
import time
import json
import hashlib
import lxml.html
import sys
reload(sys)
import chardet
sys.setdefaultencoding("utf-8")


def insert_GONG_PLAT_COMPANY_IC_DATA(conn, cur, COMPANY_NAME, IC_DATA, SHAREHOLDER_DATA, PRINCIPAL_DATA, INVESTMENT_ABROAD, SOURCE_URL):
    UPDATE_DATE = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    insert_sql = "INSERT INTO GONG_PLAT_COMPANY_IC_DATA ( COMPANY_NAME, IC_DATA, SHAREHOLDER_DATA," \
                 " PRINCIPAL_DATA, INVESTMENT_ABROAD, SOURCE_URL, UPDATE_DATE) VALUES ('" + COMPANY_NAME + "','" +\
                 IC_DATA + "','" + SHAREHOLDER_DATA + "','" + PRINCIPAL_DATA + "','" + INVESTMENT_ABROAD + "','" +\
                 SOURCE_URL + "','" + UPDATE_DATE + "')"
    try:
        cur.execute(insert_sql)
        conn.commit()
    except:
        traceback.print_exc()
        pass


def insert_GONG_PLAT_COMPANY_IC_DATA21(conn21, cur21, COMPANY_NAME, IC_DATA, SHAREHOLDER_DATA, PRINCIPAL_DATA, INVESTMENT_ABROAD, SOURCE_URL):
    UPDATE_DATE = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    insert_sql = "INSERT INTO GONG_PLAT_COMPANY_IC_DATA ( COMPANY_NAME, IC_DATA, SHAREHOLDER_DATA," \
                 " PRINCIPAL_DATA, INVESTMENT_ABROAD, SOURCE_URL, UPDATE_DATE) VALUES ('" + COMPANY_NAME + "','" +\
                 IC_DATA + "','" + SHAREHOLDER_DATA + "','" + PRINCIPAL_DATA + "','" + INVESTMENT_ABROAD + "','" +\
                 SOURCE_URL + "','" + UPDATE_DATE + "')"
    try:
        cur21.execute(insert_sql)
        conn21.commit()
    except:
        traceback.print_exc()
        pass


def insert_business_info(conn, cur, credit_code, name, tax_no, no, org_no, oper_name, regist_capi, status,
                         start_date, econ_kind, bus_people, term, belong_org, check_date, eng_name, belong_area,
                         belong_industry, address, scope):
    day_date = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    create_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    insert_sql = "INSERT INTO ma.business_info (credit_code, name, tax_no, no, org_no, oper_name, regist_capi," \
                 " status, start_date, econ_kind, bus_people, term, belong_org, check_date, eng_name, belong_area," \
                 " belong_industry, address, scope) VALUES ('" + credit_code + "','" + name + "','" + tax_no + "','" +\
                 no + "','" + org_no + "','" + oper_name + "','" + regist_capi + "','" + status + "','" + start_date +\
                 "','" + econ_kind + "','" + bus_people + "','" + term + "','" + belong_org + "','" + check_date +\
                 "','" + eng_name + "','" + belong_area + "','" + belong_industry + "','" + address + "','" + scope\
                 + "')"
    cur.execute(insert_sql)
    conn.commit()


def insert_business_shareholder(conn, cur, credit_code, stock_name, stock_percent, should_capi, should_date, stock_type):
    insert_sql = "INSERT INTO ma.business_shareholder (credit_code, stock_name, stock_percent, should_capi, " \
                 "should_date, stock_type) VALUES ('" + credit_code + "','" + stock_name + "','" + stock_percent +\
                 "','" + str(should_capi) + "','" + str(should_date) + "','" + str(stock_type) + "')"
    cur.execute(insert_sql)
    conn.commit()


def insert_business_managers(conn, cur, credit_code, name, post):
    insert_sql = "INSERT INTO ma.business_managers (credit_code, name, post) VALUES ('" + credit_code +\
                 "','" + str(name) + "','" + str(post) + "')"
    cur.execute(insert_sql)
    conn.commit()


def insert_business_judgementdoc(conn, cur, credit_code, case_name, pub_date, case_no, case_identity, court):
    insert_sql = "INSERT INTO ma.business_judgementdoc (credit_code, case_name, pub_date, case_no, case_identity, " \
                 "court) VALUES ('" + credit_code + "','" + case_name + "','" + pub_date + "','" + case_no + "','" +\
                 str(case_identity) + "','" + str(court) + "')"
    cur.execute(insert_sql)
    conn.commit()


def insert_business_court_announcement(conn, cur, credit_code, publish_date, type, party, content):
    insert_sql = "INSERT INTO ma.business_managers (credit_code, publish_date, type, party, content) VALUES ('" +\
                 credit_code + "','" +publish_date + "','" + type + "','" + party + "','" + content + "')"
    cur.execute(insert_sql)
    conn.commit()


def insert_business_enforced(conn, cur, credit_code, name, register_date, court, subject):
    insert_sql = "INSERT INTO ma.business_managers (credit_code, name, register_date, court, subject) VALUES ('" +\
                 credit_code + "','" + name + "','" + register_date + "','" + court + "','" + subject + "')"
    cur.execute(insert_sql)
    conn.commit()


def insert_begincourt_announcement(conn, cur, credit_code, begin_date, cause, accuser, accused, case_no, area,
                                   schedule_date, department, judge, court, court_ting):
    insert_sql = "INSERT INTO ma.business_managers (credit_code, begin_date, cause, accuser, accused, case_no, " \
                 "area, schedule_date, department, judge, court, court_ting) VALUES ('" + credit_code + "','" +\
                 begin_date + "','" + cause + "','" + accuser + "','" + accused + "','" + case_no + "','" + area +\
                 "','" + schedule_date + "','" + department + "','" + judge + "','" + court + "','" + court_ting + "')"
    cur.execute(insert_sql)
    conn.commit()


def insert_penalty_industry(conn, cur, credit_code, reference_no, type, content, decision_org, decision_date):
    insert_sql = "INSERT INTO ma.business_managers (credit_code, reference_no, type, content, decision_org," \
                 " decision_date) VALUES ('" + credit_code + "','" +  reference_no, type, content +\
                 "','" + decision_org + "','" + decision_date + "')"
    cur.execute(insert_sql)
    conn.commit()


def insert_penalty_china(conn, cur, credit_code, name, area, decision_date):
    insert_sql = "INSERT INTO ma.business_managers (credit_code, name, area, decision_date) VALUES ('" +\
                 credit_code + "','" +  name + "','" +  area + "','" + decision_date + "')"
    cur.execute(insert_sql)
    conn.commit()


def insert_abnormal(conn, cur, credit_code, in_date, out_date, decision_org, out_org, in_cause, out_cause):
    insert_sql = "INSERT INTO ma.business_managers (credit_code, in_date, out_date, decision_org, out_org," \
                 " in_cause, out_cause) VALUES ('" + credit_code + "','" + in_date + "','" + out_date + "','" +\
                 decision_org + "','" + out_org + "','" + in_cause + "','" + out_cause + "')"
    cur.execute(insert_sql)
    conn.commit()


def climb_info(conn_ma, cur, content, r):
    try:
        credit_code = re.findall("统一信用代码：<span><span.*?class=\"c8\"></span>(.+?)<", content)[0].strip().replace("未公开", "-")
        print credit_code
        tax_no = re.findall("纳税人识别号：.*?<span>(.+?)<", content)[0].strip().replace("未公开", "-")
        no = re.findall("工商注册号：<span>(.+?)<", content)[0].strip().replace("未公开", "-")
        org_no = re.findall("组织机构代码：<span>(.+?)<", content)[0].strip().replace("未公开", "-")
        oper_name = re.findall("onclick=\"common\.stopPropagation\(event\)\">\s*(.*?)<", content)[0].strip().replace("未公开", "-")
        regist_capi = re.findall("company.regCapital\)}}\".*?class=\"baseinfo-module-content-value\">\s*(.*?)<", content)[0].strip().replace("未公开", "-")
        status = re.findall("baseinfo-module-content-value statusType.*?>\s*(.*?)\s*<", content)[0].strip().replace("未公开", "-")
        start_date = re.findall("注册时间</div>.*?<div class=\"pb10\">.*?<div.*?title=\"([未公开|\d-]+)", content)[0].strip().replace("未公开", "-")
        econ_kind = re.findall("企业类型：<span>\s*(.+?)\s*<", content)[0].strip().replace("未公开", "-")
        # bus_people = re.findall("人员规模：</td> <td class=\"ma_left\">\s*([\d-]+)", content)[0].strip()
        term = re.findall("营业期限：.*?>\s*(.+?)\s*<", content)[0].strip().replace(" ", "").replace("未公开", "-")
        belong_org = re.findall("登记机关：<span>\s*(.+?)\s*<", content)[0].strip().replace("未公开", "-")
        check_date = re.findall("核准日期：.*?<span>\s*(.+?)\s*<", content)[0].strip().replace("未公开", "-")
        # eng_name = re.findall("英文名：</td> <td class=\"ma_left\" style=\"max-width:301px;\">\s*(.+?)\s*?", content)[0].strip()
        # belong_area = re.findall("所属地区\s*</td> <td class=\"ma_left\">\s*(.+?)\s*<", content)[0].strip()
        belong_industry = re.findall("行业：<span>\s*(.+?)\s*<", content)[0].strip().replace("未公开", "-")
        address = re.findall("注册地址：<span>\s*(.+?)\s*<", content)[0].strip().replace("查看地图", "").replace("未公开", "-")
        scope = re.findall("<span ng-if=\"!showDetail\" ng-bind-html=\"perContent\|splitNum\" class=\"js-full-container.*?>\s*(.+?)\s*<", content)[0].strip().replace("未公开", "-")
        # try:
        #     before_name = re.findall("企业地址：</td> <td class=\"ma_left\" colspan=\"3\">\s*(.+?)\s*<", content)[0].strip()
        # except:
        #     traceback.print_exc()
        #     pass
        try:
            # print chardet.detect(json.dumps({"统一社会信誉代码：": credit_code,"注册号：": no,"组织机构代码：": org_no,
            #                      "经营状态：":status,"法定代表人：":oper_name,"注册资本：":regist_capi,"公司类型：":econ_kind,"成立日期：":start_date,"营业期限：":term,\
            #  "登记机关：":belong_org,"发照日期：":check_date,"公司规模：":bus_people,"所属行业：":belong_industry,"英文名：":eng_name,"曾用名：":before_name,"企业地址：":address,"经营范围：":scope}, ensure_ascii=False).encode('utf-8')), chardet.detect(before_name)
            # print credit_code, name, tax_no, no, org_no, oper_name, regist_capi, status,start_date, econ_kind, bus_people, term, belong_org, check_date, eng_name, belong_area, belong_industry, address, scope
            return credit_code, {"统一社会信誉代码：": credit_code,"注册号：": no,"组织机构代码：": org_no,
                                 "经营状态：":status,"法定代表人：":oper_name,"注册资本：":regist_capi,"公司类型：":econ_kind,"成立日期：":start_date,"营业期限：":term,\
             "登记机关：":belong_org,"发照日期：":check_date,"所属行业：":belong_industry,"企业地址：":address,"经营范围：":scope}
            # insert_business_info(conn_ma, cur, credit_code, name, tax_no, no, org_no, oper_name, regist_capi, status,
            #                      start_date, econ_kind, bus_people, term, belong_org, check_date, eng_name, belong_area,
            #                      belong_industry, address, scope)
        except:
            traceback.print_exc()
            return False
    except:
        traceback.print_exc()
        return False


def climb_shareholder(conn_ma, cur, content, r):
    stock_name = re.findall("class=\"in-block vertival-middle overflow-width\" title=\"(.+?)\"", content)
    # should_capi = re.findall("([\d.-]+)\s*<br/> </td> <td class=\"text-center\">", content)
    # should_date = re.findall("<br/> </td> <td class=\"text-center\">\s*(.*?)\s*<", content)
    stock_percent = re.findall("<div\s*>\s*<span class=\"c-money-y\">\s*(.+?)\s*<", content)
    capi_date = re.findall("<span class=\"\">[(人民币)]*([\d.,]+)[万|万元|万\s*人民币|万元\s*人民币]*\s*</span>.*?<span\s*>时间：([\d-]+)</span\s*>", content)
    capi = re.findall("<div\s*>\s*<span class=\"\">[(人民币)]*([\d.,]+)[万|万元|万\s*人民币|万元\s*人民币]*</span\s*>\s*</div\s*>", content)
    # stock_type = re.findall("</td> <td class=\"text-center\">(.*?)</td> </tr> <tr>", content)
    if len(capi) == 0:        # capi = re.findall("<div >\s*<span class=\"\">([\d.,]+)万元*</span>\s*</div>", content)
        if len(stock_percent) > len(capi_date):
            for i in range(0, len(stock_percent) - len(capi_date)):
                capi_date.append(("-", "-"))
    elif len(stock_percent) > len(capi):
        for i in range(0, len(stock_percent) - len(capi)):
            capi.append("-")
    if len(capi) != 0 and len(capi_date) != 0:
        for i in capi:
            capi_date.append((i.replace(",", "").replace("未公开", "-"), ""))
    re_dic = {}
    for nu, i in enumerate(stock_name):
        try:
            if len(capi_date) == 0:
                re_dic[stock_name[nu]] = capi[nu].replace(",", "").replace("未公开", "-") + "万元人民币" + "|-|" + stock_percent[nu].replace("未公开", "-")
            elif capi_date[nu][0].replace(" ", "") != "未公开":
                re_dic[stock_name[nu]] = capi_date[nu][0].replace(",", "") + "万元人民币" + "|" + capi_date[nu][1].replace("未公开", "-") + "|" + stock_percent[nu].replace("未公开", "-")
            else:
                re_dic[stock_name[nu]] = capi_date[nu][0].replace(",", "").replace("未公开", "-") + "|" + capi_date[nu][1].replace("未公开", "-") + "|" + stock_percent[nu].replace("未公开", "-")
            re_dic[stock_name[nu]] = re_dic[stock_name[nu]].replace("-万元人民币", "-")
            # insert_business_shareholder(conn_ma, cur, credit_code, stock_name[nu], stock_percent[nu], should_capi[nu], should_date[nu], stock_type[nu])
        except:
            traceback.print_exc()
            continue
    return re_dic


def climb_managers(conn_ma, cur, content, r):
    try:
        name = re.findall("href=\"/human/[\w-]+\" target=\"_blank\" >\s*(.*?)\s*<", content)
        post = re.findall("solid #E2E7E8\">.*?<span >(.+?)</div>", content)
        re_list = []
        for nu, i in enumerate(name):
            try:
                # print credit_code, name[nu], post[nu]
                re_list.append({post[nu].replace(" ", "").replace("<span>", "").replace("</span>", "").replace("未公开", "-").replace("未知, 未知", "-").replace("未知", "-"): name[nu].replace("未公开", "-")})
                # insert_business_managers(conn_ma, cur, credit_code, name[nu], post[nu])
            except:
                traceback.print_exc()
                continue
        return re_list
    except:
        print url
        traceback.print_exc()
        return False


def climb_judgementdoc(conn_ma, cur, credit_code, plat_name, url, r):
    unique = re.findall("_([A-Za-z0-9]{10,40})", url)
    try:
        url_susong = "http://www.qichacha.com/company_getinfos?unique=" + unique[0] + "&companyname=" + urllib.quote(plat_name) + "&tab=susong"
        total_page = re.findall("susong\",\"wenshu\"\)'.*?([\d]+?)<", r.get(url_susong).content)
        if len(total_page) == 0:
            total_page = ["1"]
        for i in range(1, int(total_page[-1]) + 1):
            content = r.get(url_susong + "&box=wenshu&p=" + str(i)).content
            # id = re.findall("onclick='wsView\(\"(\w+?)\"\)", content)
            # content = r.post("http://www.qichacha.com/company_wenshuView", data={"id": "498bc1eeb1944bfae5b125ca842df512"}).content #裁判文书详细信息
            case_name = re.findall("\"\)'>(.+?)</a></td> ", content)
            pub_date = re.findall("<td width=\"13%\">([\d-]+?)<", content)
            case_no = re.findall("<td width=\"15%\">(.*?)<", content)
            case_identity = re.findall("<td width=\"24%\">(.*?)</td>", content)
            court = re.findall("</div> </td> <td width=\"15%\">(.*?)</td> </tr>", content)
            for nu, i in enumerate(case_identity):
                case_identity[nu] = "".join(re.findall("[^\u4e00-\u9fa5]", check_illegal(case_identity[nu])))
            if len(case_name):
                for nu, i in enumerate(case_name):
                    # print i, pub_date[nu], case_no[nu], court[nu]
                    try:
                        insert_business_judgementdoc(conn_ma, cur, credit_code, case_name[nu], pub_date[nu], case_no[nu], case_identity[nu], court[nu])
                    except:
                        continue
            else:
                print "暂无数据,裁判文书"
                break
        return True
    except:
        traceback.print_exc()
        return False


def climb_court_announcement(conn_ma, cur, credit_code, plat_name, url, r):
    unique = re.findall("_([A-Za-z0-9]{10,40})", url)
    try:
        url_susong = "http://www.qichacha.com/company_getinfos?unique=" + unique[0] + "&companyname=" + urllib.quote(plat_name) + "&tab=susong"
        total_page = re.findall("susong\",\"gonggao\"\)'.*?([\d]+?)<", r.get(url_susong).content)
        if len(total_page) == 0:
            total_page = ["1"]
        for i in range(1, int(total_page[-1]) + 1):
            content = r.get(url_susong + "&box=gonggao&p=" + str(i)).content
            publish_date = re.findall("<td width=\"15%\">([\d-]+?)<", content)
            type = re.findall("<td width=\"15%\">([\D]+?)</td> <td width=\"20%\">", content)
            party = re.findall("</td> <td width=\"20%\">(.*?)</td> <td width=\"40%\">", content)
            bis_content = re.findall("<span class=\"ma_court\">(.*?)</td> </tr>", content.replace("\n", ""))
            if len(publish_date):
                for nu, i in enumerate(publish_date):
                    print publish_date[nu], type[nu], party[nu], bis_content[nu]
                    try:
                        insert_business_court_announcement(conn_ma, cur, credit_code, publish_date[nu], type[nu], party[nu], bis_content[nu])
                    except:
                        continue
            else:
                print "暂无数据,法院公告"
                break
        return True
    except:
        traceback.print_exc()
        return False


def climb_enforced(conn_ma, cur, credit_code, plat_name, url, r):
    unique = re.findall("_([A-Za-z0-9]{10,40})", url)
    try:
        url_susong = "http://www.qichacha.com/company_getinfos?unique=" + unique[0] + "&companyname=" + urllib.quote(plat_name) + "&tab=susong"
        total_page = re.findall("susong\",\"zhixing\"\)'.*?([\d]+?)<", r.get(url_susong).content)
        if len(total_page) == 0:
            total_page = ["1"]
        for i in range(1, int(total_page[-1]) + 1):
            content = r.get(url_susong + "&box=zhixing&p=" + str(i)).content
            name = re.findall("</td><td>(.+?)<", content)
            register_date = re.findall("</td> <td>([\d-]+?)</td> <td>", content)
            court= re.findall("</td> <td>([\D]*?)</td> <td>", content)
            subject = re.findall("</td> <td>([\d]*?)</td> </tr>", content)
            if len(name):
                for nu, i in enumerate(name):
                    # print name[nu], register_date[nu], court[nu], subject[nu]
                    try:
                        insert_business_enforced(conn_ma, cur, credit_code, name[nu], register_date[nu], court[nu], subject[nu])
                    except:
                        continuev
            else:
                print "暂无数据,被执行人信息"
                break
        return True
    except:
        traceback.print_exc()
        return False


def climb_begincourt_announcement(conn_ma, cur, credit_code, plat_name, url, r):
    unique = re.findall("_([A-Za-z0-9]{10,40})", url)
    try:
        url_susong = "http://www.qichacha.com/company_getinfos?unique=" + unique[0] + "&companyname=" + urllib.quote(plat_name) + "&tab=susong"
        total_page = re.findall("susong\",\"notice\"\)'.*?([\d]+?)<", r.get(url_susong).content)
        if len(total_page) == 0:
            total_page = ["1"]
        for i in range(1, int(total_page[-1])+1):
            url_notice = url_susong + "&box=notice&p=" + str(i)
            ktnoticeView = re.findall("ktnoticeView\(\"([\w]+?)\"\)", r.get(url_notice).content)
            if len(ktnoticeView) == 0:
                print "暂无数据,开庭公告"
                return True
            for j in ktnoticeView:
                notice_json = json.loads(r.post("https://www.qichacha.com/company_ktnoticeView", data={"id": j}).content)
                begin_date = notice_json["data"]["open_time"]
                cause = notice_json["data"]["case_reason"]
                accuser = accused = ""
                for k in notice_json["data"]["prosecutor"]:
                    accuser += "," + k["name"]
                for k in notice_json["data"]["defendant"]:
                    accused += "," + k["name"]
                case_no = notice_json["data"]["case_no"]
                area = notice_json["data"]["province"]
                schedule_date = notice_json["data"]["schedule_time"]
                department = notice_json["data"]["undertake_department"]
                judge = notice_json["data"]["chief_judge"]
                court = notice_json["data"]["execute_gov"]
                court_ting = notice_json["data"]["execute_unite"]
                # print begin_date, cause, accuser, accused, case_no, area, schedule_date, department, judge, court, court_ting
                try:
                    insert_begincourt_announcement(conn, cur, credit_code, begin_date, cause, accuser, accused, case_no, area, schedule_date, department, judge, court, court_ting)
                except:
                    continue
            break
        return True
    except:
        traceback.print_exc()
        return False


def climb_penalty(conn_ma, cur, credit_code, plat_name, url, r):
    unique = re.findall("_([A-Za-z0-9]{10,40})", url)
    url_run = "http://www.qichacha.com/company_getinfos?unique=" + unique[0] + "&companyname=" + urllib.quote(plat_name) + "&tab=run"
    try:  # 工商局处罚
        url_penalty_industry = url_run + "&box=penalty&source=1"
        content = r.get(url_penalty_industry).content
        if len(re.findall("暂无数据", content)):
            print "暂无数据,工商局处罚"
        else:
            reference_no = re.findall("<tr><td class=\"ma_twoword\">\d*</td> <td>(.+?)<", content)
            type = re.findall("<tr><td class=\"ma_twoword\">\d*</td> <td>.*?</td> <td>(.+?)<", content)
            bis_content = re.findall("<tr><td class=\"ma_twoword\">\d*</td> <td>.*?</td> <td>.*?</td> <td>(.+?)<", content.replace("\n", ""))
            decision_org = re.findall("<tr><td class=\"ma_twoword\">\d*</td> <td>.*?</td> <td>.*?</td> <td>.*?</td> <td>(.+?)<", content.replace("\n", ""))
            decision_date = re.findall("<tr><td class=\"ma_twoword\">\d*</td> <td>.*?</td> <td>.*?</td> <td>.*?</td> <td>.*?</td> <td style=\"width:100px;\">(.+?)<", content.replace("\n", ""))
            for nu, i in enumerate(reference_no):
                # print reference_no[nu], type[nu], bis_content[nu], decision_org[nu], decision_date[nu]
                try:
                    insert_penalty_industry(conn_ma, cur, credit_code, reference_no[nu], type[nu], content[nu], decision_org[nu], decision_date[nu])
                except:
                    continue
    except:
        traceback.print_exc()
        print "工商局处罚获取失败"
    try:  # 信用中国处罚
        url_penalty_china = url_run + "&box=penalty&source=2"
        content = r.get(url_penalty_china).content
        if len(re.findall("暂无数据", content)):
            print "暂无数据,信用中国处罚"
        else:
            name = re.findall("<tr><td class=\"ma_twoword\">.*?</td><td>(.*?)<", content)
            area = re.findall("<tr><td class=\"ma_twoword\">.*?</td><td>.*?</td><td widtd=\"10%\">.*?<", content)
            decision_date = re.findall("<tr><td class=\"ma_twoword\">.*?</td><td>.*?</td><td widtd=\"10%\">.*?</td><td widtd=\"15%\">(.+?)<", content)
            for nu, i in enumerate(name):
                # print name, area, decision_date
                try:
                    insert_penalty_china(conn, cur, credit_code, name[nu], area[nu], decision_date[nu])
                except:
                    continue
        return True
    except:
        traceback.print_exc()
        return False


def climb_abnormal(conn_ma, cur, credit_code, plat_name, url, r):
    unique = re.findall("_([A-Za-z0-9]{10,40})", url)
    try:
        url = "http://www.qichacha.com/company_getinfos?unique=" + unique[0] + "&companyname=" + urllib.quote(plat_name) + "&tab=run"
        content = r.get(url).content
        in_date = re.findall("列入日期：\s*<span class=\"black-6\">(.+?)<", content.replace("\n", ""))
        out_date = re.findall("移出日期：\s*<span class=\"black-6\">(.+?)<", content.replace("\n", ""))
        decision_org = re.findall("作出决定机关：\s*<span class=\"black-6\">(.+?)<", content.replace("\n", ""))
        out_org = re.findall("移除决定机关：\s*<span class=\"black-6\">(.+?)<", content.replace("\n", ""))
        in_cause = re.findall("列入经营异常名录原因：\s*<span class=\"black-6\">(.+?)<", content.replace("\n", ""))
        out_cause = re.findall("移出经营异常名录原因：\s*<span class=\"black-6\">(.+?)<", content.replace("\n", ""))
        if len(in_date):
            for nu, i in enumerate(in_date):
                # print in_date[nu], out_date[nu], decision_org[nu], out_org[nu], in_cause[nu], out_cause[nu]
                try:
                    insert_abnormal(conn, cur, credit_code, in_date[nu], out_date[nu], decision_org[nu], out_org[nu], in_cause[nu], out_cause[nu])
                except:
                    continue
        else:
            print "暂无数据,经营异常"
        return True
    except:
        traceback.print_exc()
        return False


def climb_invest(conn_ma, cur, content, r):
    try:
        company_name = re.findall("style=\"word-break: break-all;\">\s*<span\s*class=\"text-click-color\">(.+?)<", content)
        oper_name = re.findall("point new-c4\" target=\"_blank\"\s*title=\"(.+?)\"", content)
        capi = re.findall("</a>\s*?</span>\s*?</span>.*?</td>\s*?<td>\s*?<span class=\"\">(.*?)</span>", content)
        if len(company_name) > len(oper_name):
            for i in range(0, len(company_name) - len(oper_name)):
                oper_name.append("-")
        if len(company_name) > len(capi):
            for i in range(0, len(company_name) - len(capi)):
                capi.append("-")
        status = re.findall("[\d-]+\s*?</span>\s*?</td>\s*?<td>\s*?<span class=\"\">(.*?)<", content)
        if len(company_name) > len(status):
            for i in range(0, len(company_name) - len(status)):
                status.append("-")
        # percent = re.findall("</td> <td class=\"text-center\">\s*[\d%]+?\s*<", content)
        # capi_inve_per_date_status = re.findall("</a>\s*?</span>\s*?</span>\s*?</td>\s*?<td>\s*?<span class=\"\">(.*?)</span>\s*?</td>\s*?<td>\s*?<span class=\"\">(.*?)\s*?</span>\s*?</td>\s*?<td>" \
        #                             "\s*?<span class=\".*?\">(.*?)\s*?</span>\s*?</td>\s*?<td>\s*?<span class=\"\">([\d-]+)\s*?</span>\s*?</td>\s*?<td>\s*?<span class=\"\">(.*?)\s*?<", content)

        if len(company_name):
            re_dic = {"state": "ok", "message": "", "data": {"total": len(company_name), "result": []}}
            for nu, i in enumerate(company_name):
                try:
                    # print company_name[nu], status[nu], oper_name[nu], capi[nu].rstrip("人民币").rstrip("元") + "元人民币"
                    dic_invest = {"name": company_name[nu].replace("未公开", "-"),
                                  "regStatus": status[nu].strip().replace("未公开", "-"),
                                  "legalPersonName": oper_name[nu].strip().replace("未公开", "-"),
                                    "regCapital": capi[nu].strip().lstrip("(人民币)").rstrip("万元").rstrip("万").rstrip("万元人民币") + "万元人民币".replace("未公开", "-")
                                  # "regDate": capi_inve_per_date_status[nu][3].strip(),
                                  # "invest_amount": capi_inve_per_date_status[nu][1].strip(),
                                  # "invest_percent": capi_inve_per_date_status[nu][2].strip()
                    }
                    re_dic["data"]["result"].append(dic_invest)
                    # "name": "上海图辰企业信用征信有限公司", "base": "sh", "regStatus": "存续（在营、开业、在册）",
                    # "estiblishTime": 1461859200000, "type": 1, "legalPersonName": "朱畑宇",
                    # "pencertileScore": 5839
                except:
                    print capi, status
                    traceback.print_exc()
                    continue
            return re_dic
        else:
            print "暂无数据,无投资"
            return {"state":"warn","message":"无数据","data":"null"}
    except:
        print url
        traceback.print_exc()
        return False


def get_info(conn_ma, cur, conn_ma_be, cur_be, r, conn_ma_21, cur_21, name_url, index):
    global url
    for nu, n_u in enumerate(name_url.iterrows()):  # 从测试库里查询所有公司
        if nu < index:
            continue
        plat_name = n_u[1]['company_name'].strip().encode("utf-8")
        url = n_u[1]['source_url']
        r.proxies = get_proxies()
        # try:
        #     search_result = r.get("http://www.tianyancha.com/search?key=" + urllib.quote(plat_name) + "&checkFrom=searchBox").content.replace("\n", "")
        # except:
        #     print plat_name
        #     traceback.print_exc()
        #     return plat_name
            # continue
        # try:
        #     # url = re.findall(plat_name + ".*?" + plat_name + ".*?(http[s]*://www.tianyancha.com/company/\w+)", search_result)[0]
        #
        # except:
        #     print "URL有误或请求错误: " + plat_name
        #     traceback.print_exc()
        #     continue
        if url is None:
            continue
        credit_code = ""
        try:
            content = r.get(url).content.replace("\n", "")
            # print content
            credit_code, dic_IC_DATA= climb_info(conn_ma, cur, content, r)
            # credit_code = dic_IC_DATA = {}
            if len(re.findall("change-type=\"holder\"", content)):  # 股东多页
                url_holder = "http://www.tianyancha.com/pagination/holder.xhtml?ps=30&id=" + re.findall("\d+", url)[0] + "&pn="
                for i in range(2, int(re.findall("change-type=\"holder\">.*?<span>共</span>\s*(\d)\s*<span>页</span>", content)[0])+1):
                    content += r.get(url_holder + str(i)).content.replace("\n", "")
            list_SHAREHOLDER_DATA = climb_shareholder(conn_ma, cur, content, r)
            # list_SHAREHOLDER_DATA = {}
            if len(re.findall("change-type=\"staff\"", content)):  # 主要成员多页
                url_staff = "http://www.tianyancha.com/pagination/staff.xhtml?ps=30&id=" + re.findall("\d+", url)[0] + "&pn="
                for i in range(2, int(re.findall("change-type=\"staff\">.*?<span>共</span>\s*(\d)\s*<span>页</span>", content)[0])+1):
                    content += r.get(url_staff + str(i)).content.replace("\n", "")
            list_PRINCIPAL_DATA = climb_managers(conn_ma, cur, content, r)
            # list_PRINCIPAL_DATA = {}change-type="holder"
            if len(re.findall("change-type=\"invest\"", content)):  # 投资多页
                url_invest = "http://www.tianyancha.com/pagination/invest.xhtml?ps=30&id=" + re.findall("\d+", url)[0] + "&pn="
                for i in range(2, int(re.findall("change-type=\"invest\">.*?<span>共</span>\s*(\d)\s*<span>页</span>", content)[0])+1):
                    content += r.get(url_invest + str(i)).content.replace("\n", "")
            # if "北京恒昌利通投资管理有限公司" == plat_name or "宜信惠民投资管理（北京）有限公司" == plat_name:
            #     content = r.get(url).text.replace("\n", "")
            #     if len(re.findall("change-type=\"invest\"", content)):  # 投资多页
            #         url_invest = "http://www.tianyancha.com/pagination/invest.xhtml?ps=30&id=" + re.findall("\d+", url)[0] + "&pn="
            #         for i in range(2, int(re.findall(u"change-type=\"invest\">.*?<span>共</span>\s*(\d)\s*<span>页</span>", content)[0]) + 1):
            #                 content += r.get(url_invest + str(i)).text.replace("\n", "")
            dic_INVESTMENT_ABROAD = climb_invest(conn_ma, cur, content, r)
            # dic_INVESTMENT_ABROAD = {}
            print plat_name
            print url
            print json.dumps(dic_IC_DATA, encoding="UTF-8", ensure_ascii=False)
            print json.dumps(list_SHAREHOLDER_DATA, encoding="UTF-8", ensure_ascii=False)
            print json.dumps(list_PRINCIPAL_DATA, encoding="UTF-8", ensure_ascii=False)
            try:
                print json.dumps(dic_INVESTMENT_ABROAD, encoding="UTF-8", ensure_ascii=False)
            except:  # 投资页出现非utf-8编码格式
                content = r.get(url).text.replace("\n", "")
                if len(re.findall("change-type=\"invest\"", content)):  # 投资多页
                    url_invest = "http://www.tianyancha.com/pagination/invest.xhtml?ps=30&id=" + re.findall("\d+", url)[0] + "&pn="
                    for i in range(2, int(re.findall(u"change-type=\"invest\">.*?<span>共</span>\s*(\d)\s*<span>页</span>", content)[0]) + 1):
                        content += r.get(url_invest + str(i)).text.replace("\n", "")
                dic_INVESTMENT_ABROAD = climb_invest(conn_ma, cur, content, r)
                print json.dumps(dic_INVESTMENT_ABROAD, encoding="UTF-8", ensure_ascii=False)
            # insert_GONG_PLAT_COMPANY_IC_DATA(conn_ma, cur, plat_name,
            #                                  str(json.dumps(dic_IC_DATA, encoding="UTF-8", ensure_ascii=False)),
            #                                  str(json.dumps(list_SHAREHOLDER_DATA, encoding="UTF-8", ensure_ascii=False)),
            #                                  str(json.dumps(list_PRINCIPAL_DATA, encoding="UTF-8", ensure_ascii=False)),
            #                                  str(json.dumps(dic_INVESTMENT_ABROAD, encoding="UTF-8", ensure_ascii=False)),
            #                                     url)
            # insert_GONG_PLAT_COMPANY_IC_DATA21(conn_ma_be, cur_be, plat_name,
            #                                    str(json.dumps(dic_IC_DATA, encoding="UTF-8", ensure_ascii=False)),
            #                                    str(json.dumps(list_SHAREHOLDER_DATA, encoding="UTF-8",
            #                                                   ensure_ascii=False)),
            #                                    str(json.dumps(list_PRINCIPAL_DATA, encoding="UTF-8",
            #                                                   ensure_ascii=False)),
            #                                    str(json.dumps(dic_INVESTMENT_ABROAD, encoding="UTF-8",
            #                                                   ensure_ascii=False)),
            #                                    url)
            # insert_GONG_PLAT_COMPANY_IC_DATA21(conn_ma_21, cur_21, plat_name,
            #                                  str(json.dumps(dic_IC_DATA, encoding="UTF-8", ensure_ascii=False)),
            #                                  str(json.dumps(list_SHAREHOLDER_DATA, encoding="UTF-8", ensure_ascii=False)),
            #                                  str(json.dumps(list_PRINCIPAL_DATA, encoding="UTF-8", ensure_ascii=False)),
            #                                  str(json.dumps(dic_INVESTMENT_ABROAD, encoding="UTF-8", ensure_ascii=False)),
            #                                  url)
            # return ""  # 仅仅爬取一条时，立即返回
        except:
            print plat_name, url
            traceback.print_exc()
            return plat_name
        # time.sleep(300)  # 每五分钟采一条
        if (nu - index + 1) % 20 == 0:  # 每三十分钟采二十条
            time.sleep(1800)
    return ""
        # climb_judgementdoc(conn_ma, cur, credit_code, plat_name, url, r)
        # climb_court_announcement(conn_ma, cur, credit_code, plat_name, url, r)
        # climb_enforced(conn_ma, cur, credit_code, plat_name, url, r)
        # climb_begincourt_announcement(conn_ma, cur, credit_code, plat_name, url, r)
        # climb_penalty(conn_ma, cur, credit_code, plat_name, url, r)
        # climb_abnormal(conn_ma, cur, credit_code, plat_name, url, r)
        # insert_GONG_PLAT_COMPANY_IC_DATA(conn, cur, i, str(IC_DATA), str(SHAREHOLDER_DATA), PRINCIPAL_DATA,
        #                                  INVESTMENT_ABROAD, url)
        # break


def get_proxies():
    ip = json.loads(requests.get(
        "http://dps.kuaidaili.com/api/getdps/?orderid=958964320330191&num=50&ut=1&format=json&sep=1").content)
    proxies = {  # 每次请求从代理ip中随机产生一个地址
        "http": "http://8283891:ojonvhe8@" + ip["data"]["proxy_list"][random.randint(0, len(ip) - 1)]
    }
    return proxies


def get_cookie():
    return ""


def check_illegal(text):
    illegal = ["v", "-", "x", "y", "%", "\\", "/"]
    for k in illegal:
        if k in text:
            text = text.replace(k, "")
    return text


def get_company_url(conn):
    select_sql = "SELECT company_name,source_url FROM GONG_PLAT_COMPANY_SPIDER"
    app_management = pd.read_sql(select_sql, conn)
    # ls_company = app_management.get("company_name")
    name_url = app_management
    return name_url
    
# def update():
#     for i in ls_url:
#     update_sql = "UPDATE db_2.GONG_PLAT_COMPANY_IC_DATA SET account_url='" + "" + i +\
#                  "' where account_id='" + i + "'"
#     cur.execute(update_sql)
#     conn.commit()


# 测试函数
def login(r, username, pwd):
    m = hashlib.md5()
    m.update(pwd)
    print m.hexdigest()
    # print r.post('https://www.tianyancha.com/cd/login.json?mobile=' + username + '&cdpassword=' + m.hexdigest() + '&loginway=PL&autoLogin=true').content
    print r.post('https://www.tianyancha.com/cd/login.json', data=json.dumps({'mobile': username, 'cdpassword': str(m.hexdigest()), 'loginway': 'PL', 'autoLogin': True})).content
    return r


if __name__ == "__main__":
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    conn_ma = connect_database(db_nick='db_2')
    cur = conn_ma.cursor()
    conn_ma_21 = connect_database(db_nick='db_21')
    cur_21 = conn_ma_21.cursor()
    conn_ma_be = connect_database(db_nick='ma')
    cur_be = conn_ma_be.cursor()
    r = requests.session()
    r.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0, WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        # "Cookie": get_cookie(),
        'Host': 'www.tianyancha.com',
        # 'Referer': 'https://www.tianyancha.com/',
        # 'X-Requested-With': 'XMLHttpRequest',
        # 'Host': 'www.tianyancha.com',
        'Connection': 'keep-alive',
        'Content-Length': '106',
        'Origin': 'https://www.tianyancha.com',
        'Content-Type': 'application/json; charset=UTF-8',  # x-www-form-urlencoded
        'Accept': '*/*',
        # 'Referer': 'https://www.tianyancha.com/login',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    # r = login(r, '', '')
    # r.headers.pop( "Accept")
    # r.headers.pop('Origin')
    # r.headers.pop('Content-Length')
    # r.headers.pop('Referer')
    # r.headers.pop('X-Requested-With')
    r.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0, WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        # "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.8',
        # 'Connection': 'keep-alive',
        # 'Host': 'www.tianyancha.com',
        # 'Referer': 'https://www.tianyancha.com/',
        # 'Upgrade-Insecure-Requests': '1',
        "Cookie": get_cookie()
    }
    url = ""
    credit_code = ""
    # update_url(conn_ma_be, cur_be, r)
    # compare_url(conn_ma_be, cur_be, r)
    # urltoxianshang(conn_ma, cur, conn_ma_be, cur_be, conn_ma_21, cur_21)
    # delete_repeat(conn_ma, cur, conn_ma_be, cur_be, conn_ma_21, cur_21)
    # error_plat = get_info(conn_ma, cur, conn_ma_be, cur_be, r, conn_ma_21, cur_21, name_url).decode("utf-8")

    name_url = get_company_url(conn_ma)
    error_plat = u""  # 默认从第一条运行
    # error_plat = u""
    nu = 0
    while len(error_plat):
        time.sleep(1)
        index = list(name_url.get('company_name')).index(error_plat)
        error_plat = get_info(conn_ma, cur, conn_ma_be, cur_be, r, conn_ma_21, cur_21, name_url, index).decode("utf-8")
        nu += 1
        if nu % 9 == 0:  # 重复请求10次无果后停止运行
            break
    cur_be.close()
    conn_ma_be.close()
    cur_21.close()
    conn_ma_21.close()
    cur.close()
    conn_ma.close()
    print "climb finish"
