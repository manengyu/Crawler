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
import sys
reload(sys)
import chardet
sys.setdefaultencoding("utf-8")



def insert_GONG_PLAT_COMPANY_IC_DATA(conn, cur, COMPANY_NAME, IC_DATA, SHAREHOLDER_DATA, PRINCIPAL_DATA, INVESTMENT_ABROAD, SOURCE_URL):
    UPDATE_DATE = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    insert_sql = "INSERT INTO ma.GONG_PLAT_COMPANY_IC_DATA ( COMPANY_NAME, IC_DATA, SHAREHOLDER_DATA," \
                 " PRINCIPAL_DATA, INVESTMENT_ABROAD, SOURCE_URL, UPDATE_DATE) VALUES ('" + COMPANY_NAME + "','" +\
                 IC_DATA + "','" + SHAREHOLDER_DATA + "','" + PRINCIPAL_DATA + "','" + INVESTMENT_ABROAD + "','" +\
                 SOURCE_URL + "','" + UPDATE_DATE + "')"
    try:
        cur.execute(insert_sql)
        conn.commit()
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


def climb_info(conn_ma, cur, plat_name, url, r):
    unique = re.findall("_([A-Za-z0-9]{10,40})", url)
    try:
        url = "http://www.qichacha.com/company_getinfos?unique=" + unique[0] + "&companyname=" + urllib.quote(plat_name) + "&tab=base"
        # name = tax_no = no = org_no = oper_name = regist_capi = status, start_date = econ_kind = bus_people = term = belong_org = check_date = eng_name = belong_area = belong_industry = before_name = address = scope = "-"
        before_name = "-"
        content = r.get(url).content.replace("\n", "")
        credit_code = re.findall(">统一社会信用代码：</td> <td class=\"ma_left\">\s*(\w+)", content)[0].strip()
        print credit_code
        name = plat_name
        tax_no = re.findall(">纳税人识别号：</td> <td class=\"ma_left\">\s*([\d+|-])", content)[0].strip()
        no = re.findall(">注册号：</td> <td class=\"ma_left\">\s*([\d+|-])", content)[0].strip()
        org_no = re.findall(">组织机构代码：</td> <td class=\"ma_left\">\s*([\d-]+)", content)[0].strip()
        oper_name = re.findall("text-primary\">(.*?)</a>", content)[0].strip()
        regist_capi = re.findall("注册资本：</td> <td class=\"ma_left\">\s*([\d.-]+)", content)[0].strip()
        status = re.findall("经营状态：</td> <td class=\"ma_left\">\s*(.*?)\s*<", content)[0].strip()
        start_date = re.findall("成立日期：</td> <td class=\"ma_left\">\s*([\d-]+)", content)[0].strip()
        econ_kind = re.findall("公司类型：</td> <td class=\"ma_left\">\s*(.+?)\s*<", content)[0].strip()
        bus_people = re.findall("人员规模：</td> <td class=\"ma_left\">\s*([\d-]+)", content)[0].strip()
        term = re.findall("营业期限：</td> <td class=\"ma_left\">\s*(.+?)\s*<", content)[0].strip()
        belong_org = re.findall("登记机关：</td> <td class=\"ma_left\" style=\"max-width:301px;\">\s*(.+?)\s*<", content)[0].strip()
        check_date = re.findall("核准日期：</td> <td class=\"ma_left\">\s*(.+?)\s*<", content)[0].strip()
        eng_name = re.findall("英文名：</td> <td class=\"ma_left\" style=\"max-width:301px;\">\s*(.+?)\s*?", content)[0].strip()
        belong_area = re.findall("所属地区\s*</td> <td class=\"ma_left\">\s*(.+?)\s*<", content)[0].strip()
        belong_industry = re.findall("所属行业\s*</td> <td class=\"ma_left\">\s*(.+?)\s*<", content)[0].strip()
        address = re.findall("企业地址：</td> <td class=\"ma_left\" colspan=\"3\">\s*(.+?)\s*<", content)[0].strip()
        scope = re.findall("经营范围：</td> <td class=\"ma_left\" colspan=\"3\">\s*(.+?)\s*<", content)[0].strip()
        try:
            before_name = re.findall("企业地址：</td> <td class=\"ma_left\" colspan=\"3\">\s*(.+?)\s*<", content)[0].strip()
        except:
            traceback.print_exc()
            pass
        # print check_date, eng_name, belong_area, belong_industry, address, scope
        try:
            # print chardet.detect(json.dumps({"统一社会信誉代码：": credit_code,"注册号：": no,"组织机构代码：": org_no,
            #                      "经营状态：":status,"法定代表人：":oper_name,"注册资本：":regist_capi,"公司类型：":econ_kind,"成立日期：":start_date,"营业期限：":term,\
            #  "登记机关：":belong_org,"发照日期：":check_date,"公司规模：":bus_people,"所属行业：":belong_industry,"英文名：":eng_name,"曾用名：":before_name,"企业地址：":address,"经营范围：":scope}, ensure_ascii=False).encode('utf-8')), chardet.detect(before_name)
            # print credit_code, name, tax_no, no, org_no, oper_name, regist_capi, status,start_date, econ_kind, bus_people, term, belong_org, check_date, eng_name, belong_area, belong_industry, address, scope
            return credit_code, {"统一社会信誉代码：": credit_code,"注册号：": no,"组织机构代码：": org_no,
                                 "经营状态：":status,"法定代表人：":oper_name,"注册资本：":regist_capi,"公司类型：":econ_kind,"成立日期：":start_date,"营业期限：":term,\
             "登记机关：":belong_org,"发照日期：":check_date,"公司规模：":bus_people,"所属行业：":belong_industry,"英文名：":eng_name,"曾用名：":before_name,"企业地址：":address,"经营范围：":scope}
            # insert_business_info(conn_ma, cur, credit_code, name, tax_no, no, org_no, oper_name, regist_capi, status,
            #                      start_date, econ_kind, bus_people, term, belong_org, check_date, eng_name, belong_area,
            #                      belong_industry, address, scope)
        except:
            print url
            traceback.print_exc()
            return False
    except:
        print url
        traceback.print_exc()
        return False


def climb_shareholder(conn_ma, cur, credit_code, plat_name, url, r):
    r.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0, WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
                 "Cookie": get_cookie()}
    unique = re.findall("_([A-Za-z0-9]{10,40})", url)
    try:
        url = "http://www.qichacha.com/company_getinfos?unique=" + unique[0] + "&companyname=" + urllib.quote(plat_name) + "&tab=base"
        content = r.get(url).content.replace("\n", "")
        stock_name = re.findall("class=\"text-lg c_a\">(.+?)<", content)
        # stock_percent = re.findall("<span class=\"c_icon ca_plus\"></span> </a> </div> </td> <td class=\"text-center\">\s*(.+?)\s*<", content)
        # should_capi = re.findall("([\d.-]+)\s*<br/> </td> <td class=\"text-center\">", content)
        # should_date = re.findall("<br/> </td> <td class=\"text-center\">\s*(.*?)\s*<", content)
        percent_capi_date_type = re.findall("<td class=\"text-center\">\s*(.+?)\s*</td> <td class=\"text-center\">\s*(.+?)\s*</td> <td class=\"text-center\">\s*(.+?)\s*</td> <td class=\"text-center\">\s*(.+?)\s*</td> </tr>", content)
        # stock_type = re.findall("</td> <td class=\"text-center\">(.*?)</td> </tr> <tr>", content)
        re_dic = {}
        for nu, i in enumerate(stock_name):
            # print credit_code, stock_name[nu], percent_capi_date_type[nu][0], percent_capi_date_type[nu][1].replace("<br/>", "") + "万元人民币", percent_capi_date_type[nu][2].replace("<br/>", ""), percent_capi_date_type[nu][3]
            try:
                re_dic[stock_name[nu]] = percent_capi_date_type[nu][1].replace("<br/>", "").rstrip("万元人民币") + "万元人民币" + "|" + percent_capi_date_type[nu][2].replace("<br/>", "") + "|" + percent_capi_date_type[nu][0]
                # insert_business_shareholder(conn_ma, cur, credit_code, stock_name[nu], stock_percent[nu], should_capi[nu], should_date[nu], stock_type[nu])
            except:
                traceback.print_exc()
                continue
        return re_dic
    except:
        print url
        traceback.print_exc()
        return False


def climb_managers(conn_ma, cur, credit_code, plat_name, url, r):
    r = requests.session()
    r.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0, WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
                 "Cookie": get_cookie()}
    unique = re.findall("_([A-Za-z0-9]{10,40})", url)
    try:
        url = "http://www.qichacha.com/company_getinfos?unique=" + unique[0] + "&companyname=" + urllib.quote(plat_name) + "&tab=base"
        content = r.get(url).content
        name = re.findall("text-lg\" title=\".+?\">(.+?)</a></div> </td> <td class=\"text-center\">", content)
        post = re.findall("</td> <td class=\"text-center\">\s+(.*?)\s+</td> </tr>", content)
        # for nu, i in enumerate(name):
        #     print i, post[nu]
        re_list = []
        for nu, i in enumerate(name):
            try:
                print credit_code, name[nu], post[nu]
                re_list.append({post[nu]: name[nu]})
                # insert_business_managers(conn_ma, cur, credit_code, name[nu], post[nu])
            except:
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
                    print i, pub_date[nu], case_no[nu], court[nu]
                    # try:
                    #     insert_business_judgementdoc(conn_ma, cur, credit_code, case_name[nu], pub_date[nu], case_no[nu], case_identity[nu], court[nu])
                    # except:
                    #     continue
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
                    # try:
                    #     insert_business_court_announcement(conn_ma, cur, credit_code, publish_date[nu], type[nu], party[nu], bis_content[nu])
                    # except:
                    #     continue
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
                    print name[nu], register_date[nu], court[nu], subject[nu]
                    # try:
                    #     insert_business_enforced(conn_ma, cur, credit_code, name[nu], register_date[nu], court[nu], subject[nu])
                    # except:
                    #     continuev
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
                print begin_date, cause, accuser, accused, case_no, area, schedule_date, department, judge, court, court_ting
                # try:
                #     insert_begincourt_announcement(conn, cur, credit_code, begin_date, cause, accuser, accused, case_no, area, schedule_date, department, judge, court, court_ting)
                # except:
                #     continue
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
                print reference_no[nu], type[nu], bis_content[nu], decision_org[nu], decision_date[nu]
                # try:
                #     insert_penalty_industry(conn_ma, cur, credit_code, reference_no[nu], type[nu], content[nu], decision_org[nu], decision_date[nu])
                # except:
                #     continue
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
                print in_date[nu], out_date[nu], decision_org[nu], out_org[nu], in_cause[nu], out_cause[nu]
                # try:
                #     insert_abnormal(conn, cur, credit_code, in_date[nu], out_date[nu], decision_org[nu], out_org[nu], in_cause[nu], out_cause[nu])
                # except:
                #     continue
        else:
            print "暂无数据,经营异常"
        return True
    except:
        traceback.print_exc()
        return False


def climb_invest(conn_ma, cur, credit_code, plat_name, url, r):
    unique = re.findall("_([A-Za-z0-9]{10,40})", url)
    try:
        url = "http://www.qichacha.com/company_getinfos?unique=" + unique[0] + "&companyname=" + urllib.quote(plat_name) + "&tab=touzi"
        content = r.get(url).content
        company_name = re.findall("text-lg c_a\">(.+?)<", content.replace("\n", ""))
        oper_name = re.findall("class=\" c_a\">(.+?)<", content.replace("\n", ""))
        capi = re.findall("</a> </td> <td class=\"text-center\">\s*(.+?)\s*<", content.replace("\n", ""))
        percent = re.findall("</td> <td class=\"text-center\">\s*[\d%]+?\s*<", content.replace("\n", ""))
        status = re.findall("text-success m-l-xs\">(.+?)<", content.replace("\n", ""))
        if len(company_name):
            re_dic = {"state": "ok", "message": "", "data": {"total": len(company_name), "result": []}}
            for nu, i in enumerate(company_name):
                # print in_date[nu], out_date[nu], decision_org[nu], out_org[nu], in_cause[nu], out_cause[nu]
                try:
                    # print company_name[nu], status[nu], oper_name[nu], capi[nu].rstrip("人民币").rstrip("元") + "元人民币"
                    dic_invest = {"name": company_name[nu], "regStatus": status[nu], "legalPersonName": oper_name[nu],
                         "regCapital": capi[nu].rstrip("人民币").rstrip("元") + "元人民币"}
                    re_dic["data"]["result"].append(dic_invest)
                except:
                    continue
            return re_dic
        else:
            print "暂无数据,无投资"
            return {"state":"warn","message":"无数据","data":"null"}
    except:
        print url
        traceback.print_exc()
        return False


def get_info(conn_ma, cur, r):
    for plat_name in get_company():
        # plat_name = "中微（北京）信用管理有限公司"
        r.proxies = get_proxies()
        try:
            search_result = r.get("http://www.qichacha.com/search?key=" + urllib.quote(plat_name)).content
            url = "http://www.qichacha.com/" + re.findall("firm_\w+\.shtml",search_result)[0]
        except:
            print "http://www.qichacha.com/search?key=" + urllib.quote(plat_name)
            traceback.print_exc()
            return
        # print url
        credit_code = ""
        try:
            credit_code, dic_IC_DATA= climb_info(conn_ma, cur, plat_name, url, r)
            list_SHAREHOLDER_DATA = climb_shareholder(conn_ma, cur, credit_code, plat_name, url, r)
            list_PRINCIPAL_DATA = climb_managers(conn_ma, cur, credit_code, plat_name, url, r)
            dic_INVESTMENT_ABROAD = climb_invest(conn_ma, cur, credit_code, plat_name, url, r)
            print plat_name, str(dic_IC_DATA), str(list_SHAREHOLDER_DATA), str(list_PRINCIPAL_DATA),str(dic_INVESTMENT_ABROAD), url
            # insert_GONG_PLAT_COMPANY_IC_DATA(conn_ma, cur, plat_name,
            #                                  str(json.dumps(dic_IC_DATA, encoding="UTF-8", ensure_ascii=False)),
            #                                  str(json.dumps(list_SHAREHOLDER_DATA, encoding="UTF-8", ensure_ascii=False)),
            #                                  str(json.dumps(list_PRINCIPAL_DATA, encoding="UTF-8", ensure_ascii=False)),
            #                                  str(json.dumps(dic_INVESTMENT_ABROAD, encoding="UTF-8", ensure_ascii=False)),
            # url)
        except:
            traceback.print_exc()
            continue


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
    [text.replace(k, "") for k in illegal if k in text]
    return text.replace("-", "").replace("%", "").replace("v", "").replace("x", "").replace("y", "").replace("\"", "").replace("/", "").replace("\\", "")


def get_company():
    return []


# 测试函数
if __name__ == "__main__":
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    conn_ma = connect_database(db_nick='ma')
    cur = conn_ma.cursor()
    r = requests.session()
    r.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0, WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        "Cookie": get_cookie()}
    credit_code = ""
    get_info(conn_ma, cur, r)
    cur.close()
    conn_ma.close()
    print "climb finish"
