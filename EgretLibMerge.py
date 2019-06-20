import argparse
import json
import sqlite3
import zlib
from pathlib import Path
from sys import exit

# 数据库打开标识
db_open = False


def create_db():
    # 创建数据库表
    global db_open
    if db_open:
        return
    global conn
    conn = sqlite3.connect('map.db')
    global cr
    cr = conn.cursor()
    # 建表需要判断数据表是否存在 if not exists
    cr.execute('create table if not exists `md5` (id text primary key, md5_value text)')
    db_open = True


def close_db():
    # commit并关闭数据库，保存之前已经正确处理的数据
    global db_open
    if not db_open:
        return
    conn.commit()
    cr.close()
    conn.close()
    db_open = False


def cal_crc(p_file):
    """
    计算文件的crc
    :param p_file:
    :return:
    """
    prev = 0
    for each_line in open(p_file, 'rb'):
        prev = zlib.crc32(each_line, prev)
    return '%X' % (prev & 0xffffffff)


def run(p_release_dir):
    path_release = Path(p_release_dir)
    list_file = sorted(path_release.rglob('manifest.json'))

    if len(list_file) < 1:
        print('目录中没有manifest.json文件，程序退出')
        exit()

    for v in list_file:
        str_result = ''
        if not v.parent.parent.samefile(path_release):
            continue
        str_result = '//' + str(v.relative_to(path_release)) + '\n'
        ver_str = str(v.parent.relative_to(path_release))
        with open(str(v), 'r', encoding='utf-8') as f:
            json_manifest = json.loads(f.read())
            list_initial = json_manifest['initial']
            for url_js in list_initial:
                path_js = path_release / url_js
                if not path_js.exists():
                    print('不存在js文件 >>\n%s\n>> 程序退出，处理下一个' % url_js)
                    continue
                str_js = path_js.read_text(encoding='utf-8')
                str_result += ('//' + url_js + '\n')
                str_result += str_js + '\n'
            if str_result:
                path_lib_js = path_release / 'common' / 'egretLib_temp.js'
                path_lib_js.write_text(str_result, encoding='utf-8')
                crc_value = cal_crc(path_lib_js)
                path_new_file = path_release / 'common' / ('egretLib_{0}_{1}.min.js'.format(crc_value, ver_str))
                if not path_new_file.exists():
                    path_lib_js.rename(path_new_file)  # 重命名临时文件
                else:
                    path_lib_js.unlink()  # 删除临时文件
                print('合并成功 ' + path_new_file.name)
            pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='帮助信息')
    parser.add_argument('--source', type=str, default='', help='发布目录')
    args = parser.parse_args()

    source = args.source
    if not source:
        print('请指定参数"--source"，程序退出')
        exit()
    path_source = Path(source)
    print('source=' + str(path_source.absolute()))
    run(source)
