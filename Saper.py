import copy
import random
import sys
import time
import pygame
import pygame.mouse
from pygame.draw import rect
from pygame.locals import *

# from random import randint
# from math import pi
pygame.init()

# ---KOLORY------------------------------------------------------------------------------------------------------------
BLACK = (0, 0, 0)
GREY = (120, 120, 120)
GREYDARK = (66, 66, 66)
GREYLIGHT = (200, 200, 200)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREENLIGHT = (190, 250, 30)
GREENDARK = (10, 160, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 144)
ORANGE = (255, 166, 0)
BLUELIGHT = (0, 255, 255)

# ---OKIENKO-----------------------------------------------------------------------------------------------------------
szerokosc = 1000
wysokosc = 700
okienko = pygame.display.set_mode((szerokosc, wysokosc))

okienko.fill(GREY)
pygame.display.set_caption("Saper version 1.1")

# ---ZMIENNE-----------------------------------------------------------------------------------------------------------
grubosc = 1
kwadracik = 30
odstep = 40

poz_sapera_x = int(szerokosc * 0.1)
poz_sapera_y = int(wysokosc * 0.1)

wym_x = 25
wym_y = 20

wym_tablicy_x = wym_x*kwadracik
wym_tablicy_y = wym_y*kwadracik

poz_next_fig_x = poz_sapera_x + wym_tablicy_x + kwadracik * 2
poz_next_fig_y = poz_sapera_y + kwadracik * 7 + 11

tablica = [[1 for n in range(wym_x)] for n in range(wym_y)]      # tablica; 1 - zamknięte wartości, 0 - otwarte wartości
bomby = [[0 for n in range(wym_x)] for n in range(wym_y)]
# umieszczenie bomb; -1 - bomba, 0 - nie ma bomb dookoła, inne liczby - to ile bomb jest dookoła

koniec_gry = 0
liczba_bomb = 60
wskaznik_x = 0
wskaznik_y = 0                                         #pomocnicze, potem można zmienić na myszkę
klawiatura = 1

# ---import obrazków --------------------------------------------------------------------------------------------------
bomb = pygame.image.load('bomba.png')
flag = pygame.image.load('flaga.png')
box = pygame.image.load('box.png')
ifbox = pygame.image.load('ifbox.png')
zero = pygame.image.load('zero.png')
check = pygame.image.load('check.png')
bomb_small = pygame.transform.scale(bomb, (kwadracik, kwadracik))
#flag_small = pygame.transform.scale(flag, (kwadracik*0.6, kwadracik*0.6))
box_small = pygame.transform.scale(box, (kwadracik, kwadracik))
ifbox_small = pygame.transform.scale(ifbox, (kwadracik, kwadracik))
zero_small = pygame.transform.scale(zero, (kwadracik, kwadracik))
check_small = pygame.transform.scale(check, (kwadracik, kwadracik))

one = pygame.image.load('one.png')
two = pygame.image.load('two.png')
three = pygame.image.load('three.png')
four = pygame.image.load('four.png')
five = pygame.image.load('five.png')
six = pygame.image.load('six.png')
seven = pygame.image.load('seven.png')
eight = pygame.image.load('eight.png')
one_small = pygame.transform.scale(one, (kwadracik, kwadracik))
two_small = pygame.transform.scale(two, (kwadracik, kwadracik))
three_small = pygame.transform.scale(three, (kwadracik, kwadracik))
four_small = pygame.transform.scale(four, (kwadracik, kwadracik))
five_small = pygame.transform.scale(five, (kwadracik, kwadracik))
six_small = pygame.transform.scale(six, (kwadracik, kwadracik))
seven_small = pygame.transform.scale(seven, (kwadracik, kwadracik))
eight_small = pygame.transform.scale(eight, (kwadracik, kwadracik))

# ---WYGLĄD------------------------------------------------------------------------------------------------------------
pygame.draw.rect(okienko, BLACK,        [poz_sapera_x + 3, poz_sapera_y + 3, wym_x * kwadracik, wym_y * kwadracik])
pygame.draw.rect(okienko, GREYDARK,     [poz_sapera_x, poz_sapera_y, wym_x * kwadracik, wym_y * kwadracik], grubosc)
pygame.draw.rect(okienko, GREYLIGHT,    [poz_sapera_x + 1, poz_sapera_y + grubosc, wym_x * kwadracik - 2, wym_y * kwadracik - 2])

for i in range(wym_x-1):
    pygame.draw.line(okienko, GREY, [i * kwadracik + poz_sapera_x + kwadracik, poz_sapera_y + 2],
                    [i * kwadracik + poz_sapera_x + kwadracik, poz_sapera_y + 600 - 3], 1)
for i in range(wym_y-1):
    pygame.draw.line(okienko, GREY, [poz_sapera_x + 2, i * kwadracik + poz_sapera_y + kwadracik],
                    [poz_sapera_x + 400 - 3, i * kwadracik + poz_sapera_y + kwadracik], 1)

# ---Wypełnianie tablicy BOMBY ----------------------------------------------------------------------------------------

def dodawanie_bomb_do_tablicy(liczba_bomb):                                                                          # SAPER ---
    ile_bomb = liczba_bomb
    while ile_bomb > 0:
        i = random.randint(0, wym_y - 1)
        j = random.randint(0, wym_x - 1)
        if bomby[i][j] != -1:
            bomby[i][j] = -1
            ile_bomb = ile_bomb - 1

def wypelnianie_cyframi_tab_bomby():                                                                                # SAPER ---
    for i in range(wym_y):
        for j in range(wym_x):
            if bomby[i][j] == -1:
                if i - 1 >= 0 and j - 1 >= 0 and bomby[i - 1][j - 1] != -1:                 # lewa góra
                    bomby[i - 1][j - 1] = bomby[i - 1][j - 1] + 1
                if i - 1 >= 0 and bomby[i - 1][j] != -1:                                    # góra
                    bomby[i - 1][j] = bomby[i - 1][j] + 1
                if i - 1 >= 0 and j + 1 < wym_x and bomby[i - 1][j + 1] != -1:              # prawa góra
                    bomby[i - 1][j + 1] = bomby[i - 1][j + 1] + 1
                if j - 1 >= 0 and bomby[i][j - 1] != -1:                                    # lewa
                    bomby[i][j - 1] = bomby[i][j - 1] + 1
                if j + 1 < wym_x and bomby[i][j + 1] != -1:                                 # prawa
                    bomby[i][j + 1] = bomby[i][j + 1] + 1
                if i + 1 < wym_y and j - 1 >= 0 and bomby[i + 1][j - 1] != -1:              # lewa dół
                    bomby[i + 1][j - 1] = bomby[i + 1][j - 1] + 1
                if i + 1 < wym_y and bomby[i + 1][j] != -1:                                 # dół
                    bomby[i + 1][j] = bomby[i + 1][j] + 1
                if i + 1 < wym_y and j + 1 < wym_x and bomby[i + 1][j + 1] != -1:           # prawy dół
                    bomby[i + 1][j + 1] = bomby[i + 1][j + 1] + 1
# ---------------------------------------------------------------------------------------------------------------------
def zeruj_tablice():                                                                                                     # SAPER ---
    for i in range(wym_y):
        for j in range(wym_x):
            tablica[i][j] = 1

def otworz_wartosci_w_tablicy(i, j):                                                                                     # SAPER ---
    if tablica[j][i] and bomby[j][i] == 0:
        if j - 1 >= 0:                          # góra // bomba = 0
            tablica[j][i] = 0
            otworz_wartosci_w_tablicy(i, j - 1)
        if i - 1 >= 0:                          # lewa
            tablica[j][i] = 0
            otworz_wartosci_w_tablicy(i - 1, j)
        if i + 1 < wym_x:                       # prawa
            tablica[j][i] = 0
            otworz_wartosci_w_tablicy(i + 1, j)
        if j + 1 < wym_y:                       # dół
            tablica[j][i] = 0
            otworz_wartosci_w_tablicy(i, j + 1)

        if i - 1 >= 0 and j - 1 >= 0:  # lewa góra
            tablica[j][i] = 0
            otworz_wartosci_w_tablicy(i - 1, j - 1)
        if i + 1 < wym_x and j - 1 >= 0:  # prawa góra
            tablica[j][i] = 0
            otworz_wartosci_w_tablicy(i + 1, j - 1)
        if j + 1 < wym_y and i - 1 >= 0:  # lewa dół
            tablica[j][i] = 0
            otworz_wartosci_w_tablicy(i - 1, j + 1)
        if i + 1 < wym_x and j + 1 < wym_y:  # prawy dół
            tablica[j][i] = 0
            otworz_wartosci_w_tablicy(i + 1, j + 1)

    if tablica[j][i] and bomby[j][i]:
        if j - 1 >= 0:                          # góra // bomba > 0
            tablica[j][i] = 0
        if i - 1 >= 0:                          # lewa
            tablica[j][i] = 0
        if i + 1 < wym_x:                       # prawa
            tablica[j][i] = 0
        if j + 1 < wym_y:                       # dół
            tablica[j][i] = 0

def czy_koniec_gry(wskaznik_x, wskaznik_y):
    koniec_gry = 0
    if bomby[wskaznik_y][wskaznik_x] == -1 and tablica[wskaznik_y][wskaznik_x] == 0:
        koniec_gry = 1
        for i in range(wym_y):
            for j in range(wym_x):
                if bomby[i][j] == -1:
                    tablica[i][j] = 0
    return koniec_gry

def czy_wygrana(liczba_bomb):
    suma = 0
    for i in range(wym_y):
        for j in range(wym_x):
            suma = suma + tablica[i][j]
            if tablica[i][j] == 0 and bomby[i][j] == -1:
                return 1
    if liczba_bomb == suma:
        return 2

def pozycja_x(x):
    licznik_indeks_x = 0
    x = x - poz_sapera_x
    x = x/kwadracik
    for i in range(wym_x):
        if x >= licznik_indeks_x * kwadracik and x < licznik_indeks_x * kwadracik + kwadracik:
            return licznik_indeks_x

def pozycja_y(y):
    licznik_indeks_y = 0
    y = y - poz_sapera_y
    y = y/kwadracik
    for i in range(wym_y):
        if y >= licznik_indeks_y * kwadracik and y < licznik_indeks_y * kwadracik + kwadracik:
            return licznik_indeks_y

def wyswietl_tablice():
    poz_x = poz_sapera_x + 1
    poz_y = poz_sapera_y + 1
    for i in range(wym_y):
        for j in range(wym_x):
            if tablica[i][j] == 1:
                okienko.blit(box_small, (poz_x, poz_y))
            else:
                if bomby[i][j] == -1:
                    okienko.blit(bomb_small, (poz_x, poz_y))
                if bomby[i][j] == 0:
                    okienko.blit(zero_small, (poz_x, poz_y))

                if bomby[i][j] == 1:
                    okienko.blit(one_small, (poz_x, poz_y))
                if bomby[i][j] == 2:
                    okienko.blit(two_small, (poz_x, poz_y))
                if bomby[i][j] == 3:
                    okienko.blit(three_small, (poz_x, poz_y))
                if bomby[i][j] == 4:
                    okienko.blit(four_small, (poz_x, poz_y))
                if bomby[i][j] == 5:
                    okienko.blit(five_small, (poz_x, poz_y))
                if bomby[i][j] == 6:
                    okienko.blit(six_small, (poz_x, poz_y))
                if bomby[i][j] == 7:
                    okienko.blit(seven_small, (poz_x, poz_y))
                if bomby[i][j] == 8:
                    okienko.blit(eight_small, (poz_x, poz_y))
            if i == wskaznik_y and j == wskaznik_x and tablica[i][j] == 1:
                okienko.blit(ifbox_small, (poz_x, poz_y))
            if i == wskaznik_y and j == wskaznik_x and tablica[i][j] == 0:
                okienko.blit(check_small, (poz_x - 1, poz_y - 1))

            poz_x = poz_x + kwadracik
        poz_y = poz_y + kwadracik
        poz_x = poz_sapera_x + 1

# ---ZMIENNE CZ. 2-----------------------------------------------------------------------------------------------------
licznik = 0
stop = False
czas = 300



# ---GŁÓWNA------------------------------------------------------------------------------------------------------------
dodawanie_bomb_do_tablicy(liczba_bomb)
wypelnianie_cyframi_tab_bomby()

while 1:
    for event in pygame.event.get():
        wyswietl_tablice()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

        if klawiatura and event.type == KEYDOWN and event.key == K_DOWN:
            if wskaznik_y < wym_tablicy_y:
                wskaznik_y = wskaznik_y + 1
        if klawiatura and event.type == KEYDOWN and event.key == K_UP:
            if wskaznik_y > 0:
                wskaznik_y = wskaznik_y - 1
        if klawiatura and event.type == KEYDOWN and event.key == K_LEFT:
            if wskaznik_x > 0:
                wskaznik_x = wskaznik_x - 1
        if klawiatura and event.type == KEYDOWN and event.key == K_RIGHT:
            if wskaznik_x < wym_tablicy_x:
                wskaznik_x = wskaznik_x + 1

        if event.type == KEYDOWN and event.key == K_SPACE:
            otworz_wartosci_w_tablicy(wskaznik_x, wskaznik_y)
            koniec_gry = czy_koniec_gry(wskaznik_x, wskaznik_y)

        if event.type == pygame.MOUSEBUTTONDOWN and not klawiatura:
            pos = list(pygame.mouse.get_pos())
            print(pygame.mouse.get_pos())
            poz_x = pozycja_x(pos[0])
            poz_y = pozycja_y(pos[1])
            otworz_wartosci_w_tablicy(int(poz_x), int(poz_y))

    # ---RYSOWANIE TŁA, prostokąty i linie ----------------------------------------------------------------------------
    if koniec_gry == 0:
        wyswietl_tablice()

    for i in range(wym_x-1):
        pygame.draw.line(okienko, GREY,     [i * kwadracik + poz_sapera_x + kwadracik, poz_sapera_y + 2],
                                                [i * kwadracik + poz_sapera_x + kwadracik, poz_sapera_y + wym_tablicy_y - 3], 1)
    for i in range(wym_y-1):
        pygame.draw.line(okienko, GREY,     [poz_sapera_x + 2, i * kwadracik + poz_sapera_y + kwadracik],
                                                [poz_sapera_x + wym_tablicy_x - 3, i * kwadracik + poz_sapera_y + kwadracik], 1)
    # -----------------------------------------------------------------------------------------------------------------
    myfont = pygame.font.SysFont('Tahoma', 30)                   # ustawianie czcionki i wielkosci czcionki
    endfont = pygame.font.SysFont('Tahoma', 60)

    minedark = myfont.render('MINESWEEPER', False, BLACK)             # Napis "MINESWEEPER"
    minelight = myfont.render('MINESWEEPER', False, YELLOW)

    end_gamedark = endfont.render('END GAME', False, BLACK)
    end_gamelight = endfont.render('END GAME', False, RED)

    wygrana_gamedark = endfont.render('YOU WIN!', False, BLACK)
    wygrana_gamelight = endfont.render('YOU WIN!', False, GREENDARK)

# ---WYSWIETLANIE TEKSTU-----------------------------------------------------------------------------------------------
    okienko.blit(minedark, (poz_sapera_x + int(wym_tablicy_x/2) - 80 + 2, int(poz_sapera_y/2) - 15 + 2))        # TYTUŁ
    okienko.blit(minelight, (poz_sapera_x + int(wym_tablicy_x/2) - 80, int(poz_sapera_y/2) - 15))

# -----------------------------------------------------------------------------------------------------------------
    koniec_gry = czy_wygrana(liczba_bomb)

    if koniec_gry == 1:
        okienko.blit(end_gamedark, (int(wym_tablicy_x / 2) + 2, int(wym_tablicy_y / 2) + 2))
        okienko.blit(end_gamelight, (int(wym_tablicy_x / 2), int(wym_tablicy_y / 2)))

    if koniec_gry == 2:
        pygame.draw.rect(okienko, GREENDARK, [0, 0, szerokosc, wysokosc])
        pygame.draw.rect(okienko, BLACK, [0, 50, szerokosc, wysokosc - 110])
        pygame.draw.rect(okienko, GREENLIGHT, [0, 70, szerokosc, wysokosc - 150])
        okienko.blit(wygrana_gamedark, (int(wym_tablicy_x / 2) + 2, int(wym_tablicy_y / 2) + 2))
        okienko.blit(wygrana_gamelight, (int(wym_tablicy_x / 2), int(wym_tablicy_y / 2)))

    pygame.display.update()
