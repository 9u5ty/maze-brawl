from data import gear, hero_colors, items

from fighters import add_item, equip_from_bag, gain_gear, gear_bonus, is_upgrade, item_ids_in_bag, item_sell_value, remove_item, sell_gear, sell_item, sell_value, slot_of, unique, use_food

from menus import help_screen

from screen_render import center, clear_screen, col, flush_keys, get_key, hline, put, show

from state import g

from texts import atk_text, def_text, gear_label, gear_stat_name, item_summary, move_cost, move_summary
#build the core function first
# show the price of the item, pro means the product player may intend to buy
def price_of(ident):
    if ident in items:
        return items[ident]["price"]
    else:
        return gear[ident]["price"]

#build the buy and sell one
def buy(ident):
    data = g["player"]
    if ident in gear and not is_upgrade(data, ident):
        return "That is no better than what you already wear."
    if data["gold"]< price_of(ident):
        return "Not enough gold."
    else:
        data["gold"] -= price_of(ident)
        if ident in items:
            add_item(data,ident)
            return f"Bought {items[ident]['name']}."
        else:
            gain_gear(data,ident)
            return f"Bought {gear[ident]['name']}."
def sell(ident):
    data = g["player"]
    if ident in gear:
        if ident not in data["bag"]:
            return "No spare gear."
        sell_gear(data,ident)
        return f"Sold {gear[ident]['name']}."
    else:
        if data["items"].get(ident, 0) <= 0:
            return "You don't have that item."
        sell_item(data,ident)
        return f"Sold {items[ident]['name']}."

#use item
def use_entry(data,kind,ident):
    if kind == "gear":
        if ident not in data["bag"]:
            return "No spare gear."
        equip_from_bag(data,ident)
        return f"Equipped {gear[ident]['name']}."
    if data["items"].get(ident, 0) <= 0:
        return "You don't have that item."
    info = items[ident]
    if info.get("combat_only",False):
        return "This item can only be used in combat."
    if "hp" in info and data["hp"] >= data["max_hp"]:
        return "Your HP is already full."
    if "mp" in info and data["mp"] >= data["max_mp"]:
        return "Your MP is already full."
    remove_item(data,ident)
    return use_food(data,ident)


#build the inventory for shop
#choose corresponding shops
def stock_for_shop(number):
    shop = g["mapdef"]["shops"]
    if not shop:
        return[]
    return shop[min(number,len(shop)-1)]

#build the buy and sell interaction
def sell_buy(stock,tab):
    data = g["player"]
    a = []
    if tab ==0:
        for ident in stock:
            a.append((ident,price_of(ident)))
        return a
    else:
        for ident in unique(data["bag"]):
            a.append((ident,sell_value(ident)))
        for ident in item_ids_in_bag(data):
            a.append((ident,item_sell_value(ident)))
    return a
#link between sell_buy and inventory to show the things
def inventory_entry(data):
    ent = []
    for ident in item_ids_in_bag(data):
        ent.append(("item",ident))
    for ident in unique(data["bag"]):
        ent.append(("gear",ident))
    return ent
#connection between player and store&inventory page
#select stuff
def move_cursor(k,cur,count):
    if count == 0:
        return cur
    if k =="UP":
        return (cur - 1) % count
    if k =="DOWN":
        return (cur + 1) % count
    return cur
#run the shops and inventory
def shop_screen(number):
    stock = stock_for_shop(number)
    tab, cur, notice = 0,0,""
    while True:
        a = sell_buy(stock,tab)
        cur = min(cur,max(0,len(a)-1))
        draw_s(number,tab,a,cur,notice)
        notice = ""
        key = get_key()
        if key in ("ESC","e"):
            flush_keys()
            return
        if key and len(key)==1 and key in "1234567890" and 1 <= int(key) <= len(a):
            cur = int(key) - 1
        elif key in ("LEFT","RIGHT"):
            tab,cur = 1-tab,0
        elif key =="ENTER" and a:
            ident = a[cur][0]
            if tab == 0:
                notice = buy(ident)
            else:
                notice = sell(ident)
        elif key =="h":
            help_screen()
        else:
            cur = move_cursor(key,cur,len(a))
def inventory_screen():
    data = g["player"]
    cur, notice = 0,""
    while True:
        ent = inventory_entry(data)
        cur = min(cur,max(0,len(ent)-1))
        draw_inv(data,ent,cur,notice)
        notice = ""
        key = get_key()
        if key in ("ESC","i"):
            flush_keys()
            return
        elif key =="ENTER" and ent:
            kind, ident = ent[cur]
            notice = use_entry(data,kind,ident)
        elif key == "h":
            help_screen()
        else:
            cur = move_cursor(key,cur,len(ent))

#labels and selection indicators
#label for shop
def s_row_text(data,i,ident,tab):
    label = f"{i+1}. "
    if ident in items:
        count = data["items"].get(ident,0)
        return label+f"{items[ident]['name']}   ({count})"
    info = gear[ident]
    label += f"{info['name']}  (+{info['bonus']} {gear_stat_name(info)})"
    if tab == 0 and not is_upgrade(data,ident):
        label += " (Not an upgrade)"
    if tab == 1 :
        label += f" x{data['bag'].count(ident)}"
    return label
# label for inventory
def in_entry_txt(data,kind,ident):
    if kind =="item":
        return f"{items[ident]['name']} x {data['items'][ident]} - {item_summary(items[ident])}"
    else:
        l = gear_label(ident)
        if is_upgrade(data,ident):
            l += " (Upgrade)"
        return l
# join owned gear to sth easy to read
def bag_names(data):
    name = []
    for ident in data["bag"]:
        name.append(gear[ident]["name"])
    if not name:
        return "Empty"
    else:
        return ", ".join(name)
#tell player where the position of selection is
def arrow(label,selected):
    if selected:
        return ">" + label
    else:
        return " " + label

#draw the shop and inventory
#draw the row
def draw_s_row(data,i,price,ident,tab,cur):
    affordable = tab == 1 or (data["gold"] >= price and (ident in items or is_upgrade(data, ident)))
    attr = col("yellow" if affordable else "red", bold=affordable, dim=not affordable, reverse=(i == cur))
    text = arrow(s_row_text(data,i,ident,tab), i == cur)
    y = 5+i - max(0,cur - 8)
    put(y,4,f"{text:<50}",attr)
    put(y,58,f"{price:>4}$",attr)
#detail of the product in the shop
def draw_s_detail(data,ident,tab):
    if ident in items:
        put(15,4,item_summary(items[ident]),col("cyan"))
        return
    if tab == 1:
        return
    info = gear[ident]
    bonus = gear_bonus(data[slot_of(ident)])
    text = f"{info['name']}: {gear_stat_name(info)} (+{bonus})->(+{info['bonus']})"
    put(15,4,text,col("yellow"))
#header of shop can character property
def draw_s_header(number,tab,data):
    title = f"SHOP #{number+1}"
    center(0,title,col("green",bold = True))
    put(1,2,f"Gold: {data['gold']}",col("yellow",bold = True))
    text = f"HP: {data['hp']}/{data['max_hp']}   MP: {data['mp']}/{data['max_mp']}"
    put(1,20,text + f"   ATK: {atk_text(data)}   DEF: {def_text(data)}")
    buy_label, sell_label = "BUY", "SELL"
    if tab == 0:
        buy_label = "[BUY]"
    else:
        sell_label = "[SELL]"
    put(3,4,buy_label,col("blue",bold = True,reverse = (tab ==0)))
    put(3,11,sell_label,col("blue",bold = True,reverse = (tab ==1)))
    put(3,20,"LEFT/RIGHT: Switch tabs",col(dim = True))
    hline(4)
#draw rest info
def draw_s_footer(data,notice):
    put(17,2,f"Weapon: {gear_label(data['weapon'])}",col(dim = True))
    put(18,2,f"Armor: {gear_label(data['armor'])}",col(dim = True))
    put(19,2,f"Bag: {bag_names(data)}"[:76],col(dim = True))
    if notice:
        put(21,2,notice,col("green",bold = True))
    hint = "UP/DOWN/1-9: Select  ENTER: Buy/sell  LEFT/RIGHT: Tab  ESC: Leave  H: Help"
    put(23,2,hint,col("cyan"))
#combine all component shop screen together
def draw_s(number,tab,rows,cur,notice):
    data = g["player"]
    clear_screen()
    draw_s_header(number,tab,data)
    if not rows:
        message = "Nothing to sell."
        if tab == 0:
            message = "Out of stock."
        put(6,4,message,col(dim = True))
    top = max(0,cur - 8)
    for i in range(top,min(len(rows),top+9)):
        ident,price = rows[i]
        draw_s_row(data,i,price,ident,tab,cur)
    hline(14)
    if rows:
        draw_s_detail(data,rows[cur][0],tab)
    if len(rows) > 9:
        put(16,4,f"Rows {top+1}-{min(len(rows),top+9)} of {len(rows)}; use UP/DOWN to scroll.")
    draw_s_footer(data,notice)
    show()

#basic infor in inventory , like items/gear/property and etc
def draw_inv_stats(data):
    put(2,2,f"{data['name']} ({data['role']})",col(hero_colors[data["key"]],bold = True))
    text = f"HP: {data['hp']}/{data['max_hp']}   MP: {data['mp']}/{data['max_mp']}"
    put(3,2,text + f"   Gold: {data['gold']}   SPD: {data['spd']}")
    put(4,2, f"ATK: {atk_text(data)}   DEF: {def_text(data)}")
    put(5,2, f"Weapon: {gear_label(data['weapon'])}")
    put(6,2,f"Armor: {gear_label(data['armor'])}")
    put(7,2,f"Bag: {bag_names(data)}"[:74])
    put(8,2,f"Moves:",col("blue",bold = True))
    for i,move in enumerate(data["moves"]):
        summary = move_summary(move)
        put(9+i,4,f"{move['name']:<15}{move_cost(move):>5}    {summary}"[:74])
#the structure of inventory display
def draw_inv(data,entries,cur,notice):
    clear_screen()
    center(0,"INVENTORY",col("green",bold = True))
    draw_inv_stats(data)
    put(14,2,"Bag (Enter to use/equip):",col("yellow",bold = True))
    if not entries:
        put(15,4,"Your bag is empty.",col(dim = True))
    top = max(0,cur - 6)
    for i in range(top,min(len(entries),top+7)):
        kind , ident = entries[i]
        text = in_entry_txt(data,kind,ident)[:70]
        attr = col("yellow",bold = True,reverse = (i==cur))
        put(15+i-top,4,arrow(text,i==cur),attr)
    if notice:
        put(22,2,notice,col("green",bold = True))
    put(23,2,"UP/DOWN: Select  ENTER: Use/equip  ESC or I: Close  H: Help",col("cyan"))
    show()
