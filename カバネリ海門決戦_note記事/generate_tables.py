#!/usr/bin/env python3
"""
カバネリ海門決戦 note記事用テーブル画像生成
02_ボーダーG数テーブルのデザインに全て統一
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib_fontja
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'images')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 統一カラー
BG = '#1a1a2e'
CARD = '#16213e'
HEADER = '#e94560'
ROW_A = '#1a3a5c'
ROW_B = '#162d4a'
DARK_ROW = '#2a1a3a'
TEXT = '#ffffff'
ACCENT = '#f1c40f'
EDGE = '#333333'


def make_table(filename, title, subtitle, col_labels, row_data, row_colors=None, accent_cols=None, highlight_last_row=False):
    """統一フォーマットでテーブル画像を生成"""
    n_rows = len(row_data)
    n_cols = len(col_labels)
    fig_h = 2.0 + n_rows * 0.85
    fig, ax = plt.subplots(figsize=(13, fig_h))
    ax.axis('off')
    fig.patch.set_facecolor(BG)

    table = ax.table(cellText=row_data, colLabels=col_labels,
                     cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(13)
    table.scale(1, 2.2)

    # ヘッダー
    for j in range(n_cols):
        c = table[0, j]
        c.set_facecolor(HEADER)
        c.set_text_props(color=TEXT, fontweight='bold', fontsize=12)
        c.set_edgecolor(EDGE)

    # データ行
    if row_colors is None:
        row_colors = [ROW_A if i % 2 == 0 else ROW_B for i in range(n_rows)]

    if accent_cols is None:
        accent_cols = list(range(1, n_cols))  # デフォルト：1列目以降を黄色

    for i in range(n_rows):
        bg = row_colors[i] if i < len(row_colors) else ROW_A
        if highlight_last_row and i == n_rows - 1:
            bg = DARK_ROW
        for j in range(n_cols):
            c = table[i + 1, j]
            c.set_facecolor(bg)
            c.set_edgecolor(EDGE)
            if j == 0:
                c.set_text_props(color=TEXT, fontweight='bold', fontsize=12)
            elif j in accent_cols:
                c.set_text_props(color=ACCENT, fontweight='bold', fontsize=13)
            else:
                c.set_text_props(color=TEXT, fontsize=12)

    title_text = title
    if subtitle:
        title_text += f'\n{subtitle}'
    ax.set_title(title_text, fontsize=16, fontweight='bold', pad=25, color=TEXT)

    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, dpi=200, bbox_inches='tight', facecolor=BG)
    plt.close()
    print(f'✅ {filename}')


# ━━━━━━━━━━ テーブル一覧 ━━━━━━━━━━

def t01_border():
    """ボーダーG数一覧（メインテーブル）"""
    make_table(
        '01_ボーダーG数テーブル.png',
        '【等価交換】ボーダーG数一覧（設定1）',
        '※3000万G実戦値準拠',
        ['状態', '104%\nボーダー', '106%\nボーダー', '108%\nボーダー', '時給2000円', '時給3000円'],
        [
            ['リセット後',         '20G〜',  '50G〜',  '80G〜',  '90G〜',  '140G〜'],
            ['ST駆け抜け後',       '50G〜',  '80G〜',  '100G〜', '120G〜', '170G〜'],
            ['上位ST後',           '30G〜',  '60G〜',  '100G〜', '100G〜', '150G〜'],
            ['非短縮（通常天井）', '500G〜', '530G〜', '580G〜', '600G〜', '650G〜'],
        ],
        highlight_last_row=True
    )


def t02_border_56():
    """56枚交換ボーダー"""
    make_table(
        '02_ボーダーG数_56枚.png',
        '【5.6枚交換】ボーダーG数一覧（設定1）',
        '※500枚制限考慮',
        ['状態', '104%\nボーダー', '106%\nボーダー', '時給2000円', '時給3000円'],
        [
            ['リセット後',         '90G〜',  '140G〜', '160G〜', '210G〜'],
            ['ST駆け抜け後',       '120G〜', '170G〜', '190G〜', '240G〜'],
            ['上位ST後',           '100G〜', '150G〜', '170G〜', '220G〜'],
            ['非短縮（通常天井）', '570G〜', '610G〜', '660G〜', '720G〜'],
        ],
        highlight_last_row=True
    )


def t03_setting():
    """設定別スペック"""
    make_table(
        '03_設定別スペック.png',
        '【カバネリ海門決戦】設定別スペック一覧',
        '※ST突入率・景之ST率は実戦値ベース推定',
        ['設定', '機械割', 'AT合算', 'ST突入率\n（推定）', '景之ST率\n（推定）'],
        [
            ['設定1', '97.8%',  '1/237', '約25%', '約15%'],
            ['設定2', '99.2%',  '1/220', '約28%', '約18%'],
            ['設定4', '104.5%', '1/195', '約35%', '約22%'],
            ['設定5', '107.2%', '1/175', '約38%', '約26%'],
            ['設定6', '110.0%', '1/151', '約45%', '約30%'],
        ],
        row_colors=[ROW_A, ROW_B, '#1a3a2a', '#2a3a1a', '#3a2a1a'],
    )


def t04_checklist():
    """30秒チェックリスト"""
    make_table(
        '04_30秒チェックリスト.png',
        '【プロの30秒チェックリスト】',
        '台に座る前に確認する6項目',
        ['項目', '確認方法', '高期待値の条件', '信頼度'],
        [
            ['①AT信号',    'データカウンター',   'AT(ST)が1回以上',     '★★★★★'],
            ['②獲得枚数',  'データカウンター',   '前回100枚未満',       '★★★★'],
            ['③サブ液晶',  '台のサブ液晶目視',   '桜→エピボ濃厚\n海門城→短縮確定', '★★★★★'],
            ['④グラフ',    'スランプグラフ',     '右肩下がり',           '★★★'],
            ['⑤前回AT回数','履歴のAT回数',       '2回以上(景之ST可能性)', '★★★★'],
            ['⑥現在G数',   'データカウンター',   '短縮:0G〜/通常:500G〜','★★★'],
        ],
        accent_cols=[3],  # 信頼度列だけ黄色
    )


def t05_ev_tanshuku():
    """天井短縮時のG数別期待値テーブル"""
    make_table(
        '05_期待値_短縮天井.png',
        '【短縮天井596G】G数別 期待値テーブル',
        '※等価交換・設定1ベース',
        ['G数', 'ST駆け抜け後', 'リセット後', '上位ST後', '判定'],
        [
            ['0G',   '+200円',   '+500円',   '+300円',   '○ 打てる'],
            ['50G',  '+500円',   '+800円',   '+600円',   '○ 打てる'],
            ['100G', '+1,000円', '+1,300円', '+1,100円', '○ 打てる'],
            ['200G', '+2,200円', '+2,500円', '+2,300円', '◎ 狙い目'],
            ['300G', '+3,800円', '+4,200円', '+4,000円', '◎ 狙い目'],
            ['400G', '+6,000円', '+6,500円', '+6,200円', '◎ 激アツ'],
            ['500G', '+9,500円', '+10,000円','+9,800円', '◎ 激アツ'],
            ['550G', '+11,500円','+12,000円','+11,800円','◎ 激アツ'],
        ],
        accent_cols=[1, 2, 3],
    )


def t06_ev_normal():
    """通常天井時のG数別期待値テーブル"""
    make_table(
        '06_期待値_通常天井.png',
        '【通常天井996G】G数別 期待値テーブル',
        '※等価交換・設定1ベース',
        ['G数', '期待値', '時給換算', '判定'],
        [
            ['300G',  '-800円',     '—',          '× スルー'],
            ['400G',  '+200円',     '+160円/h',   '△ ボーダー'],
            ['500G',  '+1,800円',   '+1,700円/h', '○ 狙い目'],
            ['600G',  '+4,500円',   '+5,400円/h', '◎ 激アツ'],
            ['700G',  '+8,000円',   '+11,500円/h','◎ 激アツ'],
            ['800G',  '+13,000円',  '+22,000円/h','◎ 激アツ'],
            ['900G',  '+20,000円',  '+38,000円/h','◎ 激アツ'],
        ],
        accent_cols=[1, 2],
    )


def t07_sub_lcd():
    """サブ液晶背景の活用ガイド"""
    make_table(
        '07_サブ液晶ガイド.png',
        '【サブ液晶】背景別 期待値変動',
        '※一般人が最も見落とすポイント',
        ['背景', '意味', '期待値変動', '出現頻度'],
        [
            ['通常（夕焼け）', '通常状態',                  '±0',           '—'],
            ['桜',             '4周期以内エピボ濃厚',       '+5,000円以上',  '週1〜2回'],
            ['海門城',         '短縮確定＋海門回想確定',     '+8,000円以上',  '月2〜3回'],
            ['黒煙（強）',     '黒煙ポイント高蓄積示唆',   '+3,000〜5,000円','1日1回'],
        ],
        accent_cols=[2],
    )


def t08_mistakes():
    """一般人の致命的ミス"""
    make_table(
        '08_致命的ミス一覧.png',
        '【一般人が犯す致命的ミス5選】',
        '合計: 月に約58,000円の損失',
        ['ミス', '内容', '月間損失額'],
        [
            ['①天井短縮を判別しない', 'G数だけで拾う',                  '-20,000円'],
            ['②サブ液晶を見ない',     '桜/海門城に気づかず離席',        '-15,000円'],
            ['③景之ST後に即やめ',     '短縮＋ループ抽選を活用しない',   '-10,000円'],
            ['④駿城BN後にやめる',     'G数・周期引き継ぎを知らない',    '-8,000円'],
            ['⑤黒煙蓄積をスルー',     'ST駆け抜け2〜3回台を見逃す',    '-5,000円'],
        ],
        accent_cols=[2],
        row_colors=[DARK_ROW] * 5,
    )


if __name__ == '__main__':
    print('=' * 50)
    print('テーブル画像生成（統一デザイン）')
    print('=' * 50)

    # 上書き保存（削除はスキップ）

    t01_border()
    t02_border_56()
    t03_setting()
    t04_checklist()
    t05_ev_tanshuku()
    t06_ev_normal()
    t07_sub_lcd()
    t08_mistakes()

    print(f'\n全{len(os.listdir(OUTPUT_DIR))}枚生成完了')
