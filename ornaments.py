import unicodedata

ornaments = """\
👶 Baby
👼 Baby Angel
🎅 Santa Claus
🤶 Mrs. Claus
🧑‍🎄 Mx Claus
🧝 Elf
🧝‍♂️ Man Elf
🧝‍♀️ Woman Elf
👪 Family
🦌 Deer
🍪 Cookie
🥛 Glass of Milk
🍷 Wine Glass
🍴 Fork and Knife
⛪ Church
🌟 Glowing Star
⛄ Snowman Without Snow
🔥 Fire
🎄 Christmas Tree
🎁 Wrapped Gift
🧦 Socks
🔔 Bell
🎶 Musical Notes
🕯️ Candle
❄️ Snowflake
☃️ Snowman
""".splitlines()

# Double width ornaments (not candle, snowflake or snowman)
# split() to preserve modifiers
wide = [o.split()[0] for o in ornaments if unicodedata.east_asian_width(o[0]) == "W"]
