import pandas as pd
import json
import re
from datetime import datetime, timezone

INPUT_FILE = "athletic_latest.xlsx"
OUTPUT_FILE = "athletic_latest.json"

# The Athletic spreadsheet's OVR & VORP Ranks sheet
df = pd.read_excel(
    INPUT_FILE,
    sheet_name="OVR & VORP Ranks",
    header=0
)

# Overall rankings are in columns RK through VORP
# Columns:
# 40 = RK
# 41 = OVERALL PLAYER
# 42 = POS RK
# 43 = BYE
# 44 = FPS
# 45 = VORP

players = []

for _, row in df.iterrows():
    name = row.iloc[41]

    if pd.isna(name):
        continue

    name = str(name).strip()

    if not name or name == "OVERALL PLAYER":
        continue

    overall_rank = row.iloc[40]
    pos_rank = row.iloc[42]
    fps = row.iloc[44]
    vorp = row.iloc[45]

    # Convert values safely
    try:
        overall_rank = int(overall_rank)
    except (ValueError, TypeError):
        overall_rank = None

    try:
        fps = float(fps)
    except (ValueError, TypeError):
        fps = None

    try:
        vorp = float(vorp)
    except (ValueError, TypeError):
        vorp = None

    # Extract position and positional rank.
    # Examples: WR1, RB12, QB4, TE7
    position = None
    positional_rank = None

    if not pd.isna(pos_rank):
        pos_rank_text = str(pos_rank).strip()
        match = re.match(r"^(QB|RB|WR|TE)(\d+)$", pos_rank_text)

        if match:
            position = match.group(1)
            positional_rank = int(match.group(2))

    players.append({
        "name": name,
        "position": position,
        "overallRank": overall_rank,
        "positionalRank": positional_rank,
        "fps": fps,
        "vorp": vorp
    })

output = {
    "source": "The Athletic",
    "sheet": "OVR & VORP Ranks",
    "updatedAt": datetime.now(timezone.utc).isoformat(),
    "players": players
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, allow_nan=False)

print(f"Created {OUTPUT_FILE} with {len(players)} players.")
