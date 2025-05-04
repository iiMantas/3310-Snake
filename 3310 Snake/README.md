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
![image](https://github.com/user-attachments/assets/1552b21b-29e3-486d-b865-099cbc65330f)

#### Polimorfizmas naudojamas, nes Food ir Snake klasės turi tą patį draw() metodą, tačiau jis yra įgyvendintas skirtingai kiekvienoje klasėje. Game klasė tiesiog iškviečia draw() metodą, nepriklausomai nuo objekto tipo.
## Abstrakcija

Kas tai?

Abstrakcija slepia sudėtingą detalių logiką ir leidžia dirbti su aukštesnio lygio metodais.

Kaip tai veikia tavo žaidime?

Game klasė nesirūpina tuo, kaip tiksliai piešiami maistas ar gyvatė. Ji tiesiog iškviečia draw() metodą, o kuris metodas bus iškviestas priklauso nuo objekto tipo (Snake arba Food). Tai yra abstrakcija, nes žaidimas nesigilina į detales, tiesiog pasikliauja, kad kiekvienas objektas žino, kaip jį reikia nupiešti.

### Pavyzdys
![image](https://github.com/user-attachments/assets/f87e2c66-3d9c-4eb1-8451-6173dddc92b9)

#### Abstrakcija naudojama tuo, kad Game klasė tiesiog iškviečia draw() metodą, nesigilindama, kas tiksliai yra piešiama. Kiekvienas objektas žino, kaip jį nupiešti, o žaidimas tik iškviečia bendrą metodą.
## Paveldėjimas

Kas tai?

Paveldėjimas leidžia sukurti naujas klases, kurios paveldi savybes ir metodus iš kitų klasių. Tai leidžia sukurti hierarchijas ir išvengti kodo pasikartojimo.

Kaip tai veikia tavo žaidime?

Mano žaidime klasės Food ir Snake paveldi nuo bendros GameObject klasės. Tai leidžia jiems dalintis bendromis savybėmis (pvz., position) ir metodais, bet kiekviena klasė gali įgyvendinti savo versiją metodų (pvz., draw()).

### Pavyzdys
![image](https://github.com/user-attachments/assets/68407650-6166-4766-acb1-d10edfeec2a3)

#### Paveldėjimas naudojamas per bendrą GameObject klasę, iš kurios paveldi tiek Food, tiek Snake. Tai padeda sumažinti kodo pasikartojimą ir centralizuoti bendrą logiką, pvz., poziciją.
## Encapsuliacija

Kas tai?

Encapsuliacija reiškia, kad objektų duomenys yra paslėpti ir gali būti pasiekiami tik per metodus. Tai padeda valdyti ir saugoti objekto būseną.

Kaip tai veikia tavo žaidime?

Mano žaidime gyvatės kūnas (body) ir pozicija yra encapsuliuoti Snake klasėje. Tai leidžia apsaugoti šiuos duomenis nuo tiesioginio keitimo ir suteikia metodus, per kuriuos galima juos atnaujinti (pvz., per update() metodą).
### Pavyzdys
![image](https://github.com/user-attachments/assets/7a27b6cc-70a3-4385-b786-355f458df5e2)

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
![image](https://github.com/user-attachments/assets/282da24d-9e6c-4a7e-9aee-b5235c514ce5)

#### Singleton dizaino šablonas buvo pasirinktas norint užtikrinti, kad žaidime bus tik viena Game klasės instancija. Tai naudingas šablonas, nes jis leidžia valdyti žaidimo būseną ir įvykio tvarkymą tik per vieną objektą, taip išvengiant klaidų, kai būtų sukuriama daugiau nei viena Game klasės instancija.

Singleton šablonas čia yra tinkamas, nes mes tikrai nenorime turėti kelių žaidimo egzempliorių vienu metu. Turint tik vieną Game egzempliorių, mes užtikriname, kad žaidimo būsenos ir kiti parametrai bus valdomi vienoje vietoje. Tai padeda lengviau valdyti žaidimo srautą, ypač kai norime stebėti globalią žaidimo būseną (pvz., RUNNING arba STOPPED).
## Kompozicija:

Kompozicija reiškia, kad vienas objektas yra sudarytas iš kitų objektų. Tai rodo stiprų ryšį tarp objektų, ir jei tėvinis objektas sunaikinamas, visi jo sudedamieji objektai taip pat yra sunaikinami.

Mano žaidime Game klasė turi Snake ir Food objektus, ir šie objektai negali egzistuoti be Game objekto, nes jie priklauso žaidimo logikai ir būsenai. Tai yra kompozicija, nes Game klasė sudaro žaidimo logiką, kur Snake ir Food yra būtini komponentai, kuriems veikiant žaidimui.

#### Pavyzdys
![image](https://github.com/user-attachments/assets/725780df-fa7a-42e6-a52e-b83f45fbea70)

## Agregacija:

Agregacija reiškia silpnesnį ryšį, kai objektas gali priklausyti kitam objektui, tačiau jie gali egzistuoti nepriklausomai. Agregacija leidžia objekto dalims būti naudojamoms daugiau nei vienoje vietoje.

Agregacija naudojama, nes Snake ir Food objektai gali egzistuoti nepriklausomai nuo Game objekto. Pavyzdžiui, galima sukurti Snake objektą be Game, o Game gali užtikrinti, kad objektas būtų naudojamas tinkamu būdu.

### Pavyzdys 
![image](https://github.com/user-attachments/assets/24834d2a-071f-49c3-9a7b-2fa8e7975d8b)

### Trumpai

Kompozicija naudojama, nes Game turi Snake ir Food kaip savo sudedamąsias dalis. Jie negali egzistuoti be žaidimo.

Agregacija naudojama, nes Snake ir Food gali egzistuoti nepriklausomai nuo Game, tačiau jie naudojami žaidimo logikoje.

## Funkcija save_score (Rašymas į failą):
![image](https://github.com/user-attachments/assets/2674c9cf-f058-4a8a-b3ec-7d7f36a1894e)

 ## Funkcija load_scores (Skaitymas iš failo):
 ![image](https://github.com/user-attachments/assets/cf49ac93-b7c1-42cc-a822-1eda4a9ea2b2)

## Užkrauti geriausią rezultatą ir išsaugoti: Atnaujinsime Game klasę, kad galėčiau užkrauti geriausią rezultatą ir išsaugoti rezultatą žaidimo pabaigoje.
![image](https://github.com/user-attachments/assets/c3a83ac1-29eb-401c-b538-23fb3685b1eb)

## Geriausio rezultato rodymas ekrane: Pridėjau funkciją, kad žaidime būtų matomas geriausias rezultatas. Tai bus padaryta naudojant best_score iš Game klasės.
![image](https://github.com/user-attachments/assets/17153ed5-3c99-479e-86bb-07beb9779c8a)

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
