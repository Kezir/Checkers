import pygame
import pygame.locals
import os
import copy

_image_library = {}
def get_image(path):
        global _image_library
        image = _image_library.get(path)
        if image == None:
                canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
                image = pygame.image.load(canonicalized_path)
                _image_library[path] = image
        return image

pionek_bialy = get_image('flame_fire_blue (2).png')
pionek_bialy = pygame.transform.scale(pionek_bialy, (75, 75))
pionek_bialy_small = pygame.transform.scale(pionek_bialy, (25, 25))

dama_bialy = get_image('flame_fire_blue_dama.png')
dama_bialy = pygame.transform.scale(dama_bialy, (75, 75))
dama_bialy_small = pygame.transform.scale(dama_bialy, (25, 25))

pionek_czarny = get_image('flame_fire_red.png')
pionek_czarny = pygame.transform.scale(pionek_czarny, (75, 75))
pionek_czarny_small = pygame.transform.scale(pionek_czarny, (25, 25))

plansza = get_image('board.png')
plansza = pygame.transform.scale(plansza, (600, 600))

class Pole():
    def __init__(self,pozycja,stan,image,color):
        self.pozycja = pozycja
        self.stan = stan
        self.image = image
        self.color = color

    def change(self,stan,image,color):
        self.stan = stan
        self.image = image
        self.color = color

class Board(object):

    def __init__(self, width,height):

        self.surface = pygame.display.set_mode((width, height), 0, 32)
        pygame.display.set_caption("Warcaby")

        pygame.font.init()
        font_path = pygame.font.match_font('arial')
        self.font = pygame.font.Font(font_path, 48)
        self.markers = []
        self.surface.blit(plansza, (-1, 0))
        self.set_board()
        self.hit_holder = []
        self.mark = None
        self.koniec_tury = True
        self.tura = 'biale'

    def draw(self):
        self.draw_board()
        pygame.display.update()

    def draw_net(self):

        color = (255, 255, 255)
        width = self.surface.get_width()
        for i in range(1, 8):
            pos = width / 8 * i
            pygame.draw.line(self.surface, color, (0, pos), (width, pos), 1)
            pygame.draw.line(self.surface, color, (pos, 0), (pos, width), 1)

    def set_board(self):

        for x in range(8):
            if x % 2 == 1:
                for y in range(3):
                    if y % 2 == 0:
                        self.markers.append(Pole([x, y], 'pion', pionek_czarny, 'czarne'))
                    else:
                        self.markers.append(Pole([x - 1, y], 'pion', pionek_czarny, 'czarne'))
                for y in range(3, 5):
                    if y % 2 == 0:
                        self.markers.append(Pole([x, y], 'empty', None, 'empty'))
                    else:
                        self.markers.append(Pole([x - 1, y], 'empty', None, 'empty'))

                for y in range(5, 8):
                    if y % 2 == 0:
                        self.markers.append(Pole([x, y], 'pion', pionek_bialy, 'biale'))
                    else:
                        self.markers.append(Pole([x - 1, y], 'pion', pionek_bialy, 'biale'))

    def draw_board(self):

        box_side = self.surface.get_width() / 8

        for pions in self.markers:
            if pions.image != None:
                center = (pions.pozycja[0] * box_side, pions.pozycja[1] * box_side)
                self.surface.blit(pions.image, center)

    def possible_moves(self,pionek):
        possible_moves = []
        possible_hits = []
        left_up = []
        left_down = []
        right_up = []
        right_down = []

        lista_bialych = []
        lista_czarnych = []
        lista_pustych = []

        for i in self.markers:
            if i.color == 'biale':
                lista_bialych.append(i)
            elif i.color == 'czarne':
                lista_czarnych.append(i)
            else:
                lista_pustych.append(i)
        if pionek.stan == 'pion':
            poz_left_up = [pionek.pozycja[0] - 1, pionek.pozycja[1] - 1]
            poz_left_down = [pionek.pozycja[0] - 1, pionek.pozycja[1] + 1]
            poz_right_up = [pionek.pozycja[0] + 1, pionek.pozycja[1] - 1]
            poz_right_down = [pionek.pozycja[0] + 1, pionek.pozycja[1] + 1]

            poz2_left_up = [pionek.pozycja[0] - 2, pionek.pozycja[1] - 2]
            poz2_left_down = [pionek.pozycja[0] - 2, pionek.pozycja[1] + 2]
            poz2_right_up = [pionek.pozycja[0] + 2, pionek.pozycja[1] - 2]
            poz2_right_down = [pionek.pozycja[0] + 2, pionek.pozycja[1] + 2]

            for i in self.markers:
                if i.pozycja == poz_left_up:
                    left_up.append(i)
                elif i.pozycja == poz_left_down:
                    left_down.append(i)
                elif i.pozycja == poz_right_up:
                    right_up.append(i)
                elif i.pozycja == poz_right_down:
                    right_down.append(i)

            for i in self.markers:
                if i.pozycja == poz2_left_up:
                    left_up.append(i)
                elif i.pozycja == poz2_left_down:
                    left_down.append(i)
                elif i.pozycja == poz2_right_up:
                    right_up.append(i)
                elif i.pozycja == poz2_right_down:
                    right_down.append(i)

            if self.tura == 'biale':
                if len(left_up) == 1:
                    if left_up[0] in lista_pustych:
                        possible_moves.append(left_up[0])

                elif len(left_up) == 2:
                    if left_up[0] in lista_pustych:
                        possible_moves.append(left_up[0])
                    elif left_up[0] in lista_czarnych and left_up[1] in lista_pustych:
                        possible_hits.append([pionek, left_up[0], left_up[1]])

                if len(left_down) == 2:
                    if left_down[0] in lista_czarnych and left_down[1] in lista_pustych:
                        possible_hits.append([pionek, left_down[0], left_down[1]])

                if len(right_up) == 1:
                    if right_up[0] in lista_pustych:
                        possible_moves.append(right_up[0])

                elif len(right_up) == 2:
                    if right_up[0] in lista_pustych:
                        possible_moves.append(right_up[0])
                    elif right_up[0] in lista_czarnych and right_up[1] in lista_pustych:
                        possible_hits.append([pionek, right_up[0], right_up[1]])

                if len(right_down) == 2:
                    if right_down[0] in lista_czarnych and right_down[1] in lista_pustych:
                        possible_hits.append([pionek, right_down[0], right_down[1]])

            elif self.tura == 'czarne':

                if len(left_up) == 2:
                    if left_up[0] in lista_bialych and left_up[1] in lista_pustych:
                        possible_hits.append([pionek, left_up[0], left_up[1]])

                if len(left_down) == 1:
                    if left_down[0] in lista_pustych:
                        possible_moves.append(left_down[0])
                elif len(left_down) == 2:
                    if left_down[0] in lista_pustych:
                        possible_moves.append(left_down[0])
                    elif left_down[0] in lista_bialych and left_down[1] in lista_pustych:
                        possible_hits.append([pionek, left_down[0], left_down[1]])

                if len(right_up) == 2:
                    if right_up[0] in lista_bialych and right_up[1] in lista_pustych:
                        possible_hits.append([pionek, right_up[0], right_up[1]])

                if len(right_down) == 1:
                    if right_down[0] in lista_pustych:
                        possible_moves.append(right_down[0])
                elif len(right_down) == 2:
                    if right_down[0] in lista_pustych:
                        possible_moves.append(right_down[0])
                    elif right_down[0] in lista_bialych and right_down[1] in lista_pustych:
                        possible_hits.append([pionek, right_down[0], right_down[1]])


        return possible_moves,possible_hits

    def get_pozycja(self,elem):
        return elem.pozycja[0]

    def possible_moves_dama(self,pionek):

        possible_moves = []
        possible_hits = []

        left_up = []
        left_down = []
        right_up = []
        right_down = []

        temp = None

        pozycja_left_up = []
        pozycja_left_down = []
        pozycja_right_up = []
        pozycja_right_down = []

        lista_bialych = []
        lista_czarnych = []
        lista_pustych = []

        for i in self.markers:
            if i.color == 'biale':
                lista_bialych.append(i)
            elif i.color == 'czarne':
                lista_czarnych.append(i)
            else:
                lista_pustych.append(i)

        if pionek.stan == 'dama':

            for i in range(1,7):
                if pionek.pozycja[0] - i >= 0 and pionek.pozycja[1] - i >= 0:
                    pozycja_left_up.append([pionek.pozycja[0] - i,pionek.pozycja[1] - i])
                if pionek.pozycja[0] - i >= 0 and pionek.pozycja[1] + i <= 7:
                    pozycja_left_down.append([pionek.pozycja[0] - i,pionek.pozycja[1] + i])
                if pionek.pozycja[0] + i <= 7 and pionek.pozycja[1] - i >= 0:
                    pozycja_right_up.append([pionek.pozycja[0] + i,pionek.pozycja[1] - i])
                if pionek.pozycja[0] + i <= 7 and pionek.pozycja[1] + i <= 7:
                    pozycja_right_down.append([pionek.pozycja[0] + i,pionek.pozycja[1] + i])
            for i in self.markers:
                if i.pozycja in pozycja_left_up:
                    left_up.append(i)
                    pozycja_left_up.remove(i.pozycja)
                elif i.pozycja in pozycja_left_down:
                    left_down.append(i)
                    pozycja_left_down.remove(i.pozycja)
                elif i.pozycja in pozycja_right_up:
                    right_up.append(i)
                    pozycja_right_up.remove(i.pozycja)
                elif i.pozycja in pozycja_right_down:
                    right_down.append(i)
                    pozycja_right_down.remove(i.pozycja)

            left_up.sort(key=self.get_pozycja)
            left_up.reverse()
            right_up.sort(key=self.get_pozycja)
            left_down.sort(key=self.get_pozycja)
            left_down.reverse()
            right_down.sort(key=self.get_pozycja)

            for i in left_up:
                if i.color == 'empty':
                    if temp == None:
                        possible_moves.append(i)
                    else:
                        possible_hits.append([pionek,temp,i])
                        break
                elif i.color != pionek.color:
                    temp = i
                else:
                    break
            temp = None
            for i in left_down:
                if i.color == 'empty':
                    if temp == None:
                        possible_moves.append(i)
                    else:
                        possible_hits.append([pionek,temp,i])
                        break
                elif i.color != pionek.color :
                    temp = i
                else:
                    break
            temp = None
            for i in right_up:
                if i.color == 'empty':
                    if temp == None:
                        possible_moves.append(i)
                    else:
                        possible_hits.append([pionek,temp,i])
                        break
                elif i.color != pionek.color:
                    temp = i
                else:
                    break
            temp = None
            for i in right_down:
                if i.color == 'empty':
                    if temp == None:
                        possible_moves.append(i)
                    else:
                        possible_hits.append([pionek,temp,i])
                        break
                elif i.color != pionek.color:
                    temp = i
                else:
                    break
        #for i in possible_hits:
            #for j in i:
            #    print(j.pozycja)
            #print("---")
        return possible_moves,possible_hits
    def set_focus(self,pozycja):

        for i in self.markers:
            if i.pozycja == pozycja:
                if self.tura == 'biale' and i.color == 'biale':
                    self.mark = i
                elif self.tura == 'czarne' and i.color == 'czarne':
                    self.mark = i

    def hit_help(self,ruch):
        temp_1 = ruch[0].stan
        temp_2 = ruch[0].image
        temp_3 = ruch[0].color
        ruch[0].change('empty', None, 'empty')
        ruch[-1].change(temp_1, temp_2, temp_3)
        ruch[-2].change('empty', None, 'empty')

    def hit(self,ruch):
        temp_1 = ruch[0].stan
        temp_2 = ruch[0].image
        temp_3 = ruch[0].color
        for i in ruch:
            i.change('empty', None, 'empty')
        ruch[-1].change(temp_1, temp_2, temp_3)

        pygame.draw.rect(self.surface, (0, 0, 0), (ruch[0].pozycja[0] * 75, ruch[0].pozycja[1] * 75, 75, 75))
        pygame.draw.rect(self.surface, (0, 0, 0), (ruch[-2].pozycja[0] * 75, ruch[-2].pozycja[1] * 75, 75, 75))

    def move(self,pionek,ruch):

        temp_1 = pionek.stan
        temp_2 = pionek.image
        temp_3 = pionek.color
        pionek.change(ruch.stan,ruch.image,ruch.color)
        ruch.change(temp_1,temp_2,temp_3)
        pygame.draw.rect(self.surface,(0,0,0),(pionek.pozycja[0]*75,pionek.pozycja[1]*75,75,75))

    def check_marks(self):
        lista_bialych = []
        lista_czarnych = []
        lista_pustych = []

        possible_marks = []

        for i in self.markers:
            if i.color == 'biale':
                lista_bialych.append(i)
            elif i.color == 'czarne':
                lista_czarnych.append(i)
            else:
                lista_pustych.append(i)

        if self.tura == 'biale':
            for i in lista_bialych:
                if i.stan == 'pion':
                    possible_moves,possible_hits = self.possible_moves(i)
                elif i.stan == 'dama':
                    possible_moves, possible_hits = self.possible_moves_dama(i)
                    #self.possible_moves_dama(i)
                if len(possible_hits) > 0:
                    possible_marks.append(i)

        elif self.tura == 'czarne':
            for i in lista_czarnych:
                if i.stan == 'pion':
                    possible_moves,possible_hits = self.possible_moves(i)
                elif i.stan == 'dama':
                    possible_moves, possible_hits = self.possible_moves_dama(i)
                    #self.possible_moves_dama(i)
                if len(possible_hits) > 0:
                    possible_marks.append(i)


        return possible_marks

    def move_help(self,pionek,ruch):

        temp_1 = pionek.stan
        temp_2 = pionek.image
        temp_3 = pionek.color
        pionek.change(ruch.stan,ruch.image,ruch.color)
        ruch.change(temp_1,temp_2,temp_3)

    def wartosc_ruchu(self,start,koniec):
        wartosc = []
        points = 0
        count = 0
        possible_moves = []
        possible_hits_temp = []

        lista_bialych = []
        lista_czarnych = []
        lista_pustych = []

        if self.tura == 'czarne':
            for j in koniec:
                self.move_help(start,j)
                for i in self.markers:
                    if i.color == 'biale':
                        lista_bialych.append(i)
                    elif i.color == 'czarne':
                        lista_czarnych.append(i)
                    else:
                        lista_pustych.append(i)

                left_up,left_down,right_up,right_down = self.find_square(j)

                if start.pozycja[1] >= 4 and start.stan == 'pion':
                    points += 2
                self.tura = 'biale'
                for i in self.hit_holder:
                    possible_moves, possible_hits = self.possible_moves(i)
                    if len(possible_hits) == 0:
                        points += 3
                        break

                for i in lista_bialych:
                    possible_moves, possible_hits = self.possible_moves(i)
                    for x in possible_hits:
                        count += 1

                if count < len(self.hit_holder):
                    points += 3
                elif count == len(self.hit_holder):
                    points += 1
                elif count > len(self.hit_holder):
                    points -= 2


                self.tura = 'czarne'

                if left_up[0] == start:
                    if right_up[0].color != 'empty' and left_down[0].color != 'empty' and right_down[0].color != 'biale':
                        points += 2
                        if (right_up[1].color == 'empty' and right_up[0].color == 'biale') or (left_down[1].color == 'empty' and left_down[0].color == 'biale'):
                            points += 1
                    elif right_up[0].color != 'biale' and left_down[0].color != 'biale' and right_down[0].color != 'biale':
                        points += 1
                    else:
                        points += 0

                elif left_down[0] == start:
                    if left_up[0].color != 'empty' and right_down[0].color != 'empty' and right_up[0].color != 'biale':
                        points += 2
                        if (left_up[1].color == 'empty' and left_up[0].color == 'biale') or (right_down[1].color == 'empty' and right_down[0].color == 'biale'):
                            points += 1
                    elif left_up[0].color != 'biale' and right_down[0].color != 'biale' and right_up[0].color != 'biale':
                        points += 1
                    else:
                        points += 0


                elif right_up[0] == start:
                    if left_up[0].color != 'empty' and right_down[0].color != 'empty' and left_down[0].color != 'biale':
                        points += 2
                        if (left_up[1].color == 'empty' and left_up[0].color == 'biale') or (right_down[1].color == 'empty' and right_down[0].color == 'biale'):
                            points += 1
                    elif left_up[0].color != 'biale' and right_down[0].color != 'biale' and left_down[0].color != 'biale':
                        points += 1
                    else:
                        points += 0


                elif right_down[0] == start:
                    if left_down[0].color != 'empty' and right_up[0].color != 'empty' and left_up[0].color != 'biale':
                        points += 2
                        if (left_down[1].color == 'empty' and left_down[0].color == 'biale') or (right_up[1].color == 'empty' and right_up[0].color == 'biale'):
                            points += 1
                    elif left_down[0].color != 'biale' and right_up[0].color != 'biale' and left_up[0].color != 'biale':
                        points += 1
                    else:
                        points += 0

                self.move_help(start,j)
                wartosc.append([start, j, points])
                points = 0


        return wartosc

    def find_square(self,pionek):

        left_up = []
        left_down = []
        right_up = []
        right_down = []

        if pionek.stan != 'empty':
            poz_left_up = [pionek.pozycja[0] - 1, pionek.pozycja[1] - 1]
            poz_left_down = [pionek.pozycja[0] - 1, pionek.pozycja[1] + 1]
            poz_right_up = [pionek.pozycja[0] + 1, pionek.pozycja[1] - 1]
            poz_right_down = [pionek.pozycja[0] + 1, pionek.pozycja[1] + 1]

            poz2_left_up = [pionek.pozycja[0] - 2, pionek.pozycja[1] - 2]
            poz2_left_down = [pionek.pozycja[0] - 2, pionek.pozycja[1] + 2]
            poz2_right_up = [pionek.pozycja[0] + 2, pionek.pozycja[1] - 2]
            poz2_right_down = [pionek.pozycja[0] + 2, pionek.pozycja[1] + 2]

            for i in self.markers:
                if i.pozycja == poz_left_up:
                    left_up.append(i)
                elif i.pozycja == poz_left_down:
                    left_down.append(i)
                elif i.pozycja == poz_right_up:
                    right_up.append(i)
                elif i.pozycja == poz_right_down:
                    right_down.append(i)

            for i in self.markers:
                if i.pozycja == poz2_left_up:
                    left_up.append(i)
                elif i.pozycja == poz2_left_down:
                    left_down.append(i)
                elif i.pozycja == poz2_right_up:
                    right_up.append(i)
                elif i.pozycja == poz2_right_down:
                    right_down.append(i)

            temp = Pole([-1,-1],None,None,None)

            for i in range(0,2):
                if len(left_up) >= 2:
                    break
                else:
                    left_up.append(temp)

            for i in range(0,2):
                if len(left_down) >= 2:
                    break
                else:
                    left_down.append(temp)

            for i in range(0,2):
                if len(right_up) >= 2:
                    break
                else:
                    right_up.append(temp)

            for i in range(0,2):
                if len(right_down) >= 2:
                    break
                else:
                    right_down.append(temp)

        return left_up,left_down,right_up,right_down



    def check_hit_x(self,ruch,points,lista):


        if not lista:
            lista.append(ruch)
        if ruch[-1].stan == 'pion':
            possible_moves, possible_hits = self.possible_moves(ruch[-1])
        elif ruch[-1].stan == 'dama':
            possible_moves, possible_hits = self.possible_moves_dama(ruch[-1])

        if possible_hits:
            points += 2
            for i in possible_hits:
                lista.append(i)
                self.hit_help(i)
                self.check_hit_x(i,points,lista)

        return lista,points

    def wartosc_bicia(self,ruch):
        points = 0
        temp_1 = []

        if self.tura == 'czarne':

            self.hit_help(ruch)

            lista,points = self.check_hit_x(ruch,points,lista=[])
            self.tura = 'biale'
            for i in self.hit_holder:
                possible_moves, possible_hits = self.possible_moves(i)
                if len(possible_hits) == 0:
                    points += 3
                    break
            self.tura = 'czarne'

            for i in lista:
                temp_1 = temp_1 + i
            temp_1.append(points)
        return temp_1

    def back(self,lista,back_up):
        for i in range(len(lista)):
            lista[i].change(back_up[i][0],back_up[i][1],back_up[i][2])

    def AI_vs_player(self,dx,dy):
        if self.tura == 'biale':
            self.player_vs_player(dx,dy)
        if self.tura == 'czarne':

            wartosci = []
            possible_moves_temp = []
            possible_moves = []
            move_points = []
            possible_hits = []
            possible_hits_temp = []

            for i in self.markers:
                if i.stan == 'pion' and i.color == 'czarne':
                    possible_moves_temp,possible_hits_temp = self.possible_moves(i)
                elif i.stan == 'dama' and i.color == 'czarne':
                    possible_moves_temp, possible_hits_temp = self.possible_moves_dama(i)

                if len(possible_hits_temp) > 0 and i.stan != 'empty' and i.color == 'czarne':
                    for j in possible_hits_temp:
                        possible_hits.append(j)

                if not possible_hits:
                    if len(possible_moves_temp) > 0 and i.stan != 'empty' and i.color == 'czarne':
                        move_points.append(i)
                        possible_moves.append(possible_moves_temp)

            if not possible_hits:
                for i in range(len(possible_moves)):
                    wartosc = self.wartosc_ruchu(move_points[i],possible_moves[i])
                    for j in wartosc:
                        #print(j[0].pozycja,j[1].pozycja,j[2])
                        wartosci.append(j)
               # print("----")

                #for i in wartosci:
                #    print(i)
                print(wartosci)
                wynik = sorted(wartosci, key=lambda x: x[-1], reverse=True)[0]
                self.move(wynik[0],wynik[1])
                wynik.pop(-1)
            else:

                for i in range(len(possible_hits)):
                    temp_list = []
                    for j in possible_hits[i]:
                        temp_list.append([j.stan,j.image,j.color])
                    wartosc = self.wartosc_bicia(possible_hits[i])
                    wartosci.append(wartosc)
                    self.back(possible_hits[i],temp_list)
                #print("---")
                #for i in wartosci:
                #    print(i)
                #print("---")
                wynik = sorted(wartosci, key=lambda x: x[-1], reverse=True)[0]

                wynik.pop(-1)

                for i in range(0,len(wynik)-1,3):
                    self.hit([wynik[i],wynik[i+1],wynik[i+2]])

            if wynik[-1].pozycja[1] == 7 and wynik[-1].stan == 'pion':
                pygame.draw.rect(self.surface, (0, 0, 0),
                                 (wynik[-1].pozycja[0] * 75, wynik[-1].pozycja[1] * 75, 75, 75))
                wynik[-1].change('dama', dama_bialy, 'czarne')
            self.tura = 'biale'


    def player_vs_player(self, dx, dy):
        cell_size = self.surface.get_width() / 8
        x = int(dx / cell_size)
        y = int(dy / cell_size)
        pozycja = [x,y]
        ruch = None
        temp = None
        possible_moves = []
        possible_hits = []
        possible_hits_temp = []

        for i in self.markers:
            if i.pozycja == pozycja and i.stan == 'empty':
                ruch = i
            elif i.pozycja == pozycja:
                temp = i

        if self.mark != None and ruch != None or self.koniec_tury == False:
            if self.mark.stan == 'dama':
                possible_moves, possible_hits = self.possible_moves_dama(self.mark)
            else:
                possible_moves, possible_hits = self.possible_moves(self.mark)
            self.hit_holder = possible_hits

        if ruch == None:
            self.mark = None

        if self.mark != None:
            if self.mark.stan == 'pion' or self.mark.stan == 'dama':
                if not possible_hits:
                    if ruch in possible_moves:
                        self.move(self.mark,ruch)
                        if self.tura == 'biale':
                            if ruch.pozycja[1] == 0:
                                pygame.draw.rect(self.surface, (0, 0, 0),
                                                 (ruch.pozycja[0] * 75, ruch.pozycja[1] * 75, 75, 75))
                                ruch.change('dama',dama_bialy,'biale')
                            self.tura = 'czarne'
                        elif self.tura == 'czarne':
                            if ruch.pozycja[1] == 7:
                                pygame.draw.rect(self.surface, (0, 0, 0),
                                                 (ruch.pozycja[0] * 75, ruch.pozycja[1] * 75, 75, 75))
                                ruch.change('dama',dama_bialy,'czarne')
                            self.tura = 'biale'
                        self.mark = None
                        ruch = None
                else:
                    for i in possible_hits:
                        if ruch == i[-1]:
                            self.hit(i)
                            self.hit_holder.remove(i)
                            if ruch.stan == 'pion':
                                possible_moves, possible_hits_temp = self.possible_moves(ruch)
                            elif ruch.stan == 'dama':
                                possible_moves, possible_hits_temp = self.possible_moves_dama(ruch)
                            if not possible_hits_temp:
                                if self.tura == 'biale':
                                    if ruch.pozycja[1] == 0:
                                        pygame.draw.rect(self.surface, (0, 0, 0),
                                                         (ruch.pozycja[0] * 75, ruch.pozycja[1] * 75, 75, 75))
                                        ruch.change('dama', dama_bialy, 'biale')
                                    self.tura = 'czarne'
                                elif self.tura == 'czarne':
                                    if ruch.pozycja[1] == 7:
                                        pygame.draw.rect(self.surface, (0, 0, 0),
                                                         (ruch.pozycja[0] * 75, ruch.pozycja[1] * 75, 75, 75))
                                        ruch.change('dama', dama_bialy, 'czarne')
                                    self.tura = 'biale'
                                self.mark = None
                                ruch = None
                                break
                            else:
                                self.koniec_tury = False
                                self.mark = ruch
                                self.player_vs_player(dx,dy)


        self.koniec_tury = True

        if self.mark == None and ruch == None:
            possible_marks = self.check_marks()
            if not possible_marks:
                self.set_focus(pozycja)
            else:
                if temp in possible_marks:
                    self.set_focus(pozycja)



class Warcaby(object):

    def __init__(self, width,height):

        pygame.init()

        self.fps_clock = pygame.time.Clock()

        self.board = Board(width,height)

    def run(self):
        while not self.handle_events():
            self.board.draw()
            self.fps_clock.tick(15)

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                pygame.quit()
                return True

            if event.type == pygame.locals.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                #self.board.player_vs_player(x,y)
                self.board.AI_vs_player(x,y)



if __name__ == "__main__":
    game = Warcaby(600,600)
    game.run()