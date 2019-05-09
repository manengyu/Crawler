"""
validateIdCard: function(t) {
                    var e = {
                        11: "北京",
                        12: "天津",
                        13: "河北",
                        14: "山西",
                        15: "内蒙古",
                        21: "辽宁",
                        22: "吉林",
                        23: "黑龙江",
                        31: "上海",
                        32: "江苏",
                        33: "浙江",
                        34: "安徽",
                        35: "福建",
                        36: "江西",
                        37: "山东",
                        41: "河南",
                        42: "湖北",
                        43: "湖南",
                        44: "广东",
                        45: "广西",
                        46: "海南",
                        50: "重庆",
                        51: "四川",
                        52: "贵州",
                        53: "云南",
                        54: "西藏",
                        61: "陕西",
                        62: "甘肃",
                        63: "青海",
                        64: "宁夏",
                        65: "新疆",
                        71: "台湾",
                        81: "香港",
                        82: "澳门",
                        91: "国外"
                    };
                    return "" !== t && (!1 !== this.isCardNo(t) && (!1 !== this.checkProvince(t, e) && (!1 !== this.checkBirthday(t) && !1 !== this.checkParity(t))))
                },
                isCardNo: function(t) {
                    var e = /(^\d{15}$)|(^\d{17}(\d|X|x)$)/;
                    return !1 !== e.test(t)
                },
                checkProvince: function(t, e) {
                    var r = t.substr(0, 2);
                    return void 0 != e[r]
                },
                checkBirthday: function(t) {
                    var e = t.length;
                    if ("15" == e) {
                        var r = /^(\d{6})(\d{2})(\d{2})(\d{2})(\d{3})$/
                          , n = t.match(r)
                          , a = n[2]
                          , i = n[3]
                          , s = n[4]
                          , o = new Date("19" + a + "/" + i + "/" + s);
                        return this.verifyBirthday("19" + a, i, s, o)
                    }
                    if ("18" == e) {
                        var c = /^(\d{6})(\d{4})(\d{2})(\d{2})(\d{3})([0-9]|X|x)$/;
                        n = t.match(c),
                        a = n[2],
                        i = n[3],
                        s = n[4],
                        o = new Date(a + "/" + i + "/" + s);
                        return this.verifyBirthday(a, i, s, o)
                    }
                    return !1
                },
                verifyBirthday: function(t, e, r, n) {
                    var a = new Date
                      , i = a.getFullYear();
                    if (n.getFullYear() == t && n.getMonth() + 1 == e && n.getDate() == r) {
                        var s = i - t;
                        return s >= 0 && s <= 100
                    }
                    return !1
                },
                checkParity: function(t) {
                    t = this.changeFivteenToEighteen(t);
                    var e = t.length;
                    if ("18" == e) {
                        var r, n, a = new Array(7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2), i = new Array("1","0","X","9","8","7","6","5","4","3","2"), s = 0;
                        for (r = 0; r < 17; r++)
                            s += t.substr(r, 1) * a[r];
                        return n = i[s % 11],
                        n == t.substr(17, 1).toLocaleUpperCase()
                    }
                    return !1
                },
                changeFivteenToEighteen: function(t) {
                    if ("15" == t.length) {
                        var e, r = new Array(7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2), n = new Array("1","0","X","9","8","7","6","5","4","3","2"), a = 0;
                        for (t = t.substr(0, 6) + "19" + t.substr(6, t.length - 6),
                        e = 0; e < 17; e++)
                            a += t.substr(e, 1) * r[e];
                        return t += n[a % 11],
                        t
                    }
                    return t
                }
"""
