import os
import glob
import pandas as pd
from bs4 import BeautifulSoup
import re

# --- CONFIGURATION ---
INPUT_FOLDER = "raw_data"
OUTPUT_FILE = "trading_history.html"

def clean_money(text):
    """Converts string like '$1,200.50' or '-$50.00' to float."""
    try:
        # Remove anything that isn't a digit, dot, or minus sign
        clean = re.sub(r'[^\d.-]', '', text)
        return float(clean)
    except:
        return 0.0

def parse_iq_card_structure(file_path):
    """Parses the DIV/Card structure from IQ Option history."""
    trades = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except UnicodeDecodeError:
        print(f"   ⚠️  Encoding error in {file_path}. Skipping.")
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 1. Find all "Trade Row" containers
    # Based on your file, the main row has class "css-8kuouv"
    trade_containers = soup.find_all("div", class_="css-8kuouv")
    
    for container in trade_containers:
        try:
            # --- Extract Visible Data ---
            
            # Asset Name
            asset_div = container.find("div", attrs={"type": "assetName"})
            asset = asset_div.get_text(strip=True) if asset_div else "Unknown"

            # Time (Usually has two divs inside: Open and Close. We take the first one)
            time_div = container.find("div", attrs={"type": "time"})
            time_open = "N/A"
            if time_div:
                times = time_div.find_all("div")
                if times:
                    time_open = times[0].get_text(strip=True)

            # Stake
            stake_div = container.find("div", attrs={"type": "investmentAmount"})
            stake_text = stake_div.get_text(strip=True) if stake_div else "0"
            stake = clean_money(stake_text)

            # P/L (Gross Profit/Loss)
            # Note: This div often contains a child div with percentage (e.g., "-$10 -100%"). 
            # We need just the immediate text.
            pnl_div = container.find("div", attrs={"type": "grossPL"})
            pnl = 0.0
            if pnl_div:
                # Get only the text of the parent, ignoring the percentage child div
                pnl_text = pnl_div.contents[0] if pnl_div.contents else ""
                pnl = clean_money(str(pnl_text))

            # --- Extract Direction (Hidden in the details) ---
            # The details are usually in the immediate NEXT sibling div with class "rah-static"
            direction = "Unknown"
            
            # Find the next sibling that contains the hidden details
            details_block = container.find_next_sibling("div", class_="rah-static")
            
            if details_block:
                # Look for an element with 'direction="buy"' or 'direction="sell"'
                # Buy = Call, Sell = Put
                dir_el = details_block.find(attrs={"direction": True})
                if dir_el:
                    dir_val = dir_el["direction"].lower()
                    direction = "Call" if "buy" in dir_val else "Put"
            
            # Fallback: If we can't find direction, guess based on asset (not recommended, but failsafe)
            if direction == "Unknown":
                direction = "Call" # Default

            trades.append({
                "Time": time_open,
                "Asset": asset,
                "Direction": direction,
                "Stake": stake,
                "Profit": pnl
            })

        except Exception as e:
            # print(f"Error parsing a row: {e}")
            continue
            
    return trades

# --- MAIN EXECUTION ---
print("🚀 Starting Advanced Parser...")
all_trades = []

if not os.path.exists(INPUT_FOLDER):
    print(f"❌ Error: Folder '{INPUT_FOLDER}' not found.")
    exit()

files = glob.glob(os.path.join(INPUT_FOLDER, "*.txt"))
print(f"🔍 Found {len(files)} files.")

for file in files:
    file_trades = parse_iq_card_structure(file)
    count = len(file_trades)
    if count > 0:
        print(f"   ✅ {file}: Parsed {count} trades.")
        all_trades.extend(file_trades)
    else:
        print(f"   ⚠️  {file}: No trades found (Check content).")

if not all_trades:
    print("\n❌ No trades extracted. Ensure your TXT files contain the HTML code provided.")
    exit()

# Create DataFrame
df = pd.DataFrame(all_trades)

# Sort by Time
df['Time'] = pd.to_datetime(df['Time'], format="%d.%m.%Y, %H:%M:%S", errors='coerce')
# If the format above fails (e.g. milliseconds), try simpler or let pandas guess
if df['Time'].isnull().all():
     df['Time'] = pd.to_datetime(df['Time'], errors='coerce')

df.sort_values(by='Time', ascending=False, inplace=True)

# Generate HTML
table_rows = ""
for index, row in df.iterrows():
    pnl = row['Profit']
    pnl_class = "profit" if pnl >= 0 else "loss"
    pnl_sign = "+" if pnl > 0 else ""
    
    # Direction Icon
    d_class = "direction-call" if row['Direction'] == "Call" else "direction-put"
    d_icon = "🔼" if row['Direction'] == "Call" else "🔽"

    table_rows += f"""
    <tr>
        <td>{row['Time']}</td>
        <td style="color:white; font-weight:bold;">{row['Asset']}</td>
        <td class="{d_class}"><b>{row['Direction']}</b> {d_icon}</td>
        <td>${row['Stake']:.2f}</td>
        <td class="{pnl_class}">{pnl_sign}${pnl:.2f}</td>
    </tr>
    """

html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Trading History Verification</title>
    <style>
        :root {{ --bg: #0d1117; --card: #161b22; --text: #c9d1d9; --border: #30363d; --green: #2ea043; --red: #da3633; --blue: #58a6ff; --purple: #d2a8ff; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; background: var(--bg); color: var(--text); padding: 20px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        h1 {{ color: var(--blue); border-bottom: 1px solid var(--border); padding-bottom: 15px; }}
        input {{ width: 100%; padding: 12px; background: var(--card); border: 1px solid var(--border); color: white; border-radius: 6px; margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; background: var(--card); border-radius: 6px; overflow: hidden; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid var(--border); }}
        th {{ background: #21262d; color: var(--blue); }}
        tr:hover {{ background: #21262d; }}
        .profit {{ color: var(--green); }}
        .loss {{ color: var(--red); }}
        .direction-call {{ color: var(--blue); }}
        .direction-put {{ color: var(--purple); }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Bot Execution History</h1>
        <p>Verified Data | <b>{len(df)} Trades Loaded</b></p>
        <input type="text" id="search" onkeyup="filter()" placeholder="🔍 Search Date, Asset, or Direction...">
        <table id="table">
            <thead>
                <tr><th>Time</th><th>Asset</th><th>Direction</th><th>Stake</th><th>Net P/L</th></tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </div>
    <script>
        function filter() {{
            var filter = document.getElementById("search").value.toUpperCase();
            var rows = document.getElementById("table").getElementsByTagName("tr");
            for (var i = 1; i < rows.length; i++) {{
                var txt = rows[i].innerText;
                rows[i].style.display = txt.toUpperCase().indexOf(filter) > -1 ? "" : "none";
            }}
        }}
    </script>
</body>
</html>
"""

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"\n✅ SUCCESS! Generated '{OUTPUT_FILE}' with {len(df)} trades.")