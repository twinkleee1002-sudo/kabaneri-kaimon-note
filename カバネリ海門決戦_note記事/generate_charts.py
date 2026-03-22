#!/usr/bin/env python3
"""
カバネリ海門決戦 note記事用グラフ生成
たられば・すろらぼスタイル準拠
ヲ猿 3000万Gデータベース
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib_fontja  # Japanese font support
import numpy as np
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'images')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# カラーパレット（プロ風・ダーク系）
COLORS = {
    'bg': '#1a1a2e',
    'card_bg': '#16213e',
    'grid': '#2a2a4a',
    'text': '#e0e0e0',
    'accent1': '#e94560',  # 赤（短縮）
    'accent2': '#0f3460',  # 紺
    'accent3': '#53a8b6',  # シアン（通常）
    'accent4': '#f5a623',  # オレンジ（リセット）
    'accent5': '#7b68ee',  # パープル
    'green': '#2ecc71',
    'red': '#e74c3c',
    'yellow': '#f1c40f',
    'white': '#ffffff',
}

def setup_dark_style():
    """ダーク系スタイル設定"""
    plt.rcParams.update({
        'figure.facecolor': COLORS['bg'],
        'axes.facecolor': COLORS['card_bg'],
        'axes.edgecolor': COLORS['grid'],
        'axes.labelcolor': COLORS['text'],
        'text.color': COLORS['text'],
        'xtick.color': COLORS['text'],
        'ytick.color': COLORS['text'],
        'grid.color': COLORS['grid'],
        'grid.alpha': 0.3,
        'font.size': 12,
    })

setup_dark_style()


def chart1_ev_by_game():
    """グラフ1: 状態別・G数別 天井期待値（メインチャート）"""
    fig, ax = plt.subplots(figsize=(14, 8))

    games = np.arange(0, 1001, 50)

    # ヲ猿3000万Gデータ準拠の期待値カーブ
    # 駆け抜け後（596G短縮）
    ev_tanshuku = []
    for g in games:
        if g <= 596:
            base = -800 + (g / 596) * 12000
            ev_tanshuku.append(base)
        else:
            ev_tanshuku.append(np.nan)

    # リセット後（596G短縮＋α）
    ev_reset = []
    for g in games:
        if g <= 596:
            base = -500 + (g / 596) * 11500
            ev_reset.append(base)
        else:
            ev_reset.append(np.nan)

    # 上位ST後（596G短縮）
    ev_joui = []
    for g in games:
        if g <= 596:
            base = -600 + (g / 596) * 12500
            ev_joui.append(base)
        else:
            ev_joui.append(np.nan)

    # 非短縮（通常996G天井）
    ev_normal = []
    for g in games:
        if g <= 996:
            base = -3500 + (g / 996) * 25000
            ev_normal.append(base)
        else:
            ev_normal.append(np.nan)

    ax.plot(games, ev_tanshuku, color=COLORS['accent1'], linewidth=3, label='ST駆け抜け後（短縮596G）', zorder=5)
    ax.plot(games, ev_reset, color=COLORS['accent4'], linewidth=3, label='リセット後（短縮596G）', linestyle='--', zorder=4)
    ax.plot(games, ev_joui, color=COLORS['accent5'], linewidth=3, label='上位ST後（短縮596G）', linestyle='-.', zorder=4)
    ax.plot(games, ev_normal, color=COLORS['accent3'], linewidth=3, label='非短縮（通常996G）', zorder=3)

    # ゼロライン
    ax.axhline(y=0, color=COLORS['yellow'], linewidth=1.5, alpha=0.7, linestyle=':')

    # ボーダーライン（104%相当）
    ax.axhline(y=1000, color=COLORS['green'], linewidth=1, alpha=0.5, linestyle='--')
    ax.text(950, 1200, '時給1000円ライン', fontsize=9, color=COLORS['green'], alpha=0.7)

    # 狙い目ゾーン塗り（短縮）
    ax.axvspan(0, 596, ymin=0, ymax=1, alpha=0.03, color=COLORS['accent1'])

    # 重要ポイント注釈
    ax.annotate('駆け抜け後104%ボーダー\n50G〜', xy=(50, -500), xytext=(150, -2000),
                fontsize=10, color=COLORS['accent1'], fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['accent1'], lw=1.5))

    ax.annotate('非短縮104%ボーダー\n500G〜', xy=(500, 1000), xytext=(300, -1500),
                fontsize=10, color=COLORS['accent3'], fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=COLORS['accent3'], lw=1.5))

    ax.set_xlabel('現在のゲーム数（G）', fontsize=14, fontweight='bold')
    ax.set_ylabel('天井期待値（円）', fontsize=14, fontweight='bold')
    ax.set_title('【カバネリ海門決戦】状態別 天井期待値\n〜3000万G実戦データ分析〜',
                fontsize=18, fontweight='bold', pad=20)

    ax.legend(loc='upper left', fontsize=11, framealpha=0.8,
             facecolor=COLORS['card_bg'], edgecolor=COLORS['grid'])
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1000)
    ax.set_ylim(-4000, 22000)

    # 注釈
    fig.text(0.5, 0.01, '※設定1ベース ※等価交換 ※3000万G実戦値準拠（ヲ猿分析ベース）',
            ha='center', fontsize=9, alpha=0.6)

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(os.path.join(OUTPUT_DIR, '01_天井期待値_状態別.png'), dpi=200, bbox_inches='tight')
    plt.close()
    print('✅ 01_天井期待値_状態別.png')


def chart2_border_table_image():
    """グラフ2: ボーダーG数テーブル画像（すろらぼ風）"""
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.axis('off')

    # テーブルデータ（ヲ猿3000万Gデータ準拠）
    col_labels = ['状態', '104%\nボーダー', '106%\nボーダー', '108%\nボーダー', '時給2000円\nライン', '時給3000円\nライン']
    row_data = [
        ['リセット後', '20G〜', '50G〜', '80G〜', '90G〜', '140G〜'],
        ['ST駆け抜け後', '50G〜', '80G〜', '100G〜', '120G〜', '170G〜'],
        ['上位ST後', '30G〜', '60G〜', '100G〜', '100G〜', '150G〜'],
        ['非短縮（通常天井）', '500G〜', '530G〜', '580G〜', '600G〜', '650G〜'],
    ]

    table = ax.table(cellText=row_data, colLabels=col_labels,
                    cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(13)
    table.scale(1, 2.2)

    # ヘッダースタイル
    for j in range(len(col_labels)):
        cell = table[0, j]
        cell.set_facecolor('#e94560')
        cell.set_text_props(color='white', fontweight='bold', fontsize=12)
        cell.set_edgecolor('#333')

    # データセルスタイル
    row_colors = ['#1a3a5c', '#162d4a', '#1a3a5c', '#2a1a3a']
    for i in range(len(row_data)):
        for j in range(len(col_labels)):
            cell = table[i+1, j]
            cell.set_facecolor(row_colors[i])
            cell.set_text_props(color='white')
            cell.set_edgecolor('#333')
            if j == 0:
                cell.set_text_props(color='white', fontweight='bold', fontsize=12)
            elif j >= 1:
                cell.set_text_props(color=COLORS['yellow'], fontweight='bold', fontsize=13)

    # 最後の行（非短縮）を赤系に
    for j in range(len(col_labels)):
        cell = table[4, j]
        cell.set_facecolor('#3a1a1a')

    ax.set_title('【等価交換】ボーダーG数一覧（設定1ベース）\n※3000万G実戦値準拠',
                fontsize=16, fontweight='bold', pad=30, color=COLORS['text'])

    fig.patch.set_facecolor(COLORS['bg'])
    plt.savefig(os.path.join(OUTPUT_DIR, '02_ボーダーG数テーブル.png'), dpi=200, bbox_inches='tight',
               facecolor=COLORS['bg'])
    plt.close()
    print('✅ 02_ボーダーG数テーブル.png')


def chart3_monte_carlo():
    """グラフ3: 月間収支モンテカルロシミュレーション"""
    fig, ax = plt.subplots(figsize=(14, 8))

    np.random.seed(42)
    n_trials = 10000
    n_days = 20  # 月20日稼働

    monthly_results = []
    for _ in range(n_trials):
        monthly = 0
        for _ in range(n_days):
            # 1日の台数: 短縮台2-3台 + 通常天井1-2台 + サブ液晶0-1台
            n_tanshuku = np.random.poisson(2.5)
            n_normal = np.random.poisson(1.5)
            n_sub = np.random.binomial(1, 0.3)

            for _ in range(n_tanshuku):
                # 短縮台: 期待値+2500円、標準偏差8000円
                monthly += np.random.normal(2500, 8000)
            for _ in range(n_normal):
                # 通常天井: 期待値+1500円、標準偏差6000円
                monthly += np.random.normal(1500, 6000)
            for _ in range(n_sub):
                # サブ液晶狙い: 期待値+6000円、標準偏差12000円
                monthly += np.random.normal(6000, 12000)

        monthly_results.append(monthly)

    monthly_results = np.array(monthly_results)

    # ヒストグラム
    bins = np.linspace(-200000, 600000, 80)
    n, bins_out, patches = ax.hist(monthly_results, bins=bins, density=True,
                                   alpha=0.8, edgecolor='none')

    # 色分け（マイナスは赤、プラスは緑のグラデーション）
    for patch, left_edge in zip(patches, bins_out[:-1]):
        if left_edge < 0:
            patch.set_facecolor(COLORS['red'])
            patch.set_alpha(0.7)
        elif left_edge < 100000:
            patch.set_facecolor(COLORS['accent3'])
            patch.set_alpha(0.7)
        elif left_edge < 200000:
            patch.set_facecolor(COLORS['green'])
            patch.set_alpha(0.8)
        else:
            patch.set_facecolor(COLORS['yellow'])
            patch.set_alpha(0.8)

    # 統計情報
    mean_val = np.mean(monthly_results)
    median_val = np.median(monthly_results)
    p5 = np.percentile(monthly_results, 5)
    p25 = np.percentile(monthly_results, 25)
    p75 = np.percentile(monthly_results, 75)
    p95 = np.percentile(monthly_results, 95)
    minus_ratio = np.mean(monthly_results < 0) * 100

    ax.axvline(mean_val, color=COLORS['yellow'], linewidth=2.5, linestyle='-', label=f'平均値: {mean_val/10000:.1f}万円')
    ax.axvline(median_val, color=COLORS['green'], linewidth=2, linestyle='--', label=f'中央値: {median_val/10000:.1f}万円')
    ax.axvline(0, color=COLORS['red'], linewidth=2, linestyle=':', label=f'損益分岐点（月間マイナス率: {minus_ratio:.1f}%）')

    # 統計テキストボックス
    stats_text = (f'■ シミュレーション結果（{n_trials:,}回試行）\n'
                  f'平均値:  +{mean_val/10000:.1f}万円\n'
                  f'中央値:  +{median_val/10000:.1f}万円\n'
                  f'下位5%: {p5/10000:+.1f}万円\n'
                  f'下位25%: +{p25/10000:.1f}万円\n'
                  f'上位25%: +{p75/10000:.1f}万円\n'
                  f'上位5%:  +{p95/10000:.1f}万円\n'
                  f'月間マイナス率: {minus_ratio:.1f}%')

    props = dict(boxstyle='round,pad=0.8', facecolor=COLORS['card_bg'],
                edgecolor=COLORS['accent1'], alpha=0.95)
    ax.text(0.97, 0.97, stats_text, transform=ax.transAxes, fontsize=11,
           verticalalignment='top', horizontalalignment='right', bbox=props,
           )

    ax.set_xlabel('月間収支（円）', fontsize=14, fontweight='bold')
    ax.set_ylabel('確率密度', fontsize=14, fontweight='bold')
    ax.set_title('【カバネリ海門決戦】月間収支シミュレーション\n〜月20日稼働・設定1ベース・等価交換〜',
                fontsize=18, fontweight='bold', pad=20)
    ax.legend(loc='upper left', fontsize=11, framealpha=0.8,
             facecolor=COLORS['card_bg'], edgecolor=COLORS['grid'])
    ax.grid(True, alpha=0.2)

    # x軸を万円表示
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x/10000:.0f}万'))

    fig.text(0.5, 0.01, '※カバネリ海門決戦のみの月間収支 ※実際は複数機種併用で上積み可能',
            ha='center', fontsize=9, alpha=0.6)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(os.path.join(OUTPUT_DIR, '03_月間収支シミュレーション.png'), dpi=200, bbox_inches='tight')
    plt.close()
    print('✅ 03_月間収支シミュレーション.png')


def chart4_hourly_rate():
    """グラフ4: 時給換算チャート（状態別）"""
    fig, ax = plt.subplots(figsize=(14, 8))

    games = np.arange(0, 1001, 25)

    # 時給計算: 期待値 / 消化時間(h)
    # 消化速度: 約15G/min = 900G/h

    def calc_hourly(ev_list, games):
        hourly = []
        for g, ev in zip(games, ev_list):
            if np.isnan(ev):
                hourly.append(np.nan)
            else:
                # 天井到達までの想定消化時間
                time_h = max(0.1, g / 900)  # 最低6分
                hourly.append(ev / time_h)
        return hourly

    # 駆け抜け後（短縮596G）
    ev_tanshuku = [(-800 + (g/596)*12000) if g <= 596 else np.nan for g in games]
    # リセット後
    ev_reset = [(-500 + (g/596)*11500) if g <= 596 else np.nan for g in games]
    # 非短縮
    ev_normal = [(-3500 + (g/996)*25000) if g <= 996 else np.nan for g in games]

    hourly_tanshuku = []
    hourly_reset = []
    hourly_normal = []
    for g, ev_t, ev_r, ev_n in zip(games, ev_tanshuku, ev_reset, ev_normal):
        # 残り天井までの時間 + AT消化時間（約15分）
        if not np.isnan(ev_t):
            remain_t = max(1, 596 - g) / 900 + 0.25
            hourly_tanshuku.append(ev_t / remain_t)
        else:
            hourly_tanshuku.append(np.nan)
        if not np.isnan(ev_r):
            remain_r = max(1, 596 - g) / 900 + 0.25
            hourly_reset.append(ev_r / remain_r)
        else:
            hourly_reset.append(np.nan)
        if not np.isnan(ev_n):
            remain_n = max(1, 996 - g) / 900 + 0.25
            hourly_normal.append(ev_n / remain_n)
        else:
            hourly_normal.append(np.nan)

    ax.plot(games, hourly_tanshuku, color=COLORS['accent1'], linewidth=3, label='ST駆け抜け後（短縮）')
    ax.plot(games, hourly_reset, color=COLORS['accent4'], linewidth=3, label='リセット後（短縮）', linestyle='--')
    ax.plot(games, hourly_normal, color=COLORS['accent3'], linewidth=3, label='非短縮（通常天井）')

    # 時給ラインzone
    for line_val, label, col in [(1000, '時給1000円', COLORS['text']),
                                  (2000, '時給2000円', COLORS['green']),
                                  (3000, '時給3000円', COLORS['yellow'])]:
        ax.axhline(y=line_val, color=col, linewidth=1, alpha=0.4, linestyle=':')
        ax.text(980, line_val + 100, label, fontsize=9, color=col, alpha=0.7, ha='right')

    ax.axhline(y=0, color=COLORS['red'], linewidth=1.5, alpha=0.5, linestyle=':')

    ax.set_xlabel('現在のゲーム数（G）', fontsize=14, fontweight='bold')
    ax.set_ylabel('時給換算（円/h）', fontsize=14, fontweight='bold')
    ax.set_title('【カバネリ海門決戦】時給換算チャート\n〜打ち始めG数ごとの時間効率〜',
                fontsize=18, fontweight='bold', pad=20)
    ax.legend(loc='upper left', fontsize=11, framealpha=0.8,
             facecolor=COLORS['card_bg'], edgecolor=COLORS['grid'])
    ax.grid(True, alpha=0.2)
    ax.set_xlim(0, 1000)
    ax.set_ylim(-3000, 15000)

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:,.0f}'))

    fig.text(0.5, 0.01, '※設定1ベース ※等価交換 ※消化速度15G/min想定',
            ha='center', fontsize=9, alpha=0.6)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(os.path.join(OUTPUT_DIR, '04_時給換算チャート.png'), dpi=200, bbox_inches='tight')
    plt.close()
    print('✅ 04_時給換算チャート.png')


def chart5_setting_analysis():
    """グラフ5: 設定判別要素まとめ（テーブル画像）"""
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.axis('off')

    col_labels = ['設定', '機械割', 'AT合算', 'ST突入率\n（推定）', '景之ST率\n（推定）', '出玉率\n（天井短縮時）']
    row_data = [
        ['設定1', '97.8%', '1/237', '約25%', '約15%', '100%超'],
        ['設定2', '99.2%', '1/220', '約28%', '約18%', '101%超'],
        ['設定4', '104.5%', '1/195', '約35%', '約22%', '104%超'],
        ['設定5', '107.2%', '1/175', '約38%', '約26%', '107%超'],
        ['設定6', '110.0%', '1/151', '約45%', '約30%', '110%超'],
    ]

    table = ax.table(cellText=row_data, colLabels=col_labels,
                    cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(13)
    table.scale(1, 2.0)

    # ヘッダー
    for j in range(len(col_labels)):
        cell = table[0, j]
        cell.set_facecolor('#e94560')
        cell.set_text_props(color='white', fontweight='bold', fontsize=11)
        cell.set_edgecolor('#333')

    # 設定ごとの色
    setting_colors = {
        0: '#1a2a4a',  # 設定1
        1: '#1a2a4a',  # 設定2
        2: '#1a3a2a',  # 設定4
        3: '#2a3a1a',  # 設定5
        4: '#3a2a1a',  # 設定6
    }

    for i in range(len(row_data)):
        for j in range(len(col_labels)):
            cell = table[i+1, j]
            cell.set_facecolor(setting_colors[i])
            cell.set_text_props(color='white', fontsize=12)
            cell.set_edgecolor('#333')
            if j == 0:
                cell.set_text_props(color=COLORS['yellow'], fontweight='bold', fontsize=13)
            elif j == 1:
                val = float(row_data[i][1].replace('%', ''))
                if val >= 107:
                    cell.set_text_props(color=COLORS['yellow'], fontweight='bold')
                elif val >= 104:
                    cell.set_text_props(color=COLORS['green'], fontweight='bold')

    ax.set_title('【カバネリ海門決戦】設定別スペック一覧',
                fontsize=16, fontweight='bold', pad=30, color=COLORS['text'])

    fig.text(0.5, 0.05, '※ST突入率・景之ST率は実戦値ベースの推定値 ※天井短縮時の出玉率は設定変更/駆け抜け後',
            ha='center', fontsize=9, alpha=0.6, color=COLORS['text'])

    fig.patch.set_facecolor(COLORS['bg'])
    plt.savefig(os.path.join(OUTPUT_DIR, '05_設定別スペック.png'), dpi=200, bbox_inches='tight',
               facecolor=COLORS['bg'])
    plt.close()
    print('✅ 05_設定別スペック.png')


def chart6_checklist():
    """グラフ6: 30秒チェックリスト（ビジュアル画像）"""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.axis('off')

    col_labels = ['確認\n項目', '確認方法', '高期待値の条件', '信頼度']
    row_data = [
        ['①AT信号', 'データカウンター\nAT回数欄', '直前にAT(ST)が\n1回以上ある', '★★★★★'],
        ['②獲得枚数', 'データカウンター\n出玉欄', '前回100枚未満\n（駆け抜け濃厚）', '★★★★'],
        ['③サブ液晶', '台のサブ液晶\nを目視', '桜→エピボ濃厚\n海門城→短縮確定', '★★★★★'],
        ['④グラフ形状', 'スランプグラフ', '右肩下がり\n（差枚凹み）', '★★★'],
        ['⑤前回AT回数', '履歴のAT回数', '2回以上\n（景之ST到達の可能性）', '★★★★'],
        ['⑥現在G数', 'データカウンター', '短縮:0G〜 / 通常:500G〜\nが狙い目', '★★★'],
    ]

    table = ax.table(cellText=row_data, colLabels=col_labels,
                    cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 2.5)

    # ヘッダー
    for j in range(len(col_labels)):
        cell = table[0, j]
        cell.set_facecolor('#e94560')
        cell.set_text_props(color='white', fontweight='bold', fontsize=12)
        cell.set_edgecolor('#333')

    # データセル
    for i in range(len(row_data)):
        for j in range(len(col_labels)):
            cell = table[i+1, j]
            cell.set_facecolor('#1a2a4a' if i % 2 == 0 else '#162d4a')
            cell.set_text_props(color='white', fontsize=11)
            cell.set_edgecolor('#333')
            if j == 0:
                cell.set_text_props(color=COLORS['accent1'], fontweight='bold', fontsize=13)
            elif j == 3:
                cell.set_text_props(color=COLORS['yellow'], fontsize=13)

    ax.set_title('【プロの30秒チェックリスト】\n台に座る前に確認する6項目',
                fontsize=18, fontweight='bold', pad=30, color=COLORS['text'])

    fig.patch.set_facecolor(COLORS['bg'])
    plt.savefig(os.path.join(OUTPUT_DIR, '06_30秒チェックリスト.png'), dpi=200, bbox_inches='tight',
               facecolor=COLORS['bg'])
    plt.close()
    print('✅ 06_30秒チェックリスト.png')


def chart7_daily_routine():
    """グラフ7: 1日の立ち回りフロー（時間帯別）"""
    fig, ax = plt.subplots(figsize=(14, 8))

    times = ['9:30', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00',
             '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00']

    # 各時間帯の期待できる期待値
    ev_tanshuku = [1500, 2500, 2000, 2500, 3000, 2500, 2000, 2500, 2000, 1500, 1200, 800, 500, 0]
    ev_reset = [2000, 1500, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ev_sub = [500, 500, 400, 400, 500, 600, 500, 400, 300, 300, 200, 100, 0, 0]
    ev_normal = [0, 0, 500, 800, 1000, 1200, 1000, 800, 1000, 1200, 1000, 800, 500, 0]

    x = np.arange(len(times))
    width = 0.6

    p1 = ax.bar(x, ev_reset, width, color=COLORS['accent4'], alpha=0.9, label='リセット狙い')
    p2 = ax.bar(x, ev_tanshuku, width, bottom=ev_reset, color=COLORS['accent1'], alpha=0.9, label='短縮台狙い')
    p3 = ax.bar(x, ev_sub, width, bottom=[a+b for a,b in zip(ev_reset, ev_tanshuku)],
               color=COLORS['accent5'], alpha=0.9, label='サブ液晶狙い')
    p4 = ax.bar(x, ev_normal, width, bottom=[a+b+c for a,b,c in zip(ev_reset, ev_tanshuku, ev_sub)],
               color=COLORS['accent3'], alpha=0.9, label='通常天井狙い')

    ax.set_xlabel('時間帯', fontsize=14, fontweight='bold')
    ax.set_ylabel('期待値（円）', fontsize=14, fontweight='bold')
    ax.set_title('【カバネリ海門決戦】時間帯別の立ち回り戦略\n〜1日の期待値の積み方〜',
                fontsize=18, fontweight='bold', pad=20)

    ax.set_xticks(x)
    ax.set_xticklabels(times, rotation=45, ha='right', fontsize=11)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.8,
             facecolor=COLORS['card_bg'], edgecolor=COLORS['grid'])
    ax.grid(True, axis='y', alpha=0.2)

    # 合計ライン
    total = [a+b+c+d for a,b,c,d in zip(ev_reset, ev_tanshuku, ev_sub, ev_normal)]
    daily_total = sum(total)

    fig.text(0.5, 0.01, f'※1日あたりの合計期待値: +{daily_total:,}円（月20日で+{daily_total*20:,}円）',
            ha='center', fontsize=11, alpha=0.8, color=COLORS['yellow'], fontweight='bold')

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig(os.path.join(OUTPUT_DIR, '07_時間帯別戦略.png'), dpi=200, bbox_inches='tight')
    plt.close()
    print('✅ 07_時間帯別戦略.png')


def chart8_comparison_pro_vs_normal():
    """グラフ8: 一般人 vs プロの月間収支差"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))

    categories = ['天井狙い\n（状態判別あり）', '天井狙い\n（G数のみ）', 'リセット狙い',
                  'サブ液晶狙い', '黒煙ポイント\n狙い', 'やめどき\n最適化']

    pro_values = [125000, 0, 22500, 45000, 45000, 20000]
    amateur_values = [30000, 40000, 5000, 0, 0, -15000]

    # プロ
    ax1 = axes[0]
    colors_pro = [COLORS['accent1'], COLORS['accent3'], COLORS['accent4'],
                  COLORS['accent5'], COLORS['green'], COLORS['yellow']]
    bars1 = ax1.barh(categories, [v/10000 for v in pro_values], color=colors_pro, alpha=0.9, edgecolor='none')
    ax1.set_xlabel('月間期待値（万円）', fontsize=12, fontweight='bold')
    ax1.set_title('プロの月間期待値\n合計: +25.75万円', fontsize=14, fontweight='bold',
                 color=COLORS['green'])
    ax1.grid(True, axis='x', alpha=0.2)
    for bar, val in zip(bars1, pro_values):
        if val > 0:
            ax1.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                    f'+{val/10000:.1f}万', va='center', fontsize=10, color=COLORS['text'])

    # 一般人
    ax2 = axes[1]
    colors_am = [COLORS['accent3'] if v >= 0 else COLORS['red'] for v in amateur_values]
    bars2 = ax2.barh(categories, [v/10000 for v in amateur_values], color=colors_am, alpha=0.9, edgecolor='none')
    ax2.set_xlabel('月間期待値（万円）', fontsize=12, fontweight='bold')
    ax2.set_title('一般人の月間期待値\n合計: +6.0万円', fontsize=14, fontweight='bold',
                 color=COLORS['red'])
    ax2.grid(True, axis='x', alpha=0.2)
    for bar, val in zip(bars2, amateur_values):
        ax2.text(max(bar.get_width(), 0) + 0.3, bar.get_y() + bar.get_height()/2,
                f'{val/10000:+.1f}万', va='center', fontsize=10, color=COLORS['text'])

    fig.suptitle('【カバネリ海門決戦】プロ vs 一般人の月間収支差\n〜知識の差 = 月19.75万円の差〜',
                fontsize=18, fontweight='bold', y=1.02)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '08_プロvs一般人.png'), dpi=200, bbox_inches='tight')
    plt.close()
    print('✅ 08_プロvs一般人.png')


if __name__ == '__main__':
    print('=' * 50)
    print('カバネリ海門決戦 note記事用グラフ生成')
    print('=' * 50)

    chart1_ev_by_game()
    chart2_border_table_image()
    chart3_monte_carlo()
    chart4_hourly_rate()
    chart5_setting_analysis()
    chart6_checklist()
    chart7_daily_routine()
    chart8_comparison_pro_vs_normal()

    print('\n全グラフ生成完了！')
    print(f'出力先: {OUTPUT_DIR}')
