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


def count_words(string):
    values = alpha2value(string)
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


def count_balance(string):
    values = alpha2value(string)
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
    print("""
あなたの入力
    誕生年   %d
    誕生月   %d
    誕生日   %d
    名前    %s
    """ % (year, month, day, name))


    # 誕生数
    tan = shrink(shrink(year) + shrink(month) + shrink(day))
    print("誕生数\t", tan)

    # 運命数
    unn = shrink(sum(alpha2value(name)))
    print("運命数\t", unn)

    # 実現数
    print("実現数\t", shrink(tan + unn))

    # ハート数
    vow = filter_vowel(name)
    print("ハート数", shrink(sum(alpha2value(filter_vowel(name)))))

    # 人格数
    print("人格数\t", shrink(sum(alpha2value(filter_consonant(name)))))

    # 習慣数
    print("習慣数\t", shrink(len(name)))

    # 特性数/欠落数
    print("特性数/欠落数")
    count = count_words(name)
    for number in count:
        occurs, label = count[number]
        print("    %d [%d回] %s" % (number, occurs, label))

    # 気質のバランス
    count = count_balance(name)
    for key in count:
        print(key, count[key])

    # 年齢区分
    terms = []
    terms.append(("誕生", 36-tan))
    terms.append((terms[-1][1]+1, terms[-1][1]+9))
    terms.append((terms[-1][1]+1, terms[-1][1]+9))
    terms.append((terms[-1][1]+1, "終生"))

    # 頂点数
    syear = shrink(year)
    smonth = shrink(month)
    sday = shrink(day)

    cho = [
        shrink(smonth + sday, False),
        shrink(sday + syear, False),
        shrink((smonth + sday) + (sday + syear), False),
        shrink(smonth + syear, False),
    ]

    # 試練数
    shi = [
        shrink(abs(smonth - sday), False),
        shrink(abs(sday - syear), False),
        shrink(abs(abs(smonth - sday) - abs(sday - syear)), False),
        shrink(abs(smonth - syear), False),
    ]

    print("\n年齢区分")
    for i in range(4):
        print("    第%d期 %s〜%s\t%d\t%d" % (
            i+1, terms[i][0], terms[i][1],
            cho[i], shi[i]
        ))

    # 個人年
    print("個人年リスト")
    for y in range(2020, 2030):
        pyear = shrink(shrink(y) + shrink(day) + shrink(month))
        print("    %d --> 個人年%d" % (y, pyear))