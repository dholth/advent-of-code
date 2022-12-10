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
🍇 Grapes
🍈 Melon
🍉 Watermelon
🍊 Tangerine
🍋 Lemon
🍌 Banana
🍍 Pineapple
🥭 Mango
🍎 Red Apple
🍏 Green Apple
🍐 Pear
🍑 Peach
🍒 Cherries
🍓 Strawberry
🫐 Blueberries
🥝 Kiwi Fruit
🥥 Coconut
🥑 Avocado
🍆 Eggplant
🥔 Potato
🥕 Carrot
🌽 Ear of Corn
🌶️ Hot Pepper
🫑 Bell Pepper
🥒 Cucumber
🥬 Leafy Green
🥦 Broccoli
🧄 Garlic
🧅 Onion
🍄 Mushroom
🥜 Peanuts
🫘 Beans
🌰 Chestnut
🍞 Bread
🥐 Croissant
🥖 Baguette Bread
🥨 Pretzel
🥯 Bagel
🥞 Pancakes
🧇 Waffle
🧀 Cheese Wedge
🍖 Meat on Bone
🍗 Poultry Leg
🍦 Soft Ice Cream
🍧 Shaved Ice
🍨 Ice Cream
🍩 Doughnut
🍪 Cookie
🎂 Birthday Cake
🍰 Shortcake
🧁 Cupcake
🥧 Pie
🍫 Chocolate Bar
🍬 Candy
🍭 Lollipop
🍮 Custard
🍯 Honey Pot
🍼 Baby Bottle
🥛 Glass of Milk
☕ Hot Beverage
🍾 Bottle with Popping Cork
🍷 Wine Glass
🍸 Cocktail Glass
🍹 Tropical Drink
🍺 Beer Mug
🍻 Clinking Beer Mugs
🥂 Clinking Glasses
🥃 Tumbler Glass
🫗 Pouring Liquid
🥤 Cup with Straw
🧋 Bubble Tea
🧃 Beverage Box
🧉 Mate
🧊 Ice
🥢 Chopsticks
🍽️ Fork and Knife with Plate
🥄 Spoon
🫙 Jar
""".splitlines()

# Double width ornaments (not candle, snowflake or snowman)
# split() to preserve modifiers
wide = [o.split()[0] for o in ornaments if unicodedata.east_asian_width(o[0]) == "W"]
