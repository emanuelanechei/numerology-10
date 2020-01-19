import argparse


def shrink(value, is_skip_special=True):
    specials = [13, 14, 16, 19, 11, 22]

    flag = None
    while True:
        value = add_digits(value)

        if value in specials and is_skip_special:
            flag = value
            break
        if value <= 9:
            break
    return value


def add_digits(value):
    v = []
    while True:
        v.append(value % 10)
        value = value // 10
        if value <= 0:
            break
    return sum(v)


def alpha2value(string):
    values = []
    epoch = ord("a") - 1
    for s in string.lower():
        values.append(shrink(ord(s) - epoch))
    return values


def filter_vowel(string):
    vowels = "aiueo"
    return "".join([s for s in string.lower() if s in vowels])


def filter_consonant(string):
    vowels = "aiueo"
    return "".join([s for s in string.lower() if s not in vowels])


class Numerology:
    def __init__(self, year, month, day, name):
        self.year = year
        self.month = month
        self.day = day
        self.name = name.replace(" ", "").lower()

        self.is_calculated = False

    def __str__(self):
        if self.is_calculated:
            out = "あなたの入力\n"
            out += "    誕生年 %d\n" % self.year
            out += "    誕生月 %d\n" % self.month
            out += "    誕生日 %d\n" % self.day
            out += "    名前　 %s\n" % self.name
            out += "\n"
            out += "誕生数\t %s\n" % self.tanjo
            out += "運命数\t %s\n" % self.unmei
            out += "実現数\t %s\n" % self.jitsugen
            out += "ハート数 %s\n" % self.heart
            out += "人格数\t %s\n" % self.jinkaku
            out += "習慣数\t %s\n" % self.shukan

            out += "特性数/欠落数\n"
            for number in self.tokusei:
                occurs, label = self.tokusei[number]
                out += ("    %d [%d回] %s\n" % (number, occurs, label))

            out += "気質のバランス\n"
            for key in self.balance:
                out += "    %s\t%d\n" % (key, self.balance[key])

            out += "時間区分\n"
            for i, term in enumerate(self.terms):
                out += "    第%d期 %s〜%s\t%d\t%d\n" % (
                    i+1, term["区分"][0], term["区分"][1], term["頂点数"], term["試練数"]
                )
            out += "個人年リスト\n"
            for year, pyear in self.pyears:
                out += "    %d --> 個人年%d\n" % (year, pyear)
        else:
            out = "VALUE NOT AVAILABLE"
        return out

    def calc_chart(self):
        self.tanjo = self.get_tanjo()
        self.unmei = self.get_unmei()
        self.jitsugen = self.get_jitsugen()
        self.heart = self.get_heart()
        self.jinkaku = self.get_jinkaku()
        self.shukan = self.get_shukan()
        self.tokusei = self.get_tokusei()
        self.balance = self.get_balance()
        self.terms = self.get_terms()
        self.pyears = self.get_personal_years()

        self.is_calculated = True

    def get_tanjo(self):
        """誕生数の計算"""
        return shrink(shrink(self.year) + shrink(self.month) + shrink(self.day))

    def get_unmei(self):
        """運命数の計算"""
        return shrink(sum(alpha2value(self.name)))

    def get_jitsugen(self):
        """実現数の計算"""
        return shrink(self.tanjo + self.unmei)

    def get_heart(self):
        """ハート数の計算"""
        return shrink(sum(alpha2value(filter_vowel(self.name))))

    def get_jinkaku(self):
        """人格数の計算"""
        return shrink(sum(alpha2value(filter_consonant(self.name))))

    def get_shukan(self):
        """習慣数の計算"""
        return shrink(len(self.name))

    def get_tokusei(self):
        """特性数/欠落数の計算"""
        values = alpha2value(self.name)
        ret = {}
        for i in range(1, 10):
            occurrs = len([tmp for tmp in values if tmp == i])
            if occurrs == 0:
                label = "欠落数"
            elif occurrs >= 3:
                label = "特性数"
            else:
                label = ""
            ret[i] = (occurrs, label)
        return ret

    def get_balance(self):
        values = alpha2value(self.name)
        conds = {
            "身体数": [4, 5],
            "知性数": [1, 8],
            "感情数": [2, 3, 6],
            "直感数": [7, 9]
        }
        ret = {}
        for key in conds:
            ret[key] = len([v for v in values if v in conds[key]])
        return ret

    def get_terms(self):
        """年齢区分と、区分ごとの頂点数と試練数を計算"""
        # 事前の計算
        syear = shrink(self.year)
        smonth = shrink(self.month)
        sday = shrink(self.day)

        # 年齢区分
        terms = []
        terms.append(("誕生", 36-self.tanjo))
        terms.append((terms[-1][1]+1, terms[-1][1]+9))
        terms.append((terms[-1][1]+1, terms[-1][1]+9))
        terms.append((terms[-1][1]+1, "終生"))

        # 頂点数
        choten = [
            shrink(smonth + sday, False),
            shrink(sday + syear, False),
            shrink((smonth + sday) + (sday + syear), False),
            shrink(smonth + syear, False),
        ]

        # 試練数
        shiren = [
            shrink(abs(smonth - sday), False),
            shrink(abs(sday - syear), False),
            shrink(abs(abs(smonth - sday) - abs(sday - syear)), False),
            shrink(abs(smonth - syear), False),
        ]

        # 組み合わせる
        merged = ({
            "区分": terms[i], "頂点数": choten[i], "試練数": shiren[i]
        } for i in range(4))
        return merged

    def get_personal_years(self, begin=2019, end=2030):
        pyears = []
        for y in range(begin, end):
            pyear = shrink(shrink(y) + shrink(day) + shrink(month))
            pyears.append((y, pyear))
        return pyears


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--year", type=int, help="year")
    parser.add_argument("-m", "--month", type=int, help="month")
    parser.add_argument("-d", "--day", type=int, help="day")
    parser.add_argument("-n", "--name", help="name")
    args = parser.parse_args()

    # 取得と表示
    year = args.year
    month = args.month
    day = args.day
    name = args.name.replace(" ", "").lower()

    obj = Numerology(year, month, day, name)
    obj.calc_chart()
    print(obj)

