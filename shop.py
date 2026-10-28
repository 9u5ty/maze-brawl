from game.data import gear, hero_colors, items, monsters

from game.fighters import (
    add_item, atk_total, def_total, equip_from_bag, gain_gear,
    gear_bonus, is_upgrade, item_ids_in_bag, item_sell_value,
    remove_item, sell_gear, sell_item, sell_value, slot_of,
    unique, use_food
)

from game.menus import help_screen

from game.screen import (
    screen_w, center, clear_screen, col, flush_keys, get_key,
    hline, put, show
)

from game.state import g

from game.texts import (
    atk_text, def_text, gear_label, gear_stat_name,
    item_summary, move_cost, move_summary
)
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
    if data["gold"]< price_of(ident):
        return "not enough gold"
    else:
        data["gold"] -= price_of(ident)
        if ident in items:
            add_item(data,ident)
            return f"buy {items[ident]["name"]}"
        else:
            gain_gear(data,ident)
            return f"buy {gear[ident]["name"]}"
def sell(ident):
    data = g["player"]
    if ident in gear:
        if ident not in data["bag"]:
            return "no spare gear"
        sell_gear(data,ident)
        return f"sell {gear[ident]["name"]}"
    else:
        if data["items"].get(ident) is None:
            return "u don't have that item"
        sell_item(data,ident)
        return f"sell {items[ident]["name"]}"

#use item
def use_entry(data,kind,ident):
    if kind == "gear":
        if ident not in data["bag"]:
            return "no spare gear"
        equip_from_bag(data,ident)
    if data["items"].get[ident] is None:
        return "u don't have that item"
    info = items[ident]
    if info.get("combat only",False):
        return "combat only"
    if "hp" in info and data["hp"] >= data["max_hp"]:
        return "max hp already"
    if "mp" in info and data["mp"] >= data["max_mp"]:
        return "max mp already"
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
        for ident in items(data["items"]):
            a.append((ident,item_sell_value(ident)))
#link between sell_buy and inventory to show the things
def inventory_entry(data):
    ent = []
    for ident in item_ids_in_bag(data["items"]):
        ent.append(("items",ident))
    for ident in unique(data["bag"]):
        ent.append(("gear",ident))
    return ent
#connection between player and store&inventory page
#select stuff
def move_cursor(k,cur,count):
    if count == 0:
        return cur
    if k =="UP":
        return(cur-1)&count
    if k =="DOWN":
        return(cur+1)&count
    return cur
#run the shops and inventory
def shop_screen(number):
    stock = stock_for_shop(number)
    tab, cur, notice = 0,0,""
    while True:
        a = sell_buy(stock,tab)
        cur = min(cur,max(0,len(a)-1))
        draw_s(number,tab,cur,notice)
        notice = ""
        key = get_key()
        if key in ("ESE","e"):
            flush_keys()
            return
        if key and len(key)==1 and key in "1234567890" and int(key)<=len(a):
            cur = int(key-1)
        elif key in ("LEFT","RIGHT"):
            tab,cur = 1-tab,0
        elif key =="ENTER" and a:
            ident = a[cur][0]
            if tab == 0:
                notice = buy(ident)
            else:
                notice = sell(ident)
        elif key =="h":
            return help_screen()
        else:
            cur = move_cursor(k,cur,len(a))
def inventory_screen():
    data = g["player"]
    cur, notice = 0,""
    while True:
        ent = inventory_entry(data)
        cur = min(cur,max(0,len(ent)-1))
        draw_inventory(data,ent,cur,notice)
        notice = ""
        key = get_key()
        if key in ("ESE","e"):
            flush_keys()
            return
        elif key =="ENTER" and ent:
            kind, ident = ent[cur]
            notice = use_entry(data,kind,ident)
        elif key == "h":
            return help_screen()
        else:
            cur = move_cursor(k,cur,len(ent))

#labels and selection indicators
#label for shop
def s_row_text(data,i,ident,tab):
    label = f"{i+1}."
    if ident in items:
        count = data["items"].get(ident,0)
        return label+f"{items[ident]['name']}   ( {count})"
    info = gear[ident]
    label += f"{info['name']}  (+{info['bonus']} {gear_stat_name(info)})"
    if tab == 0 and not is_upgrade(data,ident):
        label += "not upgraded"
    if tab == 1 :
        label += f" x{data["bag"].count(ident)}"
    return label
# label for inventory
def in_entry_txt(data,kind,ident):
    if kind =="item":
        return f"{items[ident]['name']} x {data['items'][ident]} - {item_summary(items[ident])}"
    else:
        l = gear_label(ident,data)
        if is_upgrade(data,ident):
            l += "upgraded!"
        return l
# join owned gear to sth easy to read
def bag_names(data):
    name = []
    for ident in data["bag"]:
        name.append(gear[ident]["name"])
    if not name:
        return "empty"
    else:
        return ",".join(name)
#tell player where the position of selection is
def arrow(label,selected):
    if selected:
        return ">" + label
    else:
        return " " + label

#draw the shop and inventory
#drow the row
def draw_s_row(data,i,price,ident,tab,cur):
    attr = col("red", bold = True, rev=(i ==cur))
    text = arrow(s_row_text(data,i,ident,tab), i == cur)
    y = 5+i - max(0,cur - 8)
    put(y,4,f"{text:<50}",attr)
    put(y,58,f"{price:>4}$",attr)
#detail of the product in the shop
def draw_s_detail(data,ident,tab):
    if ident in items:
        put(15,4,item_summary(items[ident]),col("purple"))
        return
    if tab == 1:
        return
    info = gear[ident]
    bonus = gear_label(data(slot_of(ident)))
    text = f"{info['name']}: {gear_stat_name(info)}  (+{bonus})->(+{info['bonus']})"
    put(15,4,text,col("yellow"))
#header of shop can character property
def draw_s_header(number,tab,data):
    title = f"SHOP #{number+1}"
    center(0,title,col("green",bold = True))
    put(1,2,f"Gold:{data['gold']}",col("yellow",bold = True))
    text = f"HP: {data['hp']}/{data['max_hp']}   MP: {data['mp']}/{data['max_mp']}"
    put(1,20,text + f"ATK{atk_text(data)}   DEF{def_text(data)}")
    buy_label, sell_label = "BUY", "SELL"
    if tab == 0:
        buy_label = "[BUY]"
    else:
        sell_label = "[SELL]"
        put(3,4,buy_label,col("blue",bold = True,rev = (tab ==0)))
        put(3,11,sell_label,col("blue",bold = True,rev = (tab ==1)))
        put(3,20,"LEFT/RIGHT TO SWITCH",col(dim = True))
        hline(4)
#draw rest info
def draw_s_footer(data,notice):
    put(17,2,f"Weapon{gear_label(data['weapon'])}",col(dim = True))
    put(18,2,f"Armor{gear_label(data['armor'])}",col(dim = True))
    put(19,2,f"Bag     :{bag_names(data)}"[:76],col(dim = True))
    if notice:
        put(21,2,notice,col("lilac"),bold = True)
    hint = "UP/DOWN/1-9 select  ENTER buy/sell LEFT/RIGHT tab ESC leave H:help"
    put(23,2,hint,col("pink"))
#combine all component shop screen together
def draw_s(number,tab,rows,cur,notice):
    data = g["player"]
    clear_screen()
    draw_s_header(number,tab,data)
    if not rows:
        message = "nothing to sell"
        if tab == 0:
            message = "not enough stock"
        put(6,4,message,col(dim = True))
    top = max(0,cur - 8)
    for i in range(top,min(len(rows),top+9)):
        ident,price = rows[i]
        draw_s_row(data,i,price,ident,tab,cur)
    hline(14)
    if rows:
        draw_s_detail(data,rows[cur][0],tab)
    if len(rows) > 9:
        put(16,4,f"Rows {top+1}-{min(len(rows),top+9)} of {len(rows)}; arrow scroll.")
    draw_s_footer(data,notice)
    show()

#basic infor in inventory , like items/gear/property and etc
def draw_inv_stats(data):
    put(2,2,f"{data['name']} ({data['role']})",col(hero_colors[data["key"]],bold = True))
    text = f"hp: {data['hp']}/{data['max_hp']}     mp: {data['mp']}/{data['max_mp']}"
    put(3,2,text + f"Gold:{data['gold']}       SPD{data['spd']}")
    put(4,2, f"ATK:{atk_text[data]}       DEF{def_text[data]}")
    put(5,2, f"Weapon{gear_label(data['weapon'])}")
    put(6,2,f"Armor{gear_label(data['armor'])}")
    put(7,2,f"Bag{bag_names(data)}"[:74])
    put(8,2,f"Moves:",col("blue",bold = True))
    for i,move in enumerate(data["moves"]):
        summary = move_summary(move,atk_total(data),def_total(data))
        put(9+i,4,f"{move['name']:<15}{move_cost(move):>5}    {summary}"[:74])
#the structure of inventory display
def draw_inv(data,entries,cur,notice):
    clear_screen()
    center(0,"INVENTORY",col("green",bold = True))
    draw_inv_stats(data)
    put(14,2,"Bag (Entre to use/equip):",col("brown",bold = True))
    if not entries:
        put(15,4,"Your bag is empty ",col(dim = True))
    top = max(0,cur - 6)
    for i in range(top,min(len(entries),top+7)):
        kind , ident = entries[i]
        text = in_entry_txt(data,kind,ident)[:70]
        attr = col("yellow",bold = True,rev = (i==cur))
        put(15+i-top,4,arrow(text,i==cur),attr)
    if notice:
        put(22,2,notice,col("lilac"),bold = True)
        put(23,2,"UP/DOWN: select    Enter: use/equip ESC or I: close   h:help",col("cyan"))
        show()