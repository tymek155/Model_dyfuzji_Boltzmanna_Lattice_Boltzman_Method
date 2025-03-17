Go to [English version](#english-version)
# Ogólne informacje i wykorzystanie
## Projekt realizuje implementację symulacji modelu dyfuzji Boltzmanna - Lattice Boltzmann Method. Kod był uruchamiany i napisany w środowisku PyCharm.

Głównym elementem reprezentującym cząstki gazu w moim programie nadal jest klasa `Cell`. W jej polach inicjowane są wartości, 
które mówią nam o dostępności piksela/punktu planszy (tj. czy stanowi on plansze, gdzie może poruszać się badany płyn, czy barierę, 
od której ma się odpowiednio odbijać), o aktualnym stężeniu znajdującej się w punkcie, oraz trzy listy, które zawierają informacje o 
wartościach dla rozkładu równowagowego, wejściowego oraz wyjściowego, zainicjowane na wartość zero. Dodatkowo dodana została funkcja 
umożliwiająca edytowanie wartości stężenia. 

```python
class Cell: 
    def __init__(self, is_al): 
        self.is_avalible = is_al 
        self.C = 0 
        self.f_eq = [0.0, 0.0, 0.0, 0.0]  #lewo, góra, prawo, dół 
        self.f_in = [0.0, 0.0, 0.0, 0.0] 
        self.f_out = [0.0, 0.0, 0.0, 0.0] 
 
    def set_C(self, c): 
        self.C = c
```

W zakresie globalnym zainicjowana została siatka, startowo składająca się z obiektów klasy `Cell`, a każdy z nich jest ustawiony 
jako dostępny. Dodatkowo został zainicjowany wektor z wartościami wag `w`.

```python
#Siatka komórek 
grid = [[Cell(True) for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)] 
w = [0.25, 0.25, 0.25, 0.25]
```

Funkcja `eq_function` odpowiada za obliczenia wartości rozkładu równowagowego we wszystkich 
dostępnych punktach siatki. 

```python
def eq_function(): 
    for y in range(GRID_HEIGHT): 
        for x in range(GRID_WIDTH): 
            if grid[y][x].is_avalible: 
                for i in range(4): 
                    grid[y][x].f_eq[i] = grid[y][x].C * w[i]
```

Funkcja `out_function` odpowiada za obliczenia rozkładu wyjściowego, domyślnie jednak uprościłem wzór do przypisania wartości `f_eq` do `f_out` 
(możliwa jest oczywiście implementacja bardziej skomplikowanej logiki - w przypadku dyfuzji nie jest to jednak konieczne). 

```python
def out_function(): 
    for y in range(GRID_HEIGHT): 
        for x in range(GRID_WIDTH): 
            if grid[y][x].is_avalible: 
                for i in range(4): 
                    grid[y][x].f_out[i] = grid[y][x].f_eq[i]
```

Funkcja `collision` odpowiada za aktualizacje wartości rozkładu wejściowego na podstawie policzonego już rozkładu wyjściowego oraz z 
uwzględnieniem ewentualnego odbicia od ściany/przeszkody. Funkcja przechodzi przez dostępne pola całej siatki, bada czy sąsiedzi też 
byli dostępni (czy aby przypadkiem nie byli przeszkodą/ścianą). Na końcu w pętli sprawdzane jest, które komórki były dostępne i wartości 
przekazywane są do odpowiednich wartości listy f_in z f_out w przypadku odbicia lub z neighbours, jeżeli odbicie nie zachodzi. 

```python
def collision(): 
    for y in range(GRID_HEIGHT): 
        for x in range(GRID_WIDTH): 
            if grid[y][x].is_avalible: 
                #Inicjalizacja sąsiadów 
                neighbours = [-1.0, -1.0, -1.0, -1.0] 
 
                #Dolny sąsiad 
                if y > 0 and grid[y-1][x].is_avalible: 
                    neighbours[0] = grid[y-1][x].f_out[2] 
 
                #Górny sąsiad 
                if y < GRID_HEIGHT-1 and grid[y+1][x].is_avalible: 
                    neighbours[2] = grid[y+1][x].f_out[0] 
 
                #Lewy sąsiad 
                if x > 0 and grid[y][x-1].is_avalible: 
                    neighbours[1] = grid[y][x-1].f_out[3] 
 
                #Prawy sąsiad 
                if x < GRID_WIDTH-1 and grid[y][x+1].is_avalible: 
                    neighbours[3] = grid[y][x+1].f_out[1] 
 
                #Aktualizacja f_in 
                for i in range(4): 
                    if neighbours[i] == -1.0: 
                        grid[y][x].f_in[i] = grid[y][x].f_out[i]  # odbicie 
                    else: 
                        grid[y][x].f_in[i] = neighbours[i]
```

Funkcja `update_C` odpowiada za aktualizowanie wartości stężenia na podstawie otrzymanego rozkładu wejściowego. 

```python
def update_C(): 
    for y in range(GRID_HEIGHT): 
        for x in range(GRID_WIDTH): 
            if grid[y][x].is_avalible: 
                grid[y][x].C = sum(grid[y][x].f_in)
```

Funkcja `init_grid` odpowiada za zainicjowanie całej barier i przeszkód w siatce oraz za zainicjowanie wartości początkowych do 
symulacji dla lewej i prawej części sitaki.

```python
def init_grid(): 
    #Inicjalizacja warunków brzegowych i początkowych 
    for x in range(GRID_WIDTH): 
        grid[0][x] = Cell(False) 
        grid[GRID_HEIGHT - 1][x] = Cell(False) 
    for y in range(GRID_HEIGHT): 
        grid[y][0] = Cell(False) 
        grid[y][GRID_WIDTH - 1] = Cell(False) 
 
    barrier_x = GRID_WIDTH // 4 
 
    for y in range(GRID_HEIGHT): 
        if GRID_HEIGHT // 2 - 10 <= y <= GRID_HEIGHT // 2 + 10: 
            continue 
        grid[y][barrier_x] = Cell(False) 
 
    #Lewa część siatki 
    for y in range(1, GRID_HEIGHT - 1): 
        for x in range(1, barrier_x): 
            temp = Cell(True) 
            temp.set_C(1.0) 
            grid[y][x] = temp 
 
    #Prawa część siatki 
    for y in range(1, GRID_HEIGHT - 1): 
        for x in range(barrier_x + 1, GRID_WIDTH - 1): 
            temp = Cell(True) 
            temp.set_C(0.0) 
            grid[y][x] = temp 
 ```

Funkcja `draw_board` odpowiada za narysowanie w odpowiednim kolorze barier oraz komórek aktywnych w zależności poziomu stężenia 
znajdującego się w nich. 

```python
def draw_board(screen): 
    for y in range(GRID_HEIGHT): 
        for x in range(GRID_WIDTH): 
            if not grid[y][x].is_avalible: 
                color = (255, 0, 255)  #Ścianki 
            else: 
                intensity = int(np.clip(grid[y][x].C, 0, 1) * 255) 
                color = (intensity, intensity, 0) 
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
```

# Technologie
W kodzie użyto:
* Python 3.12
* NumPy 2.2.2
* Pygame 2.6.1

# Przykładowe wizualizacje
<img width="264" alt="image" src="https://github.com/user-attachments/assets/09f084db-d06c-447a-a09e-696a68b6daaf" />

<img width="252" alt="image" src="https://github.com/user-attachments/assets/b86de0c0-48db-4b5c-9488-8f8edf8a5b7e" />

<img width="255" alt="image" src="https://github.com/user-attachments/assets/1b65c35f-d90a-4036-8de9-73c510e7b7c7" />

<img width="249" alt="image" src="https://github.com/user-attachments/assets/d947f05d-fdec-433d-92dc-f75e9bf79431" />


# English version

# General Information and usage 
## The project implements the simulation of the Boltzmann diffusion model - Lattice Boltzmann Method. The code was run and written in the PyCharm environment.

