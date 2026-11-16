from tkinter import *
from tkinter import ttk,messagebox
from random import randint,shuffle, choice
import sqlite3
from datetime import datetime, timedelta
import tabulate
import time

#Глобальные переменные
pika = "♠"
kresta = "♣"
bubna = "♦"
chirva = "♥"
masti = ["♠","♣","♦","♥"]
koloda = []
player1 = []
player2 = []
attack = [False,False]
hodplayer = [False,False]
otboy = []
round_attack = []
round_defender = []
background_color = "white"
koloda2 = []
ind = False
name1 =""
name2 = ""
shrift = "Fixedsys"
text_color = "Black"
win = False
score = 0
ident = ""
langue = "ru"

# Функция для изменения цвета при наведении курсора
def on_enter(event):
    canvas.itemconfig(event.widget.find_withtag("current"), fill="#D3D3D3")
def on_leave(event):
    canvas.itemconfig(event.widget.find_withtag("current"), fill="white")
#Сравниваем карты
def comparison_cart(cart1,cart2,koz):
    # Возвращает True если карта бьет
    a = False
    if cart2[1] == cart1[1]:
        if cart2[0] > cart1[0]:
            a = True
    else:
        if cart2[1] == koz[1]:
            a = True
    return a
#Рисуем карты
def draw_all_carts():
    global player1, player2, round_attack, round_defender
    masht = 1
    width = canvas.winfo_width()  # Ширина экрана
    player = hod_player()

    # Рассчитываем количество карт, которые помещаются на экране
    card_width = 190  # Ширина карты (учитываем масштаб)
    max_cards_per_row = int((width - 10) / (card_width * masht))  # Отступы по краям

    if len(player) > max_cards_per_row:
        masht = (width - 10) / (card_width * len(player))  # Динамически уменьшаем масштаб

    canvas.delete("all")
    x = 10
    y = 10
    for card in player:
        if x > (width - 100):  # Если карты выходят за границы экрана
            x = 10
            y += 150  # Переход на следующую строку
        draw_cart(card[0], card[1], x, y, masht)
        x += 190 * masht

    if len(koloda) > 0:
        draw_cart(koloda[len(koloda) - 1][0], koloda[len(koloda) - 1][1], 10, 510, 1)
        if background_color == "black":
            canvas.create_rectangle(10, 400, 170, 500, fill="gray")
        else:
            canvas.create_rectangle(10, 400, 170, 500, fill="black")
        canvas.create_text(90, 450, text=len(koloda), font=("Arial 35"), fill="white")

    x = 300
    y = 300
    for card in round_attack:
        draw_cart(card[0], card[1], x, y, 1)
        x += 190
    x = 300
    for card in round_defender:
        draw_cart(card[0], card[1], x + 10, y + 130, 1)
        x += 190
def draw_cart(n, m, x, y, k):
    # Размеры карты
    width = 160 * k
    height = 210 * k

    # Рисуем прямоугольник карты
    rect_id = canvas.create_rectangle(x, y, x + width, y + height, activefill="#D3D3D3", fill="white")
    canvas.tag_bind(rect_id, "<Enter>", on_enter)
    canvas.tag_bind(rect_id, "<Leave>", on_leave)

    # Преобразуем значения картинок в буквы для картинок "J", "Q", "K", "A"
    if n == 11:
        n = "J"
    elif n == 12:
        n = "Q"
    elif n == 13:
        n = "K"
    elif n == 14:
        n = "A"

    # Цвет текста зависит от масти
    color = "red" if m in [bubna, chirva] else "black"

    # Отрисовка текста с учетом масштаба
    canvas.create_text(
        x + 10 * k,
        y + 10 * k,
        text=str(n),
        font=("Arial", int(10 * k)),  # Шрифт изменяется пропорционально k
        fill=color
    )
    canvas.create_text(
        x + width // 2,
        y + height // 2,
        text=m,
        font=("Arial", int(35 * k)),  # Центральный шрифт также изменяется
        fill=color
    )
    canvas.create_text(
        x + width - 10 * k,
        y + height - 10 * k,
        text=str(n),
        font=("Arial", int(10 * k)),  # Нижний угол карты
        fill=color
    )
#Управление окном
def dismiss(window):
    window.grab_release()
    window.destroy()
def center_child(Win, parent):
    Win.update_idletasks()  # Обновление размеров окна
    parent.update_idletasks()
    parent_width = parent.winfo_width()
    parent_height = parent.winfo_height()
    parent_x = parent.winfo_x()
    parent_y = parent.winfo_y()

    child_width = Win.winfo_width()
    child_height = Win.winfo_height()

    x = parent_x + parent_width // 2 - child_width // 2
    y = parent_y + parent_height // 2 - child_height // 2

    Win.geometry(f'{child_width}x{child_height}+{x}+{y}')
#Просмотр выбранных карт
def show_selected_cards(hod,selected_card):
    def proverka():
        if round_attack:
            if show_attack_player() == hod_player():
                flag = False
                for card in round_attack:
                    if player[selected_card][0] == card[0]:
                        flag = True
                        break
                if not flag:
                    for card in round_defender:
                        if player[selected_card][0] == card[0]:
                            flag = True
                            break
                return flag
            else:
                return True
        else:
            return True
    def proverka2():
        if hod_player() != show_attack_player():
            if round_attack:
                return comparison_cart(round_attack[len(round_attack) - 1], player[selected_card],koloda2[len(koloda2)-1])
            else:
                return True
        else:
            return True
    global otboy_round,round_attack,hodplayer
    change_hod()
    player = hod_player()

    if proverka():
        if proverka2():
            if (attack[0] and hodplayer[0]) or (attack[1] and hodplayer[1]):
                round_attack.append(player[selected_card])
            else:
                round_defender.append(player[selected_card])
            player.remove(player[selected_card])
            change_hod()
            dismiss(hod)
            if finish():
                finish1()
            else:
                draw_all_carts()
                choice_card()
        else:
            if langue == "ru":
                messagebox.showerror("Ошибка", "Вы не можете побить этой картой")
            elif langue == "ua":
                messagebox.showerror("Помилка", "Ви не можете побити цією картою")
            elif langue == "eng":
                messagebox.showerror("Error", "You can't beat with this card.")
            elif langue == "fr":
                messagebox.showerror("Error", "Vous ne pouvez pas battre avec cette carte")


            choice_card()
    else:
        if langue == "ru":
            messagebox.showerror("Ошибка", f"{player[selected_card]} не может быть подкинута")
        elif langue == "eng":
            messagebox.showerror("Error", f"{player[selected_card]} can't be tossed")
        elif langue == "ua":
            messagebox.showerror("Помилка", f"{player[selected_card]} не може бути підкинута")
        elif langue == "fr":
            messagebox.showerror("Error", f"{player[selected_card]} ne peut pas être jeté")

        choice_card()
#Меняем ход
def show_attack_player():
    global player1,player2,attack

    if attack[0]:
       return player1
    else:
        return player2
def change_hod():
    global hodplayer
    if hodplayer[1]:
        hodplayer[0] = True
        hodplayer[1] = False
    else:
        hodplayer[0] = False
        hodplayer[1] = True
def change_player(player):
    global hodplayer
    if player == player1:
        hodplayer[0] = False
        hodplayer[1] = True
        return player2
    else:
        hodplayer[0] = True
        hodplayer[1] = False
        return player1
def hod_player():
    global hodplayer
    if hodplayer[0]:
        return player1
    else:
        return player2
def otboy_(hod):
    global round_attack, round_defender, otboy, player1, player2, koloda,attack,hodplayer
    dismiss(hod)
    for card in round_attack:
        otboy.append(card)
    for card in round_defender:
        otboy.append(card)
    round_attack.clear()
    round_defender.clear()

    # Проверяем, хватает ли карт в колоде для раздачи
    while len(player1) < 6 and len(koloda) > 0:
        player1.append(koloda[0])
        koloda.remove(koloda[0])

    while len(player2) < 6 and len(koloda) > 0:  # Исправлено на player2
        player2.append(koloda[0])  # Исправляем на player2
        koloda.remove(koloda[0])
    change_attack()
    draw_all_carts()
    choice_card()
def vzyat(hod):
    dismiss(hod)
    global round_attack,round_defender,otboy,hodplayer,attack
    player = show_attack_player()
    player = change_player(player)
    for card in round_attack:
        player.append(card)
    for card in round_defender:
        player.append(card)
    if len(player1) < 6:
        # Проверяем, хватает ли карт в колоде для раздачи
        while len(player1) < 6 and len(koloda) > 0:
            player1.append(koloda[0])
            koloda.remove(koloda[0])
    if len(player2) < 6:
        while len(player2) < 6 and len(koloda) > 0:  # Исправлено на player2
            player2.append(koloda[0])  # Исправляем на player2
            koloda.remove(koloda[0])
    canvas.delete("all")
    round_attack.clear()
    round_defender.clear()
    change_hod()
    draw_all_carts()
    choice_card()
def prom(player,selected_card,batl):
    global round_attack,round_defender,koloda,player1,player2
    vibor = player[selected_card]
    if comparison_cart(round_attack[len(round_attack)-1], vibor, koloda2[len(koloda2)-1]):
        #messagebox.showinfo("Игра в дурака", "Карта побита")
        player.remove(vibor)
        round_defender.append(vibor)
        dismiss(batl)
        canvas.delete("all")
        draw_all_carts()
    else:
        if langue == "ru":
            messagebox.showerror("Ошибка", "Эта карта не может побить!")
        elif langue == "eng":
            messagebox.showerror("Error", "This card can't be beat!")
        elif langue == "ua":
            messagebox.showerror("Помилка", "Ця карта не може бити!")
        elif langue == "fr":
            messagebox.showerror("Error", "Cette carte ne peut pas toucher !")
        choice_card()
def change_attack():
    global attack
    if attack[0]:
        attack[0] = False
        attack[1] = True
    else:
        attack[0] = True
        attack[1] = False
def choice_card():
    global hodplayern,langue
    player = hod_player()
    if player == player1:
        hodplayer[0] = False
        hodplayer[1] = True
    else:
        hodplayer[0] = True
        hodplayer[1] = False
    if win:
        pass
    else:
        if langue == "ru":
            if player == player1:
                canvas.create_text(100, 300, text=f"Играет {name1}", tags="player", font=(shrift, 20), fill=text_color)
            else:
                canvas.create_text(100, 300, text=f"Играет {name2}", tags="player", font=(shrift, 20), fill=text_color)
        if langue == "eng":
            if player == player1:
                canvas.create_text(100, 300, text=f"Played {name1}", tags="player", font=(shrift, 20), fill=text_color)
            else:
                canvas.create_text(100, 300, text=f"Played {name2}", tags="player", font=(shrift, 20), fill=text_color)
        if langue == "ua":
            if player == player1:
                canvas.create_text(100, 300, text=f"Грає {name1}", tags="player", font=(shrift, 20), fill=text_color)
            else:
                canvas.create_text(100, 300, text=f"Грає {name2}", tags="player", font=(shrift, 20), fill=text_color)
        if langue == "fr":
            if player == player1:
                canvas.create_text(100, 300, text=f"Joue {name1}", tags="player", font=(shrift, 20), fill=text_color)
            else:
                canvas.create_text(100, 300, text=f"Joue {name2}", tags="player", font=(shrift, 20), fill=text_color)
        hod = Toplevel(Win)
        hod.geometry("300x300")
        hod.resizable(False, True)
        center_child(hod, Win)
        hod.protocol("WM_DELETE_WINDOW", lambda: None)
        if langue == "ru":
            lbl = Label(hod, text="Выберите карту для хода: ")
            lbl.pack()
        elif langue == "ua":
            lbl = Label(hod, text="Виберіть картку для ходу: ")
            lbl.pack()
        elif langue == "eng":
            lbl = Label(hod, text="Select a card to play: ")
            lbl.pack()
        elif langue == "fr":
            lbl = Label(hod, text="Sélectionnez une carte à jouer: ")
            lbl.pack()

        # Создаем переменную для хранения выбора
        selected_card = IntVar(value=0)  # Начальное значение

        # Создаем радиокнопки
        for i, card in enumerate(player):
            # Определяем текст для карты
            if card[0] == 11:
                text = "J" + str(card[1])
            elif card[0] == 12:
                text = "Q" + str(card[1])
            elif card[0] == 13:
                text = "K" + str(card[1])
            elif card[0] == 14:
                text = "A" + str(card[1])
            else:
                text = str(card[0]) + str(card[1])

            # Радиокнопка с привязкой переменной
            ttk.Radiobutton(hod, text=text, value=i, variable=selected_card).pack()
        btn = ttk.Button(hod, text="Ok", command=lambda: show_selected_cards(hod, selected_card.get()))
        btn.pack()
        if langue == "ru":
            if (hodplayer[0] and attack[0]) or (hodplayer[1] and attack[1]):
                btn1 = ttk.Button(hod, text="Взять", command=lambda: vzyat(hod))
                btn1.pack()
            else:
                btn1 = ttk.Button(hod, text="Отбой", command=lambda: otboy_(hod))
                btn1.pack()
        if langue == "ua":
            if (hodplayer[0] and attack[0]) or (hodplayer[1] and attack[1]):
                btn1 = ttk.Button(hod, text="Взяти", command=lambda: vzyat(hod))
                btn1.pack()
            else:
                btn1 = ttk.Button(hod, text="Відбій", command=lambda: otboy_(hod))
                btn1.pack()
        if langue == "eng":
            if (hodplayer[0] and attack[0]) or (hodplayer[1] and attack[1]):
                btn1 = ttk.Button(hod, text="Take it", command=lambda: vzyat(hod))
                btn1.pack()
            else:
                btn1 = ttk.Button(hod, text="Finish the round", command=lambda: otboy_(hod))
                btn1.pack()
        if langue == "fr":
            if (hodplayer[0] and attack[0]) or (hodplayer[1] and attack[1]):
                btn1 = ttk.Button(hod, text="Prends-le", command=lambda: vzyat(hod))
                btn1.pack()
            else:
                btn1 = ttk.Button(hod, text="Terminer le tour", command=lambda: otboy_(hod))
                btn1.pack()
        hod.grab_set()  # Захватываем пользовательский ввод
def pr():
    canvas.delete("welcome_text")
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    if langue == "ru":
        message = "Приветствуем вас в нашей игре"
    elif langue == "eng":
        message = "Welcome to our game"
    elif langue == "ua":
        message = "Вітаємо у нашій грі"
    else:
        message = "Bienvenue dans notre jeu"

    canvas.create_text(
        canvas_width // 2,
        canvas_height // 2 - 80,
        text=message,
        font=(shrift, 55),
        tags="welcome_text",
        fill=text_color,
        anchor='center'
    )
def start_game():
    def start(pole,pole1):
        global ind,player1,player2,name1,name2,attack
        ind = True
        canvas.delete("welcome_text")

        pl.destroy()
        global koloda,player1,player2,koloda2

        # Формируем колоду
        for i in range(4):
            for j in range(6, 15):
                koloda.append((j, masti[i]))

        # Перемешиваем колоду
        shuffle(koloda)
        koloda2 = koloda.copy()
        koz1 = []
        koz2 = []
        for k in range(6):
            player1.append(koloda[0])
            if koloda[0][1] == koloda[len(koloda)-1][1]:
                koz1.append(koloda[0])
            koloda.remove(koloda[0])
            player2.append(koloda[0])
            if koloda[0][1] == koloda[len(koloda)-1][1]:
                koz2.append(koloda[0])
            koloda.remove(koloda[0])
        if len(koz1) > 0:
            koz1.sort(key=lambda x: x[0])
        if len(koz2) > 0:
            koz2.sort(key=lambda x: x[0])

        if len(koz1) > 0 and len(koz2) > 0:
            if koz1[0] < koz2[0]:
                attack[0] = True
                attack[1] = False
            else:
                attack[0] = False
                attack[1] = True
        elif len(koz1) == 0 and len(koz2) == 0:
            player1.sort(key=lambda x: x[0])
            player2.sort(key=lambda x: x[0])
            if player1[0][0] != player2[0][0]:
                if player1[0][0] < player2[0][0]:
                    attack[0] = True
                    attack[1] = False
                else:
                    attack[0] = False
                    attack[1] = True
            else:
                if player1[1][0] < player2[1][0]:
                    attack[0] = True
                    attack[1] = False
                else:
                    attack[0] = False
                    attack[1] = True
        elif len(koz1) == 0:
            attack[0] = False
            attack[1] = True
        else:
            attack[0] = True
            attack[1] = False
        if attack[0]:
            hodplayer[0] = True
            hodplayer[1] = False
        else:
            hodplayer[0] = False
            hodplayer[1] = True
        name1 = pole
        name2 = pole1
        draw_all_carts()
        choice_card()

    pl = Toplevel(Win)
    pl.geometry("300x200")
    pl.resizable(False,False)
    center_child(pl, Win)
    pl.protocol("WM_DELETE_WINDOW",
                              lambda: dismiss(pl))  # Перехватываем нажатие на крестик
    global langue
    if langue == "ru":
        lbl = Label(pl, text="Введите имя 1 игрока")
        lbl.pack()
        pole = ttk.Entry(pl)
        pole.pack()
        lbl1 = Label(pl, text="Введите имя 2 игрока")
        lbl1.pack()
        pole1 = ttk.Entry(pl)
        pole1.pack()
        btn = ttk.Button(pl, text="Ok", command=lambda: start(pole.get(), pole1.get()))
        btn.pack()
        pl.grab_set()  # Захватываем пользовательский ввод
    if langue == "eng":
        lbl = Label(pl, text="Enter the name of player 1")
        lbl.pack()
        pole = ttk.Entry(pl)
        pole.pack()
        lbl1 = Label(pl, text="Enter the name of player 2")
        lbl1.pack()
        pole1 = ttk.Entry(pl)
        pole1.pack()
        btn = ttk.Button(pl, text="Ok", command=lambda: start(pole.get(), pole1.get()))
        btn.pack()
        pl.grab_set()  # Захватываем пользовательский ввод
    if langue == "ua":
        lbl = Label(pl, text="Введіть ім'я 1 гравця")
        lbl.pack()
        pole = ttk.Entry(pl)
        pole.pack()
        lbl1 = Label(pl, text="Введіть ім'я 2 гравця")
        lbl1.pack()
        pole1 = ttk.Entry(pl)
        pole1.pack()
        btn = ttk.Button(pl, text="Ok", command=lambda: start(pole.get(), pole1.get()))
        btn.pack()
        pl.grab_set()  # Захватываем пользовательский ввод
    if langue == "fr":
        lbl = Label(pl, text="Entrez le nom du 1er joueur")
        lbl.pack()
        pole = ttk.Entry(pl)
        pole.pack()
        lbl1 = Label(pl, text="Entrez le nom du 2eme joueur")
        lbl1.pack()
        pole1 = ttk.Entry(pl)
        pole1.pack()
        btn = ttk.Button(pl, text="Ok", command=lambda: start(pole.get(), pole1.get()))
        btn.pack()
        pl.grab_set()  # Захватываем пользовательский ввод
def parametrs():
    global background_color, shrift, text_color
    def close():
        dismiss(parametrs_window)
    def prim():
        parametrs_window.destroy()
        global background_color,shrift,text_color,langue
        # Обновляем цвет фона на основе выбранной радиокнопки
        if color_var.get() == "white":
            background_color = "white"
        elif color_var.get() == "black":
            background_color = "black"
        elif color_var.get() == "green":
            background_color = "#008000"
        elif color_var.get() == "lime":
            background_color = "#00FF00"
        elif color_var.get() == "darkgreen":
            background_color = "#006400"
        elif color_var.get() == "blue":
            background_color = "#0000FF"
        elif color_var.get() == "goluboy":
            background_color = "#00FFFF"
        elif color_var.get() == "orange":
            background_color = "#FF8C00"
        elif color_var.get() == "pink":
            background_color = "#FF1493"
        elif color_var.get() == "gold":
            background_color = "#DAA520"
        elif color_var.get() == "violet":
            background_color = "#800080"
        elif color_var.get() == "darkred":
            background_color = "#8B0000"
        elif color_var.get() == "khaki":
            background_color = "#F0E68C"
        elif color_var.get() == "olive":
            background_color = "#808000"
        elif color_var.get() == "darkolive":
            background_color = "#556B2F"
        elif color_var.get() == "chocolate":
            background_color = "#D2691E"
        elif color_var.get() == "brown":
            background_color = "#800000"
        elif color_var.get() == "aquamarine":
            background_color = "#7FFFD4"
        elif color_var.get() == "indigo":
            background_color = "#4B0082"
        elif color_var.get() == "skay":
            background_color = "#87CEEB"
        elif color_var.get() == "tomat":
            background_color = "#FF6347"
        elif color_var.get() == "coral":
            background_color = "#FF7F50"
        elif color_var.get() == "lightcoral":
            background_color = "#F08080"
        elif color_var.get() == "indian":
            background_color = "#CD5C5C"
        elif color_var.get() == "azur":
            background_color = "#F0FFFF"
        elif color_var.get() == "snow":
            background_color = "#FFFAFA"
        elif color_var.get() == "salmon":
            background_color = "#FA8072"
        elif color_var.get() == "lavan":
            background_color = "#E6E6FA"
        elif color_var.get() == "medo":
            background_color = "#F0FFF0"
        elif color_var.get() == "bordov":
            background_color = "#32CD32"
        else:
            background_color = "gray"

        if shrift_var.get() == "1":
            shrift = "Arial"
        elif shrift_var.get() == "2":
            shrift = "Georgia"
        elif shrift_var.get() == "3":
            shrift="Comic Sans MS"
        elif shrift_var.get() == "4":
            shrift="Courier New"
        elif shrift_var.get() == "5":
            shrift="Times New Roman"
        elif shrift_var.get() == "6":
            shrift="Fixedsys"
        elif shrift_var.get() == "7":
            shrift="Verdana Pro Black"
        elif shrift_var.get() == "8":
            shrift = "Montserrat Black"
        else:
            shrift = "Impact"
        if text_var.get() == "1":
            text_color = "Black"
        elif text_var.get() == "2":
            text_color = "White"
        elif text_var.get() == "3":
            text_color = "Red"
        elif text_var.get() == "4":
            text_color = "Yellow"
        elif text_var.get() == "5":
            text_color = "Orange"
        elif text_var.get() == "6":
            text_color = "Blue"
        elif text_var.get() == "7":
            text_color = "#00BFFF"
        elif text_var.get() == "8":
            text_color = "#FF00FF"
        elif text_var.get() == "10":
            text_color = "#4B0082"
        elif text_var.get() == "11":
            text_color = "#800000"
        elif text_var.get() == "12":
            text_color = "#DAA520"
        elif text_var.get() == "13":
            text_color = "#808000"
        elif text_var.get() == "14":
            text_color = "#00FF00"
        elif text_var.get() == "15":
            text_color = "#8B0000"
        elif text_var.get() == "16":
            text_color = "#7FFFD4"
        elif text_var.get() == "17":
            text_color = "#87CEEB"
        elif text_var.get() == "18":
            text_color = "#9ACD32"
        else:
            text_color = "#800080"
        if lang_var.get() == "ru":
            langue = "ru"
        elif lang_var.get() == "eng":
            langue = "eng"
        if lang_var.get() == "ua":
            langue = "ua"
        elif lang_var.get() == "fr":
            langue = "fr"
        # Обновляем цвет фона Canvas
        canvas.config(bg=background_color)
        update_menu(langue)
        Win.update_idletasks()
        pr()
    # Окно параметров
    parametrs_window = Toplevel(Win)
    parametrs_window.geometry("720x370")
    parametrs_window.resizable(False,False)
    center_child(parametrs_window, Win)
    parametrs_window.protocol("WM_DELETE_WINDOW", lambda: dismiss(parametrs_window))  # Перехватываем нажатие на крестик

    if langue == "ru":
        backgroundfrm = LabelFrame(parametrs_window, text="Цвет фона", cursor="target")
        backgroundfrm.grid(row=0, column=0)
        color_var = StringVar(
            value=background_color)  # Устанавливаем начальное значение переменной равным текущему цвету

        # Создаем радиокнопки для выбора цвета
        wh = ttk.Radiobutton(backgroundfrm, text="Белый", variable=color_var, value="white")
        wh.grid(row=1, column=0, sticky=W)

        bl = ttk.Radiobutton(backgroundfrm, text="Черный", variable=color_var, value="black")
        bl.grid(row=2, column=0, sticky=W)

        gr = ttk.Radiobutton(backgroundfrm, text="Зеленый", variable=color_var, value="green")
        gr.grid(row=3, column=0, sticky=W)

        bl = ttk.Radiobutton(backgroundfrm, text="Лаймовый", variable=color_var, value="lime")
        bl.grid(row=4, column=0, sticky=W)

        gr = ttk.Radiobutton(backgroundfrm, text="Темно-зеленый", variable=color_var, value="darkgreen")
        gr.grid(row=5, column=0, sticky=W)

        blu = ttk.Radiobutton(backgroundfrm, text="Синий", variable=color_var, value="blue")
        blu.grid(row=6, column=0, sticky=W)

        gl = ttk.Radiobutton(backgroundfrm, text="Голубой", variable=color_var, value="goluboy")
        gl.grid(row=7, column=0, sticky=W)

        gra = ttk.Radiobutton(backgroundfrm, text="Серый", variable=color_var, value="gray")
        gra.grid(row=8, column=0, sticky=W)
        ora = ttk.Radiobutton(backgroundfrm, text="Оранжевый", variable=color_var, value="orange")
        ora.grid(row=9, column=0, sticky=W)
        ora = ttk.Radiobutton(backgroundfrm, text="Зеленый лайм", variable=color_var, value="bordov")
        ora.grid(row=10, column=0, sticky=W)
        pin = ttk.Radiobutton(backgroundfrm, text="Розовый", variable=color_var, value="pink")
        pin.grid(row=1, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text="Фиолетовый", variable=color_var, value="violet")
        viol.grid(row=2, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Золотой", variable=color_var, value="gold")
        gol.grid(row=3, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text="Темно-красный", variable=color_var, value="darkred")
        viol.grid(row=4, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Хаки", variable=color_var, value="khaki")
        gol.grid(row=5, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text="Оливковый", variable=color_var, value="olive")
        viol.grid(row=6, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Темно-оливковый", variable=color_var, value="darkolive")
        gol.grid(row=7, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Шоколадный", variable=color_var, value="chocolate")
        gol.grid(row=8, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Коричневый", variable=color_var, value="brown")
        gol.grid(row=9, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Медовая роса", variable=color_var, value="medo")
        gol.grid(row=10, column=1, sticky=W)
        ar = ttk.Radiobutton(backgroundfrm, text="Индиго", variable=color_var, value="indigo")
        ar.grid(row=1, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Аквамариновый", variable=color_var, value="aquamarine")
        fyx.grid(row=2, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Томатный", variable=color_var, value="tomat")
        fyx.grid(row=3, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Кораловый", variable=color_var, value="coral")
        fyx.grid(row=4, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Светло-кораловый", variable=color_var, value="lightcoral")
        fyx.grid(row=5, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Индийский красный", variable=color_var, value="indian")
        fyx.grid(row=6, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Азурный", variable=color_var, value="azur")
        fyx.grid(row=7, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Снежный", variable=color_var, value="snow")
        fyx.grid(row=8, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Лосось", variable=color_var, value="salmon")
        fyx.grid(row=9, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Лавандовый", variable=color_var, value="lavan")
        fyx.grid(row=10, column=2, sticky=W)
        textfrm = LabelFrame(parametrs_window, text="Цвет текста", cursor="target")
        textfrm.grid(row=0, column=3)

        text_var = StringVar(value=shrift)

        ar = ttk.Radiobutton(textfrm, text="Черный", variable=text_var, value="1")
        ar.grid(row=0, column=3, sticky=W)

        geo = ttk.Radiobutton(textfrm, text="Белый", variable=text_var, value="2")
        geo.grid(row=1, column=3, sticky=W)

        comic = ttk.Radiobutton(textfrm, text="Красный", variable=text_var, value="3")
        comic.grid(row=2, column=3, sticky=W)

        courier = ttk.Radiobutton(textfrm, text="Желтый", variable=text_var, value="4")
        courier.grid(row=3, column=3, sticky=W)
        timess = ttk.Radiobutton(textfrm, text="Оранжевый", variable=text_var, value="5")
        timess.grid(row=4, column=3, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text="Синий", variable=text_var, value="6")
        fyx.grid(row=5, column=3, sticky=W)

        courier = ttk.Radiobutton(textfrm, text="Голубой", variable=text_var, value="7")
        courier.grid(row=6, column=3, sticky=W)
        timess = ttk.Radiobutton(textfrm, text="Розовый", variable=text_var, value="8")
        timess.grid(row=7, column=3, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text="Фиолетовый", variable=text_var, value="9")
        fyx.grid(row=8, column=3, sticky=W)
        ar = ttk.Radiobutton(textfrm, text="Индиго", variable=text_var, value="10")
        ar.grid(row=0, column=4, sticky=W)

        geo = ttk.Radiobutton(textfrm, text="Коричневый", variable=text_var, value="11")
        geo.grid(row=1, column=4, sticky=W)

        comic = ttk.Radiobutton(textfrm, text="Золотой", variable=text_var, value="12")
        comic.grid(row=2, column=4, sticky=W)

        courier = ttk.Radiobutton(textfrm, text="Оливковый", variable=text_var, value="13")
        courier.grid(row=3, column=4, sticky=W)
        timess = ttk.Radiobutton(textfrm, text="Лаймовый", variable=text_var, value="14")
        timess.grid(row=4, column=4, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text="Темнокрасный", variable=text_var, value="15")
        fyx.grid(row=5, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text="Аквамариновый", variable=text_var, value="16")
        fyx.grid(row=6, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text="Небесный", variable=text_var, value="17")
        fyx.grid(row=7, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text="Жёлто-зеленый", variable=text_var, value="18")
        fyx.grid(row=8, column=4, sticky=W)
        shriftfrm = LabelFrame(parametrs_window, text="Шрифт", cursor="target")
        shriftfrm.grid(row=0, column=4)
        shrift_var = StringVar(value=shrift)

        ar = ttk.Radiobutton(shriftfrm, text="Arial", variable=shrift_var, value="1")
        ar.grid(row=0, column=4, sticky=W)

        geo = ttk.Radiobutton(shriftfrm, text="Georgia", variable=shrift_var, value="2")
        geo.grid(row=1, column=4, sticky=W)

        comic = ttk.Radiobutton(shriftfrm, text="Comic Sans MS", variable=shrift_var, value="3")
        comic.grid(row=2, column=4, sticky=W)

        courier = ttk.Radiobutton(shriftfrm, text="Courier New", variable=shrift_var, value="4")
        courier.grid(row=3, column=4, sticky=W)
        timess = ttk.Radiobutton(shriftfrm, text="Times New Roman", variable=shrift_var, value="5")
        timess.grid(row=4, column=4, sticky=W)

        fyx = ttk.Radiobutton(shriftfrm, text="Fixedsys", variable=shrift_var, value="6")
        fyx.grid(row=5, column=4, sticky=W)

        ar = ttk.Radiobutton(shriftfrm, text="Verdana Pro Black", variable=shrift_var, value="7")
        ar.grid(row=6, column=4, sticky=W)

        geo = ttk.Radiobutton(shriftfrm, text="Montserrat Black", variable=shrift_var, value="8")
        geo.grid(row=7, column=4, sticky=W)

        comic = ttk.Radiobutton(shriftfrm, text="Impact", variable=shrift_var, value="9")
        comic.grid(row=8, column=4, sticky=W)
        langfrm = LabelFrame(parametrs_window, text="Язык", cursor="target")
        langfrm.grid(row=1, column=0)
        lang_var = StringVar(value=shrift)

        ar = ttk.Radiobutton(langfrm, text="Русский", variable=lang_var, value="ru")
        ar.grid(row=0, column=0, sticky=W)

        geo = ttk.Radiobutton(langfrm, text="Английский", variable=lang_var, value="eng")
        geo.grid(row=0, column=1, sticky=W)
        ar = ttk.Radiobutton(langfrm, text="Украинский", variable=lang_var, value="ua")
        ar.grid(row=0, column=2, sticky=W)

        geo = ttk.Radiobutton(langfrm, text="Французкий", variable=lang_var, value="fr")
        geo.grid(row=0, column=3, sticky=W)

        btn = ttk.Button(parametrs_window, text="Применить", width=50, command=prim)
        btn.grid(row=10, column=0)
        btn = ttk.Button(parametrs_window, text="Отмена", width=50, command=close)
        btn.grid(row=11, column=0)
        parametrs_window.grab_set()  # Захватываем пользовательский ввод
    elif langue == "eng":
        backgroundfrm = LabelFrame(parametrs_window, text="Background color", cursor="target")
        backgroundfrm.grid(row=0, column=0)

        # Здесь нужно передавать текущий цвет фона (предположим, он уже задан в глобальной переменной background_color)
        color_var = StringVar(
            value=background_color)  # Устанавливаем начальное значение переменной равным текущему цвету

        # Создаем радиокнопки для выбора цвета
        wh = ttk.Radiobutton(backgroundfrm, text="White", variable=color_var, value="white")
        wh.grid(row=1, column=0, sticky=W)

        bl = ttk.Radiobutton(backgroundfrm, text="Black", variable=color_var, value="black")
        bl.grid(row=2, column=0, sticky=W)

        gr = ttk.Radiobutton(backgroundfrm, text="Green", variable=color_var, value="green")
        gr.grid(row=3, column=0, sticky=W)

        bl = ttk.Radiobutton(backgroundfrm, text="Lime", variable=color_var, value="lime")
        bl.grid(row=4, column=0, sticky=W)

        gr = ttk.Radiobutton(backgroundfrm, text="Dark Green", variable=color_var, value="darkgreen")
        gr.grid(row=5, column=0, sticky=W)

        blu = ttk.Radiobutton(backgroundfrm, text="Blue", variable=color_var, value="blue")
        blu.grid(row=6, column=0, sticky=W)

        gl = ttk.Radiobutton(backgroundfrm, text="Light-Blue", variable=color_var, value="goluboy")
        gl.grid(row=7, column=0, sticky=W)

        gra = ttk.Radiobutton(backgroundfrm, text="Gray", variable=color_var, value="gray")
        gra.grid(row=8, column=0, sticky=W)
        ora = ttk.Radiobutton(backgroundfrm, text="Orange", variable=color_var, value="orange")
        ora.grid(row=9, column=0, sticky=W)
        ora = ttk.Radiobutton(backgroundfrm, text="Green Lime", variable=color_var, value="bordov")
        ora.grid(row=10, column=0, sticky=W)
        pin = ttk.Radiobutton(backgroundfrm, text="Pink", variable=color_var, value="pink")
        pin.grid(row=1, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text="Violet", variable=color_var, value="violet")
        viol.grid(row=2, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Gold", variable=color_var, value="gold")
        gol.grid(row=3, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text="Dark Red", variable=color_var, value="darkred")
        viol.grid(row=4, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Khaki", variable=color_var, value="khaki")
        gol.grid(row=5, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text="Olive", variable=color_var, value="olive")
        viol.grid(row=6, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Dark Olive", variable=color_var, value="darkolive")
        gol.grid(row=7, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Chocolate", variable=color_var, value="chocolate")
        gol.grid(row=8, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Brown", variable=color_var, value="brown")
        gol.grid(row=9, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Honeydew", variable=color_var, value="medo")
        gol.grid(row=10, column=1, sticky=W)
        ar = ttk.Radiobutton(backgroundfrm, text="Indigo", variable=color_var, value="indigo")
        ar.grid(row=1, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Aquamarine", variable=color_var, value="aquamarine")
        fyx.grid(row=2, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Tomate", variable=color_var, value="tomat")
        fyx.grid(row=3, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Coral", variable=color_var, value="coral")
        fyx.grid(row=4, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Light Coral", variable=color_var, value="lightcoral")
        fyx.grid(row=5, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Indian Red", variable=color_var, value="indian")
        fyx.grid(row=6, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Azure", variable=color_var, value="azur")
        fyx.grid(row=7, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Snow", variable=color_var, value="snow")
        fyx.grid(row=8, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Salmon", variable=color_var, value="salmon")
        fyx.grid(row=9, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Lavender", variable=color_var, value="lavan")
        fyx.grid(row=10, column=2, sticky=W)
        textfrm = LabelFrame(parametrs_window, text="Color Text", cursor="target")
        textfrm.grid(row=0, column=3)

        text_var = StringVar(value=shrift)

        ar = ttk.Radiobutton(textfrm, text="Black", variable=text_var, value="1")
        ar.grid(row=0, column=3, sticky=W)

        geo = ttk.Radiobutton(textfrm, text="White", variable=text_var, value="2")
        geo.grid(row=1, column=3, sticky=W)

        comic = ttk.Radiobutton(textfrm, text="Red", variable=text_var, value="3")
        comic.grid(row=2, column=3, sticky=W)

        courier = ttk.Radiobutton(textfrm, text="Yellow", variable=text_var, value="4")
        courier.grid(row=3, column=3, sticky=W)
        timess = ttk.Radiobutton(textfrm, text="Orange", variable=text_var, value="5")
        timess.grid(row=4, column=3, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text="Blue", variable=text_var, value="6")
        fyx.grid(row=5, column=3, sticky=W)

        courier = ttk.Radiobutton(textfrm, text="Light Blue", variable=text_var, value="7")
        courier.grid(row=6, column=3, sticky=W)
        timess = ttk.Radiobutton(textfrm, text="Pink", variable=text_var, value="8")
        timess.grid(row=7, column=3, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text="Violet", variable=text_var, value="9")
        fyx.grid(row=8, column=3, sticky=W)
        ar = ttk.Radiobutton(textfrm, text="Indigo", variable=text_var, value="10")
        ar.grid(row=0, column=4, sticky=W)

        geo = ttk.Radiobutton(textfrm, text="Brown", variable=text_var, value="11")
        geo.grid(row=1, column=4, sticky=W)

        comic = ttk.Radiobutton(textfrm, text="Gold", variable=text_var, value="12")
        comic.grid(row=2, column=4, sticky=W)

        courier = ttk.Radiobutton(textfrm, text="Olive", variable=text_var, value="13")
        courier.grid(row=3, column=4, sticky=W)
        timess = ttk.Radiobutton(textfrm, text="Lime", variable=text_var, value="14")
        timess.grid(row=4, column=4, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text="Dark Red", variable=text_var, value="15")
        fyx.grid(row=5, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text="Aquamarine", variable=text_var, value="16")
        fyx.grid(row=6, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text="Sky", variable=text_var, value="17")
        fyx.grid(row=7, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text="Yellow-Green", variable=text_var, value="18")
        fyx.grid(row=8, column=4, sticky=W)
        shriftfrm = LabelFrame(parametrs_window, text="Font", cursor="target")
        shriftfrm.grid(row=0, column=4)
        shrift_var = StringVar(value=shrift)

        ar = ttk.Radiobutton(shriftfrm, text="Arial", variable=shrift_var, value="1")
        ar.grid(row=0, column=4, sticky=W)

        geo = ttk.Radiobutton(shriftfrm, text="Georgia", variable=shrift_var, value="2")
        geo.grid(row=1, column=4, sticky=W)

        comic = ttk.Radiobutton(shriftfrm, text="Comic Sans MS", variable=shrift_var, value="3")
        comic.grid(row=2, column=4, sticky=W)

        courier = ttk.Radiobutton(shriftfrm, text="Courier New", variable=shrift_var, value="4")
        courier.grid(row=3, column=4, sticky=W)
        timess = ttk.Radiobutton(shriftfrm, text="Times New Roman", variable=shrift_var, value="5")
        timess.grid(row=4, column=4, sticky=W)

        fyx = ttk.Radiobutton(shriftfrm, text="Fixedsys", variable=shrift_var, value="6")
        fyx.grid(row=5, column=4, sticky=W)

        ar = ttk.Radiobutton(shriftfrm, text="Verdana Pro Black", variable=shrift_var, value="7")
        ar.grid(row=6, column=4, sticky=W)

        geo = ttk.Radiobutton(shriftfrm, text="Montserrat Black", variable=shrift_var, value="8")
        geo.grid(row=7, column=4, sticky=W)

        comic = ttk.Radiobutton(shriftfrm, text="Impact", variable=shrift_var, value="9")
        comic.grid(row=8, column=4, sticky=W)
        langfrm = LabelFrame(parametrs_window, text="Langue", cursor="target")
        langfrm.grid(row=1, column=0)
        lang_var = StringVar(value=shrift)

        ar = ttk.Radiobutton(langfrm, text="Russian", variable=lang_var, value="ru")
        ar.grid(row=0, column=0, sticky=W)

        geo = ttk.Radiobutton(langfrm, text="English", variable=lang_var, value="eng")
        geo.grid(row=0, column=1, sticky=W)
        ar = ttk.Radiobutton(langfrm, text="Ukranien", variable=lang_var, value="ua")
        ar.grid(row=0, column=2, sticky=W)

        geo = ttk.Radiobutton(langfrm, text="French", variable=lang_var, value="fr")
        geo.grid(row=0, column=3, sticky=W)

        # Кнопка применения выбора
        btn = ttk.Button(parametrs_window, text="Apply", width=50, command=prim)
        btn.grid(row=10, column=0)
        btn = ttk.Button(parametrs_window, text="Cancel", width=50, command=close)
        btn.grid(row=11, column=0)
        parametrs_window.grab_set()  # Захватываем пользовательский ввод
    elif langue == "ua":
        backgroundfrm = LabelFrame(parametrs_window, text="Колір фону", cursor="target")
        backgroundfrm.grid(row=0, column=0)


        color_var = StringVar(
            value=background_color)  # Устанавливаем начальное значение переменной равным текущему цвету

        # Создаем радиокнопки для выбора цвета
        wh = ttk.Radiobutton(backgroundfrm, text="Білий", variable=color_var, value="white")
        wh.grid(row=1, column=0, sticky=W)

        bl = ttk.Radiobutton(backgroundfrm, text="Чорний", variable=color_var, value="black")
        bl.grid(row=2, column=0, sticky=W)

        gr = ttk.Radiobutton(backgroundfrm, text="Зелений", variable=color_var, value="green")
        gr.grid(row=3, column=0, sticky=W)

        bl = ttk.Radiobutton(backgroundfrm, text="Лаймовий", variable=color_var, value="lime")
        bl.grid(row=4, column=0, sticky=W)

        gr = ttk.Radiobutton(backgroundfrm, text="Темно-зелений", variable=color_var, value="darkgreen")
        gr.grid(row=5, column=0, sticky=W)

        blu = ttk.Radiobutton(backgroundfrm, text="Синій", variable=color_var, value="blue")
        blu.grid(row=6, column=0, sticky=W)

        gl = ttk.Radiobutton(backgroundfrm, text="Голубий", variable=color_var, value="goluboy")
        gl.grid(row=7, column=0, sticky=W)

        gra = ttk.Radiobutton(backgroundfrm, text="Сірий", variable=color_var, value="gray")
        gra.grid(row=8, column=0, sticky=W)
        ora = ttk.Radiobutton(backgroundfrm, text="помаранчевий", variable=color_var, value="orange")
        ora.grid(row=9, column=0, sticky=W)
        ora = ttk.Radiobutton(backgroundfrm, text="Зелений лайм", variable=color_var, value="bordov")
        ora.grid(row=10, column=0, sticky=W)
        pin = ttk.Radiobutton(backgroundfrm, text="Рожевий", variable=color_var, value="pink")
        pin.grid(row=1, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text="Фіолетовий", variable=color_var, value="violet")
        viol.grid(row=2, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Золотий", variable=color_var, value="gold")
        gol.grid(row=3, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text="Темно-червоний", variable=color_var, value="darkred")
        viol.grid(row=4, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Хакі", variable=color_var, value="khaki")
        gol.grid(row=5, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text="Оливковий", variable=color_var, value="olive")
        viol.grid(row=6, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Темно-оливковий", variable=color_var, value="darkolive")
        gol.grid(row=7, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Шоколадний", variable=color_var, value="chocolate")
        gol.grid(row=8, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Коричневий", variable=color_var, value="brown")
        gol.grid(row=9, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Медова роса", variable=color_var, value="medo")
        gol.grid(row=10, column=1, sticky=W)
        ar = ttk.Radiobutton(backgroundfrm, text="Індіго", variable=color_var, value="indigo")
        ar.grid(row=1, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Аквамариновий", variable=color_var, value="aquamarine")
        fyx.grid(row=2, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Томатний", variable=color_var, value="tomat")
        fyx.grid(row=3, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Кораловий", variable=color_var, value="coral")
        fyx.grid(row=4, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Світло-кораловий", variable=color_var, value="lightcoral")
        fyx.grid(row=5, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Індийский червоний", variable=color_var, value="indian")
        fyx.grid(row=6, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Азурний", variable=color_var, value="azur")
        fyx.grid(row=7, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Сніжний", variable=color_var, value="snow")
        fyx.grid(row=8, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Лосось", variable=color_var, value="salmon")
        fyx.grid(row=9, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Лавандовий", variable=color_var, value="lavan")
        fyx.grid(row=10, column=2, sticky=W)
        textfrm = LabelFrame(parametrs_window, text="Колір тексту", cursor="target")
        textfrm.grid(row=0, column=3)

        text_var = StringVar(value=shrift)

        ar = ttk.Radiobutton(textfrm, text="Чорний", variable=text_var, value="1")
        ar.grid(row=0, column=3, sticky=W)

        geo = ttk.Radiobutton(textfrm, text="Білий", variable=text_var, value="2")
        geo.grid(row=1, column=3, sticky=W)

        comic = ttk.Radiobutton(textfrm, text="Червоний", variable=text_var, value="3")
        comic.grid(row=2, column=3, sticky=W)

        courier = ttk.Radiobutton(textfrm, text="Жовтий", variable=text_var, value="4")
        courier.grid(row=3, column=3, sticky=W)
        timess = ttk.Radiobutton(textfrm, text="Помаранчевий", variable=text_var, value="5")
        timess.grid(row=4, column=3, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text="Синій", variable=text_var, value="6")
        fyx.grid(row=5, column=3, sticky=W)

        courier = ttk.Radiobutton(textfrm, text="Голубий", variable=text_var, value="7")
        courier.grid(row=6, column=3, sticky=W)
        timess = ttk.Radiobutton(textfrm, text="Рожевий", variable=text_var, value="8")
        timess.grid(row=7, column=3, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text="Фіолетовий", variable=text_var, value="9")
        fyx.grid(row=8, column=3, sticky=W)
        ar = ttk.Radiobutton(textfrm, text="Індиго", variable=text_var, value="10")
        ar.grid(row=0, column=4, sticky=W)

        geo = ttk.Radiobutton(textfrm, text="Коричневий", variable=text_var, value="11")
        geo.grid(row=1, column=4, sticky=W)

        comic = ttk.Radiobutton(textfrm, text="Золотий", variable=text_var, value="12")
        comic.grid(row=2, column=4, sticky=W)

        courier = ttk.Radiobutton(textfrm, text="Оливковий", variable=text_var, value="13")
        courier.grid(row=3, column=4, sticky=W)
        timess = ttk.Radiobutton(textfrm, text="Лаймовий", variable=text_var, value="14")
        timess.grid(row=4, column=4, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text="Темно Червоний", variable=text_var, value="15")
        fyx.grid(row=5, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text="Аквамариновий", variable=text_var, value="16")
        fyx.grid(row=6, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text="небесний", variable=text_var, value="17")
        fyx.grid(row=7, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text="Жовто-зелений", variable=text_var, value="18")
        fyx.grid(row=8, column=4, sticky=W)
        shriftfrm = LabelFrame(parametrs_window, text="Шрифт", cursor="target")
        shriftfrm.grid(row=0, column=4)
        shrift_var = StringVar(value=shrift)

        ar = ttk.Radiobutton(shriftfrm, text="Arial", variable=shrift_var, value="1")
        ar.grid(row=0, column=4, sticky=W)

        geo = ttk.Radiobutton(shriftfrm, text="Georgia", variable=shrift_var, value="2")
        geo.grid(row=1, column=4, sticky=W)

        comic = ttk.Radiobutton(shriftfrm, text="Comic Sans MS", variable=shrift_var, value="3")
        comic.grid(row=2, column=4, sticky=W)

        courier = ttk.Radiobutton(shriftfrm, text="Courier New", variable=shrift_var, value="4")
        courier.grid(row=3, column=4, sticky=W)
        timess = ttk.Radiobutton(shriftfrm, text="Times New Roman", variable=shrift_var, value="5")
        timess.grid(row=4, column=4, sticky=W)

        fyx = ttk.Radiobutton(shriftfrm, text="Fixedsys", variable=shrift_var, value="6")
        fyx.grid(row=5, column=4, sticky=W)

        ar = ttk.Radiobutton(shriftfrm, text="Verdana Pro Black", variable=shrift_var, value="7")
        ar.grid(row=6, column=4, sticky=W)

        geo = ttk.Radiobutton(shriftfrm, text="Montserrat Black", variable=shrift_var, value="8")
        geo.grid(row=7, column=4, sticky=W)

        comic = ttk.Radiobutton(shriftfrm, text="Impact", variable=shrift_var, value="9")
        comic.grid(row=8, column=4, sticky=W)
        langfrm = LabelFrame(parametrs_window, text="Мова", cursor="target")
        langfrm.grid(row=1, column=0)
        lang_var = StringVar(value=shrift)

        ar = ttk.Radiobutton(langfrm, text="Російска", variable=lang_var, value="ru")
        ar.grid(row=0, column=0, sticky=W)

        geo = ttk.Radiobutton(langfrm, text="Англійска", variable=lang_var, value="eng")
        geo.grid(row=0, column=1, sticky=W)
        ar = ttk.Radiobutton(langfrm, text="Українска", variable=lang_var, value="ua")
        ar.grid(row=0, column=2, sticky=W)

        geo = ttk.Radiobutton(langfrm, text="Французька", variable=lang_var, value="fr")
        geo.grid(row=0, column=3, sticky=W)

        # Кнопка применения выбора
        btn = ttk.Button(parametrs_window, text="Застосувати", width=50, command=prim)
        btn.grid(row=10, column=0)
        btn = ttk.Button(parametrs_window, text="Скинути", width=50, command=close)
        btn.grid(row=11, column=0)
    elif langue == "fr":
        backgroundfrm = LabelFrame(parametrs_window, text="Couleur de fond", cursor="target")
        backgroundfrm.grid(row=0, column=0)
        color_var = StringVar(
            value=background_color)  # Устанавливаем начальное значение переменной равным текущему цвету

        # Создаем радиокнопки для выбора цвета
        wh = ttk.Radiobutton(backgroundfrm, text="Blanc", variable=color_var, value="white")
        wh.grid(row=1, column=0, sticky=W)

        bl = ttk.Radiobutton(backgroundfrm, text="Noir", variable=color_var, value="black")
        bl.grid(row=2, column=0, sticky=W)

        gr = ttk.Radiobutton(backgroundfrm, text="Vert", variable=color_var, value="green")
        gr.grid(row=3, column=0, sticky=W)

        bl = ttk.Radiobutton(backgroundfrm, text="Lime", variable=color_var, value="lime")
        bl.grid(row=4, column=0, sticky=W)

        gr = ttk.Radiobutton(backgroundfrm, text="Vert foncé", variable=color_var, value="darkgreen")
        gr.grid(row=5, column=0, sticky=W)

        blu = ttk.Radiobutton(backgroundfrm, text="Bleu", variable=color_var, value="blue")
        blu.grid(row=6, column=0, sticky=W)

        gl = ttk.Radiobutton(backgroundfrm, text="Bleu claire", variable=color_var, value="goluboy")
        gl.grid(row=7, column=0, sticky=W)

        gra = ttk.Radiobutton(backgroundfrm, text="Gris", variable=color_var, value="gray")
        gra.grid(row=8, column=0, sticky=W)
        ora = ttk.Radiobutton(backgroundfrm, text="Orange", variable=color_var, value="orange")
        ora.grid(row=9, column=0, sticky=W)
        ora = ttk.Radiobutton(backgroundfrm, text="Vert Lime", variable=color_var, value="bordov")
        ora.grid(row=10, column=0, sticky=W)
        pin = ttk.Radiobutton(backgroundfrm, text="Rose", variable=color_var, value="pink")
        pin.grid(row=1, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text="Violet", variable=color_var, value="violet")
        viol.grid(row=2, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Or", variable=color_var, value="gold")
        gol.grid(row=3, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text="Rouge foncé", variable=color_var, value="darkred")
        viol.grid(row=4, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Khaki", variable=color_var, value="khaki")
        gol.grid(row=5, column=1, sticky=W)
        viol = ttk.Radiobutton(backgroundfrm, text="Olive", variable=color_var, value="olive")
        viol.grid(row=6, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Olive foncé", variable=color_var, value="darkolive")
        gol.grid(row=7, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Chocolate", variable=color_var, value="chocolate")
        gol.grid(row=8, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Marron", variable=color_var, value="brown")
        gol.grid(row=9, column=1, sticky=W)
        gol = ttk.Radiobutton(backgroundfrm, text="Miellat", variable=color_var, value="medo")
        gol.grid(row=10, column=1, sticky=W)
        ar = ttk.Radiobutton(backgroundfrm, text="Indigo", variable=color_var, value="indigo")
        ar.grid(row=1, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Aquamarine", variable=color_var, value="aquamarine")
        fyx.grid(row=2, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Tomate", variable=color_var, value="tomat")
        fyx.grid(row=3, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Coral", variable=color_var, value="coral")
        fyx.grid(row=4, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Coral foncé", variable=color_var, value="lightcoral")
        fyx.grid(row=5, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Rouge indien", variable=color_var, value="indian")
        fyx.grid(row=6, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Azure", variable=color_var, value="azur")
        fyx.grid(row=7, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Neige", variable=color_var, value="snow")
        fyx.grid(row=8, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Saumon", variable=color_var, value="salmon")
        fyx.grid(row=9, column=2, sticky=W)
        fyx = ttk.Radiobutton(backgroundfrm, text="Lavande", variable=color_var, value="lavan")
        fyx.grid(row=10, column=2, sticky=W)
        textfrm = LabelFrame(parametrs_window, text="Couleur de text", cursor="target")
        textfrm.grid(row=0, column=3)

        text_var = StringVar(value=shrift)

        ar = ttk.Radiobutton(textfrm, text="Noir", variable=text_var, value="1")
        ar.grid(row=0, column=3, sticky=W)

        geo = ttk.Radiobutton(textfrm, text="Blanc", variable=text_var, value="2")
        geo.grid(row=1, column=3, sticky=W)

        comic = ttk.Radiobutton(textfrm, text="Rouge", variable=text_var, value="3")
        comic.grid(row=2, column=3, sticky=W)

        courier = ttk.Radiobutton(textfrm, text="Jaune", variable=text_var, value="4")
        courier.grid(row=3, column=3, sticky=W)
        timess = ttk.Radiobutton(textfrm, text="Orange", variable=text_var, value="5")
        timess.grid(row=4, column=3, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text="Bleu", variable=text_var, value="6")
        fyx.grid(row=5, column=3, sticky=W)

        courier = ttk.Radiobutton(textfrm, text="Bleu claire", variable=text_var, value="7")
        courier.grid(row=6, column=3, sticky=W)
        timess = ttk.Radiobutton(textfrm, text="Rose", variable=text_var, value="8")
        timess.grid(row=7, column=3, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text="Violet", variable=text_var, value="9")
        fyx.grid(row=8, column=3, sticky=W)
        ar = ttk.Radiobutton(textfrm, text="Indigo", variable=text_var, value="10")
        ar.grid(row=0, column=4, sticky=W)

        geo = ttk.Radiobutton(textfrm, text="Marron", variable=text_var, value="11")
        geo.grid(row=1, column=4, sticky=W)

        comic = ttk.Radiobutton(textfrm, text="Or", variable=text_var, value="12")
        comic.grid(row=2, column=4, sticky=W)

        courier = ttk.Radiobutton(textfrm, text="Olive", variable=text_var, value="13")
        courier.grid(row=3, column=4, sticky=W)
        timess = ttk.Radiobutton(textfrm, text="Lime", variable=text_var, value="14")
        timess.grid(row=4, column=4, sticky=W)

        fyx = ttk.Radiobutton(textfrm, text="Rouge foncé", variable=text_var, value="15")
        fyx.grid(row=5, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text="Aquamarine", variable=text_var, value="16")
        fyx.grid(row=6, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text="Céleste,", variable=text_var, value="17")
        fyx.grid(row=7, column=4, sticky=W)
        fyx = ttk.Radiobutton(textfrm, text="Jaune-Vert", variable=text_var, value="18")
        fyx.grid(row=8, column=4, sticky=W)
        shriftfrm = LabelFrame(parametrs_window, text="Police", cursor="target")
        shriftfrm.grid(row=0, column=4)
        shrift_var = StringVar(value=shrift)

        ar = ttk.Radiobutton(shriftfrm, text="Arial", variable=shrift_var, value="1")
        ar.grid(row=0, column=4, sticky=W)

        geo = ttk.Radiobutton(shriftfrm, text="Georgia", variable=shrift_var, value="2")
        geo.grid(row=1, column=4, sticky=W)

        comic = ttk.Radiobutton(shriftfrm, text="Comic Sans MS", variable=shrift_var, value="3")
        comic.grid(row=2, column=4, sticky=W)

        courier = ttk.Radiobutton(shriftfrm, text="Courier New", variable=shrift_var, value="4")
        courier.grid(row=3, column=4, sticky=W)
        timess = ttk.Radiobutton(shriftfrm, text="Times New Roman", variable=shrift_var, value="5")
        timess.grid(row=4, column=4, sticky=W)

        fyx = ttk.Radiobutton(shriftfrm, text="Fixedsys", variable=shrift_var, value="6")
        fyx.grid(row=5, column=4, sticky=W)

        ar = ttk.Radiobutton(shriftfrm, text="Verdana Pro Black", variable=shrift_var, value="7")
        ar.grid(row=6, column=4, sticky=W)

        geo = ttk.Radiobutton(shriftfrm, text="Montserrat Black", variable=shrift_var, value="8")
        geo.grid(row=7, column=4, sticky=W)

        comic = ttk.Radiobutton(shriftfrm, text="Impact", variable=shrift_var, value="9")
        comic.grid(row=8, column=4, sticky=W)
        langfrm = LabelFrame(parametrs_window, text="Langue", cursor="target")
        langfrm.grid(row=1, column=0)
        lang_var = StringVar(value=shrift)

        ar = ttk.Radiobutton(langfrm, text="Russe", variable=lang_var, value="ru")
        ar.grid(row=0, column=0, sticky=W)

        geo = ttk.Radiobutton(langfrm, text="Anglais", variable=lang_var, value="eng")
        geo.grid(row=0, column=1, sticky=W)
        ar = ttk.Radiobutton(langfrm, text="Ukranien", variable=lang_var, value="ua")
        ar.grid(row=0, column=2, sticky=W)

        geo = ttk.Radiobutton(langfrm, text="Français", variable=lang_var, value="fr")
        geo.grid(row=0, column=3, sticky=W)
        btn = ttk.Button(parametrs_window, text="Appliquer", width=50, command=prim)
        btn.grid(row=10, column=0)
        btn = ttk.Button(parametrs_window, text="Annuler", width=50, command=close)
        btn.grid(row=11, column=0)
    if color_var.get() == "white":
        color_var.set("white")
    elif color_var.get() == "black":
        color_var.set("black")
    elif color_var.get() == "#008000":
        color_var.set("green")
    elif color_var.get() == "#00FF00":
        color_var.set("lime")
    elif color_var.get() == "#006400":
        color_var.set("darkgreen")
    elif color_var.get() == "#0000FF":
        color_var.set("blue")
    elif color_var.get() == "#00FFFF":
        color_var.set("goluboy")
    elif color_var.get() == "gray":
        color_var.set("gray")
    elif color_var.get() == "#FF8C00":
        color_var.set("orange")
    elif color_var.get() == "#FF1493":
        color_var.set("pink")
    elif color_var.get() == "#800080":
        color_var.set("violet")
    elif color_var.get() == "#F0E68C":
        color_var.set("khaki")
    elif color_var.get() == "#8B0000":
        color_var.set("darkred")
    elif color_var.get() == "#808000":
        color_var.set("olive")
    elif color_var.get() == "#556B2F":
        color_var.set("darkolive")
    elif color_var.get() == "#D2691E":
        color_var.set("chocolate")
    elif color_var.get() == "#800000":
        color_var.set("brown")
    elif color_var.get() == "#7FFFD4":
        color_var.set("aquamarine")
    elif color_var.get() == "#87CEEB":
        color_var.set("skay")
    elif color_var.get() == "#4B0082":
        color_var.set("indigo")
    elif color_var.get() == "#FF6347":
        color_var.set("tomat")
    elif color_var.get() == "#FF7F50":
        color_var.set("coral")
    elif color_var.get() == "#F08080":
        color_var.set("lightcoral")
    elif color_var.get() == "#CD5C5C":
        color_var.set("indian")
    elif color_var.get() == "#F0FFFF":
        color_var.set("azur")
    elif color_var.get() == "#FFFAFA":
        color_var.set("snow")
    elif color_var.get() == "#FA8072":
        color_var.set("salmon")
    elif color_var.get() == "#E6E6FA":
        color_var.set("lavan")
    elif color_var.get() == "#F0FFF0":
        color_var.set("medo")
    elif color_var.get() == "#32CD32":
        color_var.set("bordov")
    else:
        color_var.set("gold")
    if shrift == "Arial":
        shrift_var.set("1")
    elif shrift == "Georgia":
        shrift_var.set("2")
    elif shrift == "Comic Sans MS":
        shrift_var.set("3")
    elif shrift == "Courier New":
        shrift_var.set("4")
    elif shrift == "Times New Roman":
        shrift_var.set("5")
    elif shrift == "Fixedsys":
        shrift_var.set("6")
    elif shrift == "Verdana Pro Black":
        shrift_var.set("7")
    elif shrift == "Montserrat Black":
        shrift_var.set("8")
    else:
        shrift_var.set("9")  # По умолчанию Fixedsys
    if text_color == "Black":
        text_var.set("1")
    elif text_color == "White":
        text_var.set("2")
    elif text_color == "Red":
        text_var.set("3")
    elif text_color == "Yellow":
        text_var.set("4")
    elif text_color == "Orange":
        text_var.set("5")
    elif text_color == "Blue":
        text_var.set("6")
    elif text_color == "#00BFFF":
        text_var.set("7")
    elif text_color == "#FF00FF":
        text_var.set("8")
    elif text_color == "#4B0082":
        text_var.set("10")
    elif text_color == "#800000":
        text_var.set("11")
    elif text_color == "#DAA520":
        text_var.set("12")
    elif text_color == "#808000":
        text_var.set("13")
    elif text_color == "#00FF00":
        text_var.set("14")
    elif text_color == "#8B0000":
        text_var.set("15")
    elif text_color == "#7FFFD4":
        text_var.set("16")
    elif text_color == "#87CEEB":
        text_var.set("17")
    elif text_color == "#9ACD32":
        text_var.set("18")
    else:
        text_var.set("9")
    if langue == "ru":
        lang_var.set("ru")
    elif langue == "eng":
        lang_var.set("eng")
    elif langue == "ua":
        lang_var.set("ua")
    elif langue == "fr":
        lang_var.set("fr")
def on_closing(event = None):
    def exitt():
        global name1,name2,background_color,text_color,ident
        if ident:
            # 2. Создаем подключение к базе данных (если базы данных не существует, она будет создана)
            conn = sqlite3.connect('players_game_durak.db')

            # 3. Создаем курсор
            cursor = conn.cursor()

            # 4. Выполняем SQL-запросы
            # Пример создания таблицы
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS players (
                                id INTEGER PRIMARY KEY,
                                name TEXT,
                                score INTEGER,
                                background_color TEXT,
                                text_color TEXT,
                                time TEXT
                        )
                    ''')
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Прмер вставки данных
            cursor.execute('''
                        INSERT INTO players (name, score,background_color,text_color,time) VALUES (?,?,?,?,?)
                    ''', (ident, score, background_color, text_color, current_time))

            # Пример выборки данных
            cursor.execute('''SELECT * FROM players ''')

            # Сохраняем изменения
            conn.commit()

            # 5. Закрываем подключение
            conn.close()
            exx.destroy()
            Win.destroy()
        else:
            Win.destroy()
    def no():
        exx.destroy()
    exx = Toplevel(Win)
    exx.geometry("300x100")
    exx.resizable(False,False)
    center_child(exx, Win)
    exx.protocol("WM_DELETE_WINDOW",
                 lambda: dismiss(exx))  # Перехватываем нажатие на крестик
    global langue
    if langue == "ru":
        lbl = Label(exx, text="Вы действительно хотите выйти из игры?")
        lbl.pack()

        btn = ttk.Button(exx, text="Да", command=exitt)
        btn.pack()
        btn1 = ttk.Button(exx, text="Нет", command=no)
        btn1.pack()
        exx.grab_set()  # Захватываем пользовательский ввод
    if langue == "eng":
        lbl = Label(exx, text="Are you sure you want to exit the game?")
        lbl.pack()

        btn = ttk.Button(exx, text="Yes", command=exitt)
        btn.pack()
        btn1 = ttk.Button(exx, text="No", command=no)
        btn1.pack()
        exx.grab_set()  # Захватываем пользовательский ввод
    if langue == "ua":
        lbl = Label(exx, text="Ви дійсно хочете вийти із гри?")
        lbl.pack()

        btn = ttk.Button(exx, text="Так", command=exitt)
        btn.pack()
        btn1 = ttk.Button(exx, text="Ні", command=no)
        btn1.pack()
        exx.grab_set()  # Захватываем пользовательский ввод
    if langue == "fr":
        lbl = Label(exx, text="Voulez-vous vraiment quitter le jeu?")
        lbl.pack()

        btn = ttk.Button(exx, text="Oui", command=exitt)
        btn.pack()
        btn1 = ttk.Button(exx, text="Non", command=no)
        btn1.pack()
        exx.grab_set()  # Захватываем пользовательский ввод
def sort_alf():
    information_win = Toplevel(Win)
    information_win.title("Информация")
    information_win.geometry("700x350")
    information_win.resizable(False, False)
    center_child(information_win, Win)
    information_win.protocol("WM_DELETE_WINDOW",
                             lambda: dismiss(information_win))  # Перехватываем нажатие на крестик
    n = Text(information_win)
    scrollbar = Scrollbar(information_win, command=n.yview)
    n.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    n.pack()

    # Подключение к базе данных и выполнение запроса
    conn = sqlite3.connect('players_game_durak.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT name,
                      score, 
                      background_color,
                      text_color,
                      time
               FROM players
               ORDER BY name ASC;''')  # Сортировка по возрастанию имени
    rows = cursor.fetchall()

    # Определение заголовков столбцов
    columns = ["Name", "Wins", "Background_Color", "Text_Color", "Time"]

    # Форматирование данных с помощью tabulate
    results = tabulate.tabulate(rows, headers=columns, tablefmt="center")

    # Вставка результатов в текстовое поле
    n.insert(1.0, str(results) + '\n')
    conn.commit()
    conn.close()
def sort_score():
    information_win = Toplevel(Win)
    information_win.title("Информация")
    information_win.geometry("700x350")
    information_win.resizable(False, False)
    center_child(information_win, Win)
    information_win.protocol("WM_DELETE_WINDOW",
                             lambda: dismiss(information_win))  # Перехватываем нажатие на крестик
    n = Text(information_win)
    scrollbar = Scrollbar(information_win, command=n.yview)
    n.config(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=RIGHT, fill=Y)
    n.pack()

    # Подключение к базе данных и выполнение запроса
    conn = sqlite3.connect('players_game_durak.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT name,
                      score, 
                      background_color,
                      text_color,
                      time
               FROM players
               ORDER BY score DESC;''')  # Сортировка по убыванию очков
    rows = cursor.fetchall()

    # Определение заголовков столбцов
    columns = ["Name", "Wins", "Background_Color", "Text_Color", "Time"]

    # Форматирование данных с помощью tabulate
    results = tabulate.tabulate(rows, headers=columns, tablefmt="center")

    # Вставка результатов в текстовое поле
    n.insert(1.0, str(results) + '\n')
    conn.commit()
    conn.close()
def data_raz():
    global langue
    if langue == "ru":
        messagebox.showinfo("Информация","Разработчики этой игры Булыгин Святослав и Сергей Багач")
    elif langue == "eng":
        messagebox.showinfo("Information","The developers of this game are Svyatoslav Bulygin and Sergey Bagach")
    elif langue == "ua":
        messagebox.showinfo("Інформація","Розробники цієї гри Булигін Святослав та Сергій Багач")
    elif langue == "fr":
        messagebox.showinfo("Information","Les développeurs de ce jeu sont Bulygin Sviatoslav et Sergey Bagach")
def datagame():
    global langue
    if langue == "ru":
        messagebox.showinfo("Информация","Эта игра написана на языке програмирования Python с использованием библиотеки Tkinter")
    elif langue == "eng":
        messagebox.showinfo("Information","This game is based on programming Python and is installed Tkinter library")
    elif langue == "ua":
        messagebox.showinfo("Информація","Ця гра написана на мові програмування Python з застосуванням біблиотеки Tkinter")
    elif langue == "fr":
        messagebox.showinfo("Information","Ce jeu est écrit dans le langage de programmation Python en utilisant la bibliothèque Tkinter")
def finish():
    global player1,player2,koloda
    if (len(player1) == 0 and len(koloda) == 0) or (len(player2) == 0 and len(koloda) == 0):
        return True
    else:
        return False
def finish1():
    global name1,name2,win,ind,score,ident,langue
    ind = False
    win = True
    if langue == "ru":
        if len(player1) == 0:
            messagebox.showinfo("Победа", f"Выграл игрок '{name1}'")
            score = 1
            ident = name1
            canvas.delete("all")
            pr()
        else:
            messagebox.showinfo("Победа", f"Выграл игрок '{name2}'")
            score = 1
            ident = name2
            canvas.delete("all")
            pr()
    elif langue == "eng":
        if len(player1) == 0:
            messagebox.showinfo("Win", f"Player '{name1} wons'")
            score = 1
            ident = name1
            canvas.delete("all")
            pr()
        else:
            messagebox.showinfo("Win", f"Player '{name2} wons'")
            score = 1
            ident = name2
            canvas.delete("all")
            pr()
    elif langue == "ua":
        if len(player1) == 0:
            messagebox.showinfo("Win", f"Player '{name1} wons'")
            score = 1
            ident = name1
            canvas.delete("all")
            pr()
        else:
            messagebox.showinfo("Win", f"Player '{name2} wons'")
            score = 1
            ident = name2
            canvas.delete("all")
            pr()
    elif langue == "fr":
        if len(player1) == 0:
            messagebox.showinfo("Victoire", f"Joueur '{name1} gagne'")
            score = 1
            ident = name1
            canvas.delete("all")
            pr()
        else:
            messagebox.showinfo("Victoire", f"Joueur '{name2} gagne'")
            score = 1
            ident = name2
            canvas.delete("all")
            pr()
def update_menu(langue):
    main_menu = Menu()
    info_menu = Menu()
    data = Menu()
    if langue == "ru":
        main_menu.add_cascade(label="Играть", command=start_game)
        main_menu.add_cascade(label="Параметры", command=parametrs)
        main_menu.add_cascade(label="Инфо", menu=info_menu)
        main_menu.add_cascade(label="Турнирная таблица", menu=data)
        data.add_cascade(label="Сортировка по алфавиту",command=sort_alf)
        data.add_cascade(label="Сортировка по очкам", command=sort_score)
        info_menu.add_cascade(label="Данные про разработчиков", command=data_raz)
        info_menu.add_cascade(label="Данные про игру", command=datagame)
        main_menu.add_cascade(label="Выход", command=on_closing)
    elif langue == "eng":
        main_menu.add_cascade(label="Play", command=start_game)
        main_menu.add_cascade(label="Parameters", command=parametrs)
        main_menu.add_cascade(label="Info", menu=info_menu)
        main_menu.add_cascade(label="Tournament table",menu=data)
        data.add_cascade(label="Sort by alphabet", command=sort_alf)
        data.add_cascade(label="Sort by points", command=sort_score)
        info_menu.add_cascade(label="Developer data", command=data_raz)
        info_menu.add_cascade(label="Game data", command=datagame)
        main_menu.add_cascade(label="Exit", command=on_closing)
    elif langue == "ua":
        main_menu.add_cascade(label="Грати", command=start_game)
        main_menu.add_cascade(label="Параметри", command=parametrs)
        main_menu.add_cascade(label="Інфо", menu=info_menu)
        main_menu.add_cascade(label="Турнирна таблиця",menu=data)
        data.add_cascade(label="Сортування за абеткою", command=sort_alf)
        data.add_cascade(label="Сортування за очками", command=sort_score)
        info_menu.add_cascade(label="Данні про розробников", command=data_raz)
        info_menu.add_cascade(label="Данні про гру", command=datagame)
        main_menu.add_cascade(label="Вихід", command=on_closing)
    elif langue == "fr":
        main_menu.add_cascade(label="Jouer", command=start_game)
        main_menu.add_cascade(label="Parametres", command=parametrs)
        main_menu.add_cascade(label="Info", menu=info_menu)
        main_menu.add_cascade(label="Résultats classements", menu=data)
        data.add_cascade(label="Trier par alphabet", command=sort_alf)
        data.add_cascade(label="Tri par points", command=sort_score)
        info_menu.add_cascade(label="Données de développeur", command=data_raz)
        info_menu.add_cascade(label="Données de jeu", command=datagame)
        main_menu.add_cascade(label="Sortie", command=on_closing)
    Win.config(menu=main_menu)
#Окно
Win = Tk()

Win.title("Игра в дурака")
Win.geometry(f"{Win.winfo_screenwidth()}x{Win.winfo_screenheight()}")
Win.bind('<Escape>', on_closing)
Win.bind('<Alt-F4>', on_closing)
Win.protocol("WM_DELETE_WINDOW", on_closing)
# Устанавливаем иконку окна
icon_image = PhotoImage(file="D:\programar\Poker\_-removebg-preview.png")
Win.iconphoto(True, icon_image)

update_menu(langue)

canvas = Canvas(Win, bg=background_color, width=480, height=480)
canvas.pack(expand=True, fill=BOTH, padx=10, pady=10)
Win.update_idletasks()
Win.update()  # Обновляет размеры виджетов
pr()  # Вызываем функцию после обновления
Win.mainloop()