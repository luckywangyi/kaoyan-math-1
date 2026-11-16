# -*- coding: utf-8 -*-
"""按《考研数学基础30讲·高等数学分册》目录，将大 PDF 拆成按讲的小份 PDF。
识别依据：目录页 + 逐讲首页核验，书内页码 + 6 = PDF 页码（前置页 6 页）。
"""
import os
import csv
import pymupdf

SRC = r'C:\Users\25819\Documents\xwechat_files\wxid_81wkbp9r7hlw22_4f35\msg\file\2026-07\27张宇基础30讲（高数）.pdf'
OUT = r'C:\Users\25819\Desktop\高数\分章PDF'
OFFSET = 6  # 书内页码 -> PDF 页码

# (文件名, 书内起始页, 类别)
UNITS = [
    ('00_前置页_封面与前言目录', None, '前置'),
    ('第01讲_函数极限与连续', 1, '讲'),
    ('第02讲_数列极限', 76, '讲'),
    ('第03讲_一元函数微分学的概念', 99, '讲'),
    ('第04讲_一元函数微分学的计算', 119, '讲'),
    ('第05讲_一元函数微分学的应用(一)几何应用', 139, '讲'),
    ('第06讲_一元函数微分学的应用(二)中值定理与微分不等式', 164, '讲'),
    ('第07讲_一元函数微分学的应用(三)物理应用与经济应用', 186, '讲'),
    ('第08讲_一元函数积分学的概念与性质', 195, '讲'),
    ('第09讲_一元函数积分学的计算', 230, '讲'),
    ('第10讲_一元函数积分学的应用(一)几何应用', 263, '讲'),
    ('第11讲_一元函数积分学的应用(二)积分等式与积分不等式', 282, '讲'),
    ('第12讲_一元函数积分学的应用(三)物理应用与经济应用', 294, '讲'),
    ('第13讲_多元函数微分学', 304, '讲'),
    ('第14讲_二重积分', 338, '讲'),
    ('第15讲_微分方程', 377, '讲'),
    ('第16讲_无穷级数(仅数学一数学三)', 409, '讲'),
    ('第17讲_多元函数积分学的预备知识(仅数学一)', 464, '讲'),
    ('第18讲_多元函数积分学(仅数学一)', 488, '讲'),
    ('附录1_图像变换', 546, '附录'),
    ('附录2_常用平面图形', 549, '附录'),
    ('附录3_常用空间图形', 552, '附录'),
    ('附录4_重要公式', 555, '附录'),
    ('附录5_从指数函数到双曲函数', 558, '附录'),
    ('附录6_变形技巧', 563, '附录'),
]

# 完整讲名（用于书签与清单）
FULL_TITLES = {
    '第01讲_函数极限与连续': '第1讲 函数极限与连续',
    '第02讲_数列极限': '第2讲 数列极限',
    '第03讲_一元函数微分学的概念': '第3讲 一元函数微分学的概念',
    '第04讲_一元函数微分学的计算': '第4讲 一元函数微分学的计算',
    '第05讲_一元函数微分学的应用(一)几何应用': '第5讲 一元函数微分学的应用（一）——几何应用',
    '第06讲_一元函数微分学的应用(二)中值定理与微分不等式': '第6讲 一元函数微分学的应用（二）——中值定理、微分等式与微分不等式',
    '第07讲_一元函数微分学的应用(三)物理应用与经济应用': '第7讲 一元函数微分学的应用（三）——物理应用与经济应用',
    '第08讲_一元函数积分学的概念与性质': '第8讲 一元函数积分学的概念与性质',
    '第09讲_一元函数积分学的计算': '第9讲 一元函数积分学的计算',
    '第10讲_一元函数积分学的应用(一)几何应用': '第10讲 一元函数积分学的应用（一）——几何应用',
    '第11讲_一元函数积分学的应用(二)积分等式与积分不等式': '第11讲 一元函数积分学的应用（二）——积分等式与积分不等式',
    '第12讲_一元函数积分学的应用(三)物理应用与经济应用': '第12讲 一元函数积分学的应用（三）——物理应用与经济应用',
    '第13讲_多元函数微分学': '第13讲 多元函数微分学',
    '第14讲_二重积分': '第14讲 二重积分',
    '第15讲_微分方程': '第15讲 微分方程',
    '第16讲_无穷级数(仅数学一数学三)': '第16讲 无穷级数（仅数学一、数学三）',
    '第17讲_多元函数积分学的预备知识(仅数学一)': '第17讲 多元函数积分学的预备知识（仅数学一）',
    '第18讲_多元函数积分学(仅数学一)': '第18讲 多元函数积分学（仅数学一）',
    '附录1_图像变换': '附录1 图像变换',
    '附录2_常用平面图形': '附录2 常用平面图形',
    '附录3_常用空间图形': '附录3 常用空间图形',
    '附录4_重要公式': '附录4 重要公式',
    '附录5_从指数函数到双曲函数': '附录5 从指数函数到双曲函数',
    '附录6_变形技巧': '附录6 变形技巧',
    '00_前置页_封面与前言目录': '封面、前言与目录',
}


def main():
    os.makedirs(OUT, exist_ok=True)
    src = pymupdf.open(SRC)
    total = len(src)
    assert total == 586, f'页数异常: {total}'

    # 计算各单元 PDF 起止页（1-based，含端点）
    starts = []
    for name, book_page, _ in UNITS:
        starts.append(1 if book_page is None else book_page + OFFSET)
    bounds = []
    for i, s in enumerate(starts):
        e = (starts[i + 1] - 1) if i + 1 < len(starts) else total
        bounds.append((s, e))

    rows = []
    for (name, book_page, kind), (s, e) in zip(UNITS, bounds):
        out_path = os.path.join(OUT, name + '.pdf')
        new = pymupdf.open()
        new.insert_pdf(src, from_page=s - 1, to_page=e - 1, annots=False)
        new.set_metadata({
            'title': FULL_TITLES[name],
            'author': '张宇',
            'subject': '考研数学基础30讲·高等数学分册 · 分章拆分',
            'keywords': f'PDF页 {s}-{e}; 书内页 {book_page}',
        })
        new.set_toc([[1, FULL_TITLES[name], 1]])
        new.save(out_path, garbage=3, deflate=True)
        new.close()

        # 校验
        chk = pymupdf.open(out_path)
        ok = (len(chk) == e - s + 1) and (len(chk[0].get_images(full=True)) >= 1)
        size_mb = os.path.getsize(out_path) / 1024 / 1024
        chk.close()
        rows.append([kind, name + '.pdf', FULL_TITLES[name], book_page or '', s, e, e - s + 1,
                     round(size_mb, 1), 'OK' if ok else 'FAIL'])
        print(f'{"OK " if ok else "FAIL"} {name}.pdf  PDF页{s}-{e}  {e-s+1}页  {size_mb:.1f}MB', flush=True)

    src.close()

    with open(os.path.join(OUT, '_拆分清单.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['类别', '文件名', '完整标题', '书内起始页', 'PDF起始页', 'PDF结束页', '页数', '大小MB', '校验'])
        w.writerows(rows)

    print('\n合计页数:', sum(r[6] for r in rows), '合计大小MB:', round(sum(r[7] for r in rows), 1))
    print('失败项:', [r[1] for r in rows if r[8] == 'FAIL'])


if __name__ == '__main__':
    main()
