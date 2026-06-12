import sys, os

SCRIPTS_DIR = "/root/.claude/skills/vedic-calculator/scripts"
sys.path.insert(0, SCRIPTS_DIR)

from engine import calculate_full_chart
from transit import calc_transit
from formatter import format_structured_data

chart = calculate_full_chart(
    year=1995, month=8, day=19,
    hour=23, minute=30,
    lat=26.4226, lon=112.8598,
    tz_str="Asia/Shanghai"
)

transit = calc_transit(
    chart['lagna']['sign_idx'],
    chart['planets']['Moon']['sign_idx'],
    "Asia/Shanghai"
)

meta = {
    'dob': '1995-08-19',
    'time': '23:30',
    'place': '湖南省耒阳市',
    'lat': 26.4226, 'lon': 112.8598,
    'time_precision': '精确到分钟',
    'time_source': '未追问'
}

user_info = {
    'gender': '未提供',
    'relationship': '未提供'
}

md = format_structured_data(chart, transit, meta, user_info)
with open("/home/user/vedic-astro-skills/structured_data.md", 'w', encoding='utf-8') as f:
    f.write(md)

SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
sav_total = sum(chart['sav'].get(s, 0) for s in SIGNS)
print(f"SAV total: {sav_total}")
assert sav_total == 337, f"SAV FAILED: {sav_total} != 337"

print(f"Lagna: {chart['lagna']['sign']} {chart['lagna']['deg_str']}")
for p in ['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu']:
    pl = chart['planets'][p]
    print(f"{p}: {pl['sign']} {pl['deg_str']} H{pl['house']} {'(R)' if pl['retrograde'] else ''}")

rahu_lon = chart['planets']['Rahu']['longitude']
ketu_lon = chart['planets']['Ketu']['longitude']
diff = abs(rahu_lon - ketu_lon) % 360
print(f"Ra-Ke diff: {diff}")
print("OK")
