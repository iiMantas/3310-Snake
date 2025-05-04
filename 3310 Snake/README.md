![image](https://github.com/user-attachments/assets/f739e17b-85ac-4677-b8e7-751d1350264d)
# 3310 Snake
Ši programėlė – tai žaidimas, įkvėptas klasikinio „Snake“ žaidimo. Žaidėjas valdo gyvatę, kuri turi valgyti maistą, kad augtų, tačiau turi vengti susidurti su savo kūnu ir kraštais. Žaidimas baigiasi, kai gyvatė susiduria su sienomis arba savo kūnu.
Norint paleisti žaidimą, reikalinga Python aplinka, kurioje įdiegta Pygame biblioteka. Po to tereikia atlikti šiuos žingsnius: Atsisiųsti žaidimo failus ir paleisti snake.py failą.
Žaidėjas valdo gyvatę naudodamas rodyklių klavišus. Tikslas – suvalgyti maistą ir padidinti gyvatės ilgį, nesusiduriant su sienomis ar pačios gyvatės kūnu. Žaidimas baigiasi, jei įvyksta viena iš šių sąlygų.
# Analizė
## Polimorfizmas
Kas tai?
Polimorfizmas reiškia galimybę skirtingiems objektams reaguoti į tą patį metodą skirtingais būdais. Tai leidžia vieną metodą naudoti kelioms klasėms, tačiau kiekviena klasė įgyvendina šį metodą pagal savo poreikius.

Kaip tai veikia?
Kai metodas yra iškviečiamas ant skirtingų objektų, kurie priklauso skirtingoms klasėms, bus iškviesta teisinga versija priklausomai nuo objekto tipo.

Kaip tai naudojama tavo žaidime?
Mano žaidime polimorfizmas naudojamas per draw() metodą, kuris yra tiek Food, tiek Snake klasėse. Nors abi klasės turi tą patį metodą (draw()), jų įgyvendinimas skiriasi. Game klasė neturi žinoti, kas yra piešiamas, ji tiesiog iškviečia draw() metodą, o teisingas įgyvendinimas priklauso nuo to, ar tai Snake ar Food objektas.
### Pavyzdys
class Food(GameObject):
    def draw(self, screen):  
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        screen.blit(food_surface, food_rect)

class Snake(GameObject):
    def draw(self, screen):
        for segment in self.body:
            segment_rect = (OFFSET + segment.x * cell_size, OFFSET + segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARK_GREEN, segment_rect, 0, 7)
#### Polimorfizmas naudojamas, nes Food ir Snake klasės turi tą patį draw() metodą, tačiau jis yra įgyvendintas skirtingai kiekvienoje klasėje. Game klasė tiesiog iškviečia draw() metodą, nepriklausomai nuo objekto tipo.
## Abstrakcija
Kas tai?
Abstrakcija slepia sudėtingą detalių logiką ir leidžia dirbti su aukštesnio lygio metodais.

Kaip tai veikia tavo žaidime?
Game klasė nesirūpina tuo, kaip tiksliai piešiami maistas ar gyvatė. Ji tiesiog iškviečia draw() metodą, o kuris metodas bus iškviestas priklauso nuo objekto tipo (Snake arba Food). Tai yra abstrakcija, nes žaidimas nesigilina į detales, tiesiog pasikliauja, kad kiekvienas objektas žino, kaip jį reikia nupiešti.
### Pavyzdys
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0
    def draw(self, screen):  
        self.food.draw(screen)  
        self.snake.draw(screen) 
#### Abstrakcija naudojama tuo, kad Game klasė tiesiog iškviečia draw() metodą, nesigilindama, kas tiksliai yra piešiama. Kiekvienas objektas žino, kaip jį nupiešti, o žaidimas tik iškviečia bendrą metodą.
## Paveldėjimas
Kas tai?
Paveldėjimas leidžia sukurti naujas klases, kurios paveldi savybes ir metodus iš kitų klasių. Tai leidžia sukurti hierarchijas ir išvengti kodo pasikartojimo.

Kaip tai veikia tavo žaidime?
Mano žaidime klasės Food ir Snake paveldi nuo bendros GameObject klasės. Tai leidžia jiems dalintis bendromis savybėmis (pvz., position) ir metodais, bet kiekviena klasė gali įgyvendinti savo versiją metodų (pvz., draw()).
### Pavyzdys
class GameObject:
    def __init__(self, position):
        self.position = position
    def draw(self, screen):
        raise NotImplementedError("Subclasses must implement this method")

class Food(GameObject):
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)
    def draw(self, screen):
        food_rect = pygame.Rect(OFFSET + self.position.x * cell_size, OFFSET + self.position.y * cell_size, cell_size, cell_size)
        screen.blit(food_surface, food_rect)

class Snake(GameObject):
    def __init__(self):
        super().__init__(Vector2(6, 9))  # Paveldima pozicija iš GameObject klasės
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]
        self.direction = Vector2(1, 0)
#### Paveldėjimas naudojamas per bendrą GameObject klasę, iš kurios paveldi tiek Food, tiek Snake. Tai padeda sumažinti kodo pasikartojimą ir centralizuoti bendrą logiką, pvz., poziciją.
## Encapsuliacija
Kas tai?
Encapsuliacija reiškia, kad objektų duomenys yra paslėpti ir gali būti pasiekiami tik per metodus. Tai padeda valdyti ir saugoti objekto būseną.

Kaip tai veikia tavo žaidime?
Mano žaidime gyvatės kūnas (body) ir pozicija yra encapsuliuoti Snake klasėje. Tai leidžia apsaugoti šiuos duomenis nuo tiesioginio keitimo ir suteikia metodus, per kuriuos galima juos atnaujinti (pvz., per update() metodą).
class Snake:
    def __init__(self):
        self._body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]  # Privatus kūno duomenų saugojimas
    def get_body(self):  # Getter metodas
        return self._body
    def set_direction(self, direction):  # Setter metodas
        self.direction = direction
    def update(self):
        self._body.insert(0, self._body[0] + self.direction)  # Kūno atnaujinimas per metodą
        if not self.add_segment:
            self._body = self._body[:-1]  # Kūnas yra encapsuliuotas
#### Encapsuliacija naudojama gyvatės kūnui ir maisto pozicijai saugoti. Kūnas yra privačiai saugomas kaip _body ir gali būti keičiamas tik per metodus, tokius kaip get_body() ir update().
### Santrauka:
Polimorfizmas naudojamas, nes Food ir Snake turi bendrą draw() metodą, tačiau kiekvienas jų turi savo piešimo logiką.
Abstrakcija leidžia žaidimui nesigilinti į detales, tiesiog iškviečiant bendrą metodą draw().
Paveldėjimas leidžia Food ir Snake paveldėti savybes ir metodus iš GameObject klasės.
Encapsuliacija užtikrina, kad gyvatės kūnas ir pozicija yra paslėpti ir gali būti keičiami tik per metodus.
## Singleton dizaino šablonas
Kas tai?
Singleton dizaino šablonas užtikrina, kad klasė turės tik vieną egzempliorių (objektą) visoje sistemoje, ir suteikia globalų tašką šiam objektui pasiekti.

Kaip jis veikia?
Singleton šablonas apriboja klasės instancijų kūrimą iki vienos ir suteikia būdą gauti tą vieną egzempliorių. Pavyzdžiui, jei žaidime yra tik vienas Game objektas, Singleton užtikrina, kad nesukursi kitos Game klasės instancijos, nes visada dirbsi su tuo pačiu egzemplioriumi.

Kodą pritaikymas
Mano žaidime yra naudojamas Singleton šablonas per GameSingleton klasę. Šis šablonas užtikrina, kad Game klasė turi tik vieną egzempliorių, nepriklausomai nuo to, kiek kartų bandysime sukurti Game objektą.
### Pavyzdys
class GameSingleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GameSingleton, cls).__new__(cls)
        return cls._instance
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.game = Game()
            self.initialized = True
#### Singleton dizaino šablonas buvo pasirinktas norint užtikrinti, kad žaidime bus tik viena Game klasės instancija. Tai naudingas šablonas, nes jis leidžia valdyti žaidimo būseną ir įvykio tvarkymą tik per vieną objektą, taip išvengiant klaidų, kai būtų sukuriama daugiau nei viena Game klasės instancija.
Singleton šablonas čia yra tinkamas, nes mes tikrai nenorime turėti kelių žaidimo egzempliorių vienu metu. Turint tik vieną Game egzempliorių, mes užtikriname, kad žaidimo būsenos ir kiti parametrai bus valdomi vienoje vietoje. Tai padeda lengviau valdyti žaidimo srautą, ypač kai norime stebėti globalią žaidimo būseną (pvz., RUNNING arba STOPPED).
## Kompozicija:
Kompozicija reiškia, kad vienas objektas yra sudarytas iš kitų objektų. Tai rodo stiprų ryšį tarp objektų, ir jei tėvinis objektas sunaikinamas, visi jo sudedamieji objektai taip pat yra sunaikinami.
Mano žaidime Game klasė turi Snake ir Food objektus, ir šie objektai negali egzistuoti be Game objekto, nes jie priklauso žaidimo logikai ir būsenai. Tai yra kompozicija, nes Game klasė sudaro žaidimo logiką, kur Snake ir Food yra būtini komponentai, kuriems veikiant žaidimui.
#### Pavyzdys
class Game:
    def __init__(self):
        self.snake = Snake()  # Kompozicija: Game sudaro Snake
        self.food = Food(self.snake.body)  # Kompozicija: Game sudaro Food
## Agregacija:
Agregacija reiškia silpnesnį ryšį, kai objektas gali priklausyti kitam objektui, tačiau jie gali egzistuoti nepriklausomai. Agregacija leidžia objekto dalims būti naudojamoms daugiau nei vienoje vietoje.
Agregacija naudojama, nes Snake ir Food objektai gali egzistuoti nepriklausomai nuo Game objekto. Pavyzdžiui, galima sukurti Snake objektą be Game, o Game gali užtikrinti, kad objektas būtų naudojamas tinkamu būdu.
### Pavyzdys 
class Snake:
    def __init__(self):
        self.body = [Vector2(6, 9), Vector2(5, 9), Vector2(4, 9)]  # Agregacija: Snake gali egzistuoti nepriklausomai
        self.direction = Vector2(1, 0)

class Food:
    def __init__(self, snake_body):
        self.position = self.generate_random_pos(snake_body)  # Agregacija: Food nepriklauso tiesiogiai nuo Game
### Trumpai
Kompozicija naudojama, nes Game turi Snake ir Food kaip savo sudedamąsias dalis. Jie negali egzistuoti be žaidimo.
Agregacija naudojama, nes Snake ir Food gali egzistuoti nepriklausomai nuo Game, tačiau jie naudojami žaidimo logikoje.
## Funkcija save_score (Rašymas į failą):
ef save_score(score):
    with open("game_results.txt", "a") as file:  # "a" prideda įrašus į failą, jei failas jau egzistuoja
        file.write(f"Score: {score}\n")  # Išsaugome žaidimo taškus į failą
 ## Funkcija load_scores (Skaitymas iš failo):
 def load_scores():
    try:
        with open("game_results.txt", "r") as file:
            scores = file.readlines()  # Skaitome visas eilutes iš failo
            scores = [int(score.strip().split(":")[1]) for score in scores]  # Pašaliname "Score:" ir paverčiame į int
        return scores
    except FileNotFoundError:
        return []  # Jei failas neegzistuoja, grąžiname tuščią sąrašą
## Užkrauti geriausią rezultatą ir išsaugoti (Naudojimas žaidime):Atnaujinsime Game klasę, kad galėčiau užkrauti geriausią rezultatą ir išsaugoti rezultatą žaidimo pabaigoje.
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0
        self.best_score = max(load_scores(), default=0)  # Užkrauname geriausią rezultatą
    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()
    def draw(self, screen):  
        self.food.draw(screen)  
        self.snake.draw(screen)  
    def check_collision_with_food(self):
        if self.snake.body[0] == self.food.position:
            self.food.position = self.food.generate_random_pos(self.snake.body)
            self.snake.add_segment = True
            self.score += 1
            self.snake.eat_sound.play()
    def check_collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over() 
    def check_collision_with_tail(self):
        headless_body = self.snake.body[1:]
        if self.snake.body[0] in headless_body:
            self.game_over()
    def game_over(self):
        save_score(self.score)  # Išsaugome rezultatą į failą
        self.best_score = max(self.best_score, self.score)  # Atnaujiname geriausią rezultatą
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"
        self.score = 0
## Geriausio rezultato rodymas ekrane: Pridėjau funkciją, kad žaidime būtų matomas geriausias rezultatas. Tai bus padaryta naudojant best_score iš Game klasės.
best_score_surface = score_font.render(f"Best Score: {game.best_score}", True, DARK_GREEN)
screen.blit(best_score_surface, (OFFSET - 5, OFFSET + cell_size * number_of_cells + 50))  # Rodyti geriausią rezultatą
### Trumpai
Rašymas į failą (save_score()): Kai žaidimas baigiasi, išsaugomas rezultatas į failą.
Skaitymas iš failo (load_scores()): Užkrauname geriausią rezultatą ir rodomą ekrane.
Geriausio rezultato rodymas: Geriausias rezultatas rodomas žaidimo ekrane.
## Mano pateiktame unittest kode yra šie testai, kurie tikrina įvairias žaidimo funkcijas:
test_save_score
Testuoja, ar teisingai išsaugomas taškų rezultatas į failą.

test_load_scores
Patikrina, ar kelias rezultatų išsaugotas failuose ir teisingai užkraunami.

test_load_scores_empty
Tikrina, ar failas yra tuščias, jei nėra įrašytų taškų.

test_food_position_on_edge
Tikrina, kad maistas nebūtų sugeneruotas ant krašto, kur gyvatė gali susidurti.

test_snake_length_increase
Patikrina, ar gyvatės ilgis padidėja, kai ji suvalgo maistą.

test_game_over_collision_with_wall
Testuoja, ar žaidimas baigiasi, jei gyvatė susiduria su siena.

test_score_increase
Patikrina, ar taškai padidėja po to, kai gyvatė suvalgo maistą.

test_food_generation
Testuoja, kad maistas nesusiduria su gyvate ir visada generuojamas kitoje vietoje.

test_game_start
Patikrina, ar žaidimas prasideda, kai žaidėjas paspaudžia klavišą.

test_game_state_transition
Patikrina, ar žaidimo būsena keičiasi tarp „RUNNING“ ir „STOPPED“.

test_multiple_game_updates
Patikrina, ar žaidimas atnaujinamas kelis kartus ir gyvatė teisingai juda.

test_snake_cannot_turn_180
Testuoja, kad gyvatė negali apsukti savo krypties 180 laipsnių kampu.

test_game_start_and_reset
Patikrina, ar žaidimas prasideda ir baigiasi teisingai po paspaudimo.

test_best_score_persistence
Tikrina, ar geriausias rezultatas išsaugomas ir užkraunamas teisingai.
### Programa tenkina PEP8 style guidelines.
## Rezultatai:
Sukūriau unit testus, užtikrinančius žaidimo funkcionalumą (pvz., gyvatės ilgio padidėjimas ir žaidimo pabaiga).
Įdėjau vaizdą į maistą ir užtikrinau, kad jis nesikerta su gyvatės kūnu.
Susidūriau su iššūkiais, ypač dėl judėjimo apribojimų, kad gyvatė negalėtų judėti atgal.
Testavau žaidimą su įvairiais žaidėjų įvedimais.
##Išvados:
Sukūriau funkcinį žaidimą, kuriame gyvatė juda ir valgo maistą, taip pat pasibaigia, kai susiduria su siena ar savo kūnu.
Sukurtas taškų sistemos ir rezultatai, kuriuos galima išsaugoti ir užkrauti naudojant failus.
Programoje įdiegti pagrindiniai žaidimo mechanizmai, tokie kaip maisto generavimas ir gyvatės ilgio didinimas.
### Ateityje būtų galima pridėti įvairių lygių, sudėtingumo lygio variantų ir vizualinių patobulinimų, kad žaidimas būtų dar įdomesnis ir interaktyvesnis.
