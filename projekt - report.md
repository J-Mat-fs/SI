
# 1. Řídící systém robotického manipulátoru
Autor: Jan Matouš 

Předmět: Softwarové inženýrství

Akademický rok 2025/2026

Vedoucí předmětu: Ing. Pavel Steinbauer, Ph.D. a Ing. Jan Pelikán, Ph.D.

<div align="center">
  <hr>
</div>




## 1.1.Vision and Scope

<div align="center">
  <hr>
</div>


### Vision

<div align="justify">
Cílem projektu je návrh řídícího systému pro 3-osý pick and place manipulátor typu Gantry, který automatizuje manipulaci s výrobním materiálem v prostředí poloautonomní výrobní linky. Systém zajistí nepřetržitost výroby, vysokou opakovatelnost a eliminaci rizika práce s agresivní chemií. 
</div>


<div align="center">
  <img src="images/img_1.3.png" alt="Robotický manipulátor" width="220">
  <br>
  <i>obr. 1.1 - Robotický manipulátor</i>
</div>

<br>


<div align="center">
  <img src="images/img_1.2.png" alt="CAD model robotického manipulátoru" width="510">
  <br>
  <i>obr. 1.2 - CAD model robotického manipulátoru</i>
</div>


### Stakeholders
1. **Operátor výroby** - interaguje s manipulátorem, kontroluje správnost chodu stroje, ovládá kličové ochranné prvky (stop tlačítko)
2. **Servisní technik** - dohlíží nad správným a funkčím stavem manipulátoru (diagnostika, kalibrace senzorů)
3. **Koordniátor výroby** - monitoring efektivity linky, plánování kapacit, směn
4. **Bezpečnostní technik** - soulad s bezpečnostními normami ISO, validace fungování 
5. **Vývojář řídícího systému** - nasazení a aktualizace firmware/software
  
### Klíčové scénáře


1. **Homing** - Synchronizace fyzické polohy motorů s logickým nulovým bodem softwaru pro definování souřadného systému.
2. **Pohyb na souřadnice (Point-to-Point)** - Přesun Tool Center Pointu (TCP) na kokntréntí zadané souřadnice (X,Y,Z) v rámci pracovního prostoru
3. **Úchop desky** - Sestup osy Z k polotovaru, aktivace gripperu a ověření dosažení úchopu skrz koncový spínač
4. **Uvolnění desky** - Přesné uložení desky do slotu a uvolnění úchopu gripperu
5. **Nouzové brzdění** - Prioritní přerušení všech probíhajícíh pohybů a odpojení výkonu pohonů při detekci narušení bezpečnosti
6. **Monitoring stavu** - Periodické odesílání informací o aktuální poloze, rychlosti do nadřazeného systému 


### Odhad rizik
1. **Koroze** - vlivem chemických výparů může docházet k poškození senzorů a dalších kritických součástek
2. **Kolize** - mechanické poškození vlivem chyby trajektorie/souřadnicového systému 
3. **Selhání manipulace** - vlivem nepřesnosti výroby, nemožnost manipulovat (variabilita v rozměrech destiček, další deformace)

### Plán ověření
"Úspěchem nazveme stav, kdy dojde k autonomnímu vykonání 30 cycklů bez chyby úchopu a v případě otevření klece dojde k zastavení manipulátoru do 500 ms."
s
<div style="page-break-after: always;"></div>


### Kontextový diagram
<div align="center">
  <img src="images/img_1.4.png" alt="Kontextový diagram" width="680">
  <br>
  <i>obr. 1.3 - Kontextový diagram</i>
</div>

### Seznam podnětů z okolí 

1. **Uchop desku** - v X,Y,Z koordinací předá ROS síť požadavek o vyzvednutí desky
2. **Bezpečnostní zastavení** - vlivem otevření klece dojde k poslání signálu k zastavení manipulátoru
3. **Home sekvence** - signál k inicializaci polohy manipulátoru
4. **Neuchopení desky** - signál koncových čidel o neuchopení deksy


### Seznam rolí a aktérů
- **Operátor** - primární aktér - Účastní se běžného provozu, spouští chod a provádí vizuální kontrolu linky jak přes panel, tak přes vizuální kontrolu

- **Servisní technik** - technická role - Údržb mechaniky, kalibrace os a dignostiky softwarovcýh chyb
- **Bezpečnostní technik** - bezpečností role - Zodpovíva za schálení bezpečnostních limitů, konfiguraci stop stavu a revizi klece
- **Systémový administrátor** - IT role - Správa síťové infrastruktury a verzování řídícího software
  
### Základní omezení

Technické i legislativní omezení:
  
- **Komunikační standardy** - Komunikace mezi moduly probíhá přes standardy ROS2 zpráv
  
- **Software safety** - V případě výpadku komunikace nebo překročení mezních hodnot (překročení rychlosti nad xxx mm/s) software autonomně vyvolá stop stav bez zásahu nadřazené sítě.
  
- **Reálný čas** - Řídící smyčka pro plánování trajektorie běží s pevnou periodou pro zaručení stability pohybu 
  
- **Legislativní normy** - Návrh SW architektury musí odpovídat požadavkům normy ISO 10218 na spolehlivost logických bezpečnostních funkcí. Kód musí být verzován (Git) a dokumentován pro potřeby budoucí certifikace.


### Plán práce týmu a rozdělení rolí

<div align="center">


<div align="center">

| Fáze projektu | Odpovědná role | Výstup (Artefakt) |
| :--- | :--- | :--- |
| **Analýza a vize** | Systémový architekt | Vision & Scope dokumentace, C4 diagram |
| **Specifikace požadavků** | Requirements Engineer | Seznam FR a NFR, Use-case model |
| **Návrh a modelování** | SW Inženýr | Doménový model, stavové automaty |
| **Ověřování a testy** | V&V Specialista | Testovací případy, V&V matice |
| **Prototypování** | Vývojář | ROS2 simulace, kód klíčové funkce |

<br>

</div>
<i>tab. 1.1 - Rozdělení rolí v týmu</i>
</div>
<br>


<div align="center">
  <hr>
</div>

## 1.2. Requirements Specification

<div align="center">
  <hr>
</div>



Cílem je definování systému tak, aby byl jednoznačný, testovatelný a zaměřený na softwarové řízení 3-osého manipulátoru.

### Usecase model
Model se zaměřuje na elementární (atomické) operace systému, ze kterých se skládají komplexní procesy.

**Seznam elementárních případů užití:**

  - **UC_01**: Inicializace a homing – uvedení systému do výchozího stavu, kalibrace os a určení referenční polohy robota.

- **UC_02**: Přenesení desky – hlavní pracovní scénář systému, při kterém robot přesune desku ze zdrojové pozice na cílovou pozici.

- **UC_03**: Sledování stavu a telemetrie – průběžné zobrazování stavu robota, aktuální pozice, chybových hlášení a provozních dat.

- **UC_04**: Nouzové zastavení robota – prioritní bezpečnostní zásah, který přeruší pohyb robota a uvede systém do bezpečného stavu.

- **UC_05**: Servisní ovládání pohybu – ruční nebo servisní řízení pohybu robota pro účely testování, údržby nebo seřízení.

-  **UC_06**: Kalibrace systému – nastavení a ověření kalibračních parametrů systému, například rozsahu pohybu, referenčních bodů a přesnosti polohování.

-  **UC_07**: Diagnostika poruchy – zjištění příčiny chybového stavu pomocí stavových informací, telemetrie a logů systému.

-  **UC_08**: Přijetí pohybového příkazu – příjem požadavku na pohyb z nadřazeného systému nebo ROS2 rozhraní.

-  **UC_09**: Odeslání stavu a telemetrie – předání aktuálních stavových dat, provozních hodnot a diagnostických informací do ROS2 nebo nadřazeného systému.
 
<div align="center">
  <img src="images/img_1.5.png" alt="Usecase diagram" width="680">
  <br>
  <i>obr. 1.4 - Usecase diagram</i>
</div>


#### Seznam požadavků (FR & NFR)


<div align="center">

| ID         | Use case ID                    | Požadavek                                                                                                                 | Priorita | Zdroj                | Verifikace    | Evidence                                             |
| :--------- | :----------------------------- | :------------------------------------------------------------------------------------------------------------------------ | :------- | :------------------- | :------------ | :--------------------------------------------------- |
| **FR-01**  | **UC_01, UC_06**               | Systém musí umožnit automatickou kalibraci všech 3 os (Homing)                                                            | Vysoká   | Servisní technik     | Test          | Konzole ROS2 (zpráva)                                |
| **FR-02**  | **UC_10, UC_02**               | Pohyb (P2P): Systém musí umožnit přesun TCP na definované souřadnice X, Y, Z s přesností ± 0.1 mm.                        | Vysoká   | Provozní scénář      | Demonstrace   | Porovnání cílových a aktuálních souřadnic            |
| **FR-03**  | **UC_12, UC_02**               | Systém musí aktivovat a detekovat úspěšný úchop destičky pomocí koncového senzoru                                         | Vysoká   | Provozní scénář      | Test          | Změna v provozním logu u gripper_status              |
| **FR-04**  | **UC_13, UC_02**               | Systém deaktivuje gripper a potvrdí uvolnění gripperu před odjezdem osy Z                                                 | Vysoká   | Provozní scénář      | Test          | Log událostí a následná změna Z souřadnic            |
| **FR-05**  | **UC_05**                      | Systém musí umožnit posuv os v servisním režimu                                                                           | Nízká    | Servisní technik     | Test          | Záznam o přijetí příkazu z ovladače (panel)          |
| **FR-06**  | **UC_11, UC_16, UC_10**        | Systém musí softwarově kontrolovat mechanické limity pracovního prostoru a odmítnout pohyb mimo povolený rozsah.          | Vysoká   | Bezpečnostní technik | Test          | Chybová hláška v terminálu při pohybu mimo rozsah    |
| **FR-07**  | **UC_03, UC_09, UC_14**        | Ukládání systémových dat o dokončených cyklech, chybových hlášení a stavu senzorů do logu a odesílat přes ROS2 v realtimu | Střední  | Záznám výsledků      | Analýza logu  | soubor .log na disku s historií dat                  |
| **NFR-01** | **UC_04, UC_17**               | Systém musí přejít do bezpečného stop-stavu při detekci poruchy/červeného tlačítka do 500 ms (Failsafe).                  | Kritická | Bezpečnostní technik | Měření        | Časový rozdíl v logu mezi chybou a zastavením motoru |
| **NFR-02** | **UC_02, UC_03, UC_07, UC_14** | Provozuschopnost systému víc než 95 % plánované výrobní doby za období jednoho týdně                                      | Vysoká   | Koordnitánor výroby  | Analýza logu  | Report z diagnostického modulu                       |
| **NFR-03** | **UC_08, UC_09**               | Síťová komunikace ROS2 izolována od veřejné sítě a ochráněna od neoprávných příkazů                                       | Vysoká   | Vývojář              | Inspekce sítě | Konfigurační soubor firewallu                        |

<br>
<i>tab. 1.2 - Tabulka se seznamem požadavků (FR & NFR)</i>
</div>
<br>






**Požadavky na rozhraní**

- **SW rozhraní** - ROS2 API
- **HW rozhraníí** - Signál z koncového senzoru, řízení přes USB/CAN
- **Časování** - Perioda řídící smyčky 10 ms


**Stop stavy a chování při poruchách**

- **Failsafe režim** - při ztrátě komunika s nadřazeným systémem musí robot dokončit pohyb do neutrální polohy nebo okamžitě zastavit
- **Emergency STOP** - Fyzické odpojení napájení motorů při narušení klece




#### Akceptační kritéria rozhraní

<div align = "center">

||Detekce neúspěšného úchopu - navázáno na FR-03|
| :--- | :--- | 
| **Given** | Robot se nachází na zásobníkem a spustil uchopovací cyklus
| **When** | Koncový senzor nahlásí zmáčknutí koncového spínače indikující chybějící polotovar
| **Then** | Robot přeruší cyklus, zvedne osu Z do bezpečné výšky a aktivuje alarm |
</div>

<div align = "center">
<i>tab. 1.3 - Akceptační kritéria rozhraní pro FR-03 </i>
<br>
<br>
</div>


<div align = "center">

||Reakce na nouzové zastavení - navázáno na NRF-01|
| :--- | :--- | 
| **Given** | Robot provádí pohyb v libovolné ose
| **When** | Dojde k rozpojení bezpečnostního okruhu (tlačítko, otevření klece)
| **Then** | Systém odpojí pohony a veškerý pohyb se zastaví do 500 ms |
| **Then** | Systém odpojí pohony a veškerý pohyb se zastaví do 500 ms |

<i>tab. 1.4 - Akceptační kritéria rozhraní - pro NRF-01 </i>
</div>
<br>

<div style="page-break-after: always;"></div>


<div align="center">
  <hr>
</div>

## 1.3. Model system

<div align="center">
  <hr>
</div>



Specifikujeme vnitřní strukturu a dynamické chování řídícího systému pro Gantry robot. Modely definují rozhraní mezi jednotlivámi softwarowými moduly a jejich interakci s okolím.

**Doménový model**

Doménový model popisuje hlavní pojmy problémové domény a jejich vzájemné vztahy, nikoliv detailní implementaci programu. V tomto modelu je centrální entitou Gantry Robot, který nese základní stavové informace systému, například status, is_initialized a is_homed. Na robota jsou navázány tři osy typu Osa, které obsahují informace o své identifikaci, cílové a aktuální pozici, limitech a stavu pohybu. Model dále obsahuje třídu Pose, která reprezentuje prostorovou polohu pomocí souřadnic x, y, z, třídu Gripper pro popis stavu uchopovacího mechanismu, Koncový senzor pro informaci o stavu senzoru a Log pro uchování časových záznamů a událostí systému. Vztahy mezi třídami ukazují, že robot je složen z několika os, spolupracuje s gripperem a senzorem, používá cílové polohy a vytváří provozní logy. Model tedy slouží jako přehled klíčových datových objektů, se kterými systém pracuje při řízení pohybu, uchopení desky a diagnostice.


<div align="center">
  <img src="images/img_1.6.png" alt="Doménový model" width="730">
  <br>
  <i>obr. 1.5 - Doménový model</i>
</div>

<div style="page-break-after: always;"></div>

**Dynamický model: Stavový automat**

Stavový automat popisuje dynamické chování gantry robota od zapnutí systému přes inicializaci, připravenost a pracovní cyklus až po poruchový stav. Po spuštění systém přechází ze stavu START / POWER OFF do INIT / HOMING, kde probíhá spuštění homingu. Po nalezení nulové polohy a odeslání stavu do ROS2 přechází robot do stavu READY. Odtud může po validaci souřadnic a výpočtu trajektorie přejít do pohybu, následně do stavů Picking a Placing, které reprezentují uchopení a uložení desky. Přechody jsou popsány pomocí trojice T/P/A, tedy trigger, podmínka a akce, což zpřesňuje, kdy je přechod povolen a co se při něm vykoná. Klíčovým bezpečnostním prvkem je stav Fault, do kterého systém přechází při selhání kalibrace, ztrátě úchopu, mechanickém odporu, bezpečnostní události nebo chybě úchopu. Tento stav zajišťuje zastavení motorů, vypnutí gripperu a upozornění obsluhy, čímž odděluje běžný pracovní cyklus od poruchového chování systému.
<br>

<br>

<div align="center">
  <img src="images/img_1.7.png" alt="Doménový model" width="700">
  <br>
  <i>obr. 1.6 - Dynamický model </i>
</div>

<div style="page-break-after: always;"></div>


**Procesní model - Data Flow Diagram**

Diagram datových toků popisuje systém jako centrální proces, který komunikuje s okolními terminátory: uživatelem, kamerou, koncovým senzorem a gantry robotem. Kontextová část ukazuje základní vstupy a výstupy systému, zejména datové a řídicí vazby mezi systémem a robotem, kamerou, senzorem a uživatelem. Podrobnější rozpad systému obsahuje dílčí procesy pro vyžádání dat z ROS2 databáze, ověření dosažitelnosti souřadnic, přejetí na zadané souřadnice zásobníku, aktivaci gripperu, přejetí na bezpečnou polohu a odeslání dat o úchopu do databáze. Diagram zároveň znázorňuje, že kamera poskytuje data pro optickou kontrolu, koncový senzor dodává signál o stavu úchopu, uživatel zadává příkazy přes UI a gantry robot vykonává pohybové a manipulační akce.


<div align="center">
  <img src="images/img_1.8.png" alt="Data Flow Diagram" width="700">
  <br>
  <i>obr. 1.7 - Data Flow Diagram </i>
</div>


<div style="page-break-after: always;"></div>


**Model rozhraní a nasazení**

Model popisující fyzické a logické rozmístění softwarových komponent na hardwarových uzlech. Architektura je dekomponována na vnitřní podstruktury samotného robotického systému a vnější entity, jako například "Factory Control Server", se kterým systém komunikuje.

Vnitřní architektura systému je tvořena dvěma hlavními výpočetními uzly. Master PC slouží jako centrální řídicí jednotka, která zprostředkovává komunikaci s vnějším světem, zajišťuje vizualizaci dat a plánuje úkony na nejvyšší úrovni. Skrze lokální síť (Ethernet) je tento uzel propojen s řídicí jednotkou robota (Robot Control Unit), která funguje jako real-time vykonavatel. Právě zde běží hlavní stavový automat a řídicí logika, která již přímo ovládá koncovou hardwarovou vrstvu stroje – tedy samotné pohony, ventily a senzory.

Toto fyzické i logické oddělení vrstev umožňuje bezpečnou integraci robota do širšího továrního ekosystému. Veškerá komunikace s okolím probíhá výhradně přes Master PC, které přijímá výrobní úlohy z nadřazeného Factory Control Serveru a reportuje aktuální stav vzdálenému uživateli přes zabezpečené síťové rozhraní. Systém zároveň průběžně odesílá provozní data na externí Logging Server, čímž je zajištěna spolehlivá archivace telemetrie, aniž by se zbytečně zatěžoval výpočetní výkon samotného řízení robota.

<div align="center">
  <img src="images/img_1.9.png" alt="Model rozhraní a nasazení" width="700">
  <br>
  <i>obr. 1.8 - Model rozhraní a nasazení</i>
</div>


<div style="page-break-after: always;"></div>

<div align="center">
  <hr>
</div>




## 1.4. Verification and Validation

<div align="center">
  <hr>
</div>



**V&V Matice - Traceability**

Pro vybrané požadavky z kapitoly 1.2

<div align="center" >

| ID | Požadavek | Metoda ověření | Specifikace ověření | Test Case ID |
| :--- | :--- | :--- | :--- | :--- |
|FR-01 | Homing | Zátěžový test | 10x po sobě jdoucí úspěšná kalibrace z náhodných počátečních poloh os | TC-01
FR-02 | Přesnost pohybu | Měření | Najetí na 3 náhodné body v 5 opakováních, výpočet odchylky | TC-02
|FR-03| Úchop | Test | 20 cyklů úchopu a zdvihu bez pádu polotovaru nebo falešné detekce uchopení | TC-03
|FR-06| Soft Limity | Negativní test | 5 pokusů o zadání souřadníc mimo pracovní prostor přes ROS2 | TC-04
|NFR-01| Stop stav | Časová analýza | 10x simulace chyby, změření času od logu události po zastavení příkazu motorů | TC-05
|NFR-02|   Uptime 95 % | Test | 24hodinový běh v simulovaném stress-test cyklu |  TC-06

<i>tab. 1.5 - V&V Matice - Traceability</i>
</div>

<br>

**Testovací strategie po úrovních**

Pro omezení fyzických škod způsobené chybami softwaru, přistoupíme k testingu pomocí víceúrovňové simulace, ve které postupně zvyšujeme množinu celku zapojení robota.
Pro omezení fyzických škod způsobené chybami softwaru, přistoupíme k testingu pomocí víceúrovňové simulace, ve které postupně zvyšujeme množinu celku zapojení robota.

1. **Unit Testing** - Testování jednotlivých funkcí (výpočet inverzní kinematiky, parsování ROS2 zpráv) bez nutnosti připojeného HW
2. **Unit Testing** - Testování jednotlivých funkcí (výpočet inverzní kinematiky, parsování ROS2 zpráv) bez nutnosti připojeného HW
   
3. **Software in the Loop** - Testování kompletního kódu v simulovaném prostředí (například Gazebo), kde pozorujeme chování robota ve virtuálním prostředí.
4. **Hardware in the Loop** - Řídící algoritmus běží na Master PC, ale je připojem k realným driverům motorů bez mechanické zátěže pro otestování komunikace.
5. **System Inert Fluid Testing** - První testování stroje v prostředí lázní plněné inertní kapalinou (vodou)
6. **System Stress Testing** - Vědomé přetězování softwarové logiky v bezpečném prostředí (bez chemie) 
7. **System Endtesting**  - Finální testování kompletního stroje v chemickém provozu 
8. **Software in the Loop** - Testování kompletního kódu v simulovaném prostředí (například Gazebo), kde pozorujeme chování robota ve virtuálním prostředí.
9. **Hardware in the Loop** - Řídící algoritmus běží na Master PC, ale je připojem k realným driverům motorů bez mechanické zátěže pro otestování komunikace.
10. **System Inert Fluid Testing** - První testování stroje v prostředí lázní plněné inertní kapalinou (vodou)
11. **System Stress Testing** - Vědomé přetězování softwarové logiky v bezpečném prostředí (bez chemie) 
12. **System Endtesting**  - Finální testování kompletního stroje v chemickém provozu 

<br>
<br>

**Test cases**

<div align="center">

| ID | Název testu | Vstupní podmínka | Očekávaný výsledek | Pass/Fail kritérium |
| :--- | :--- | :--- | :--- | :--- |
|TC-01 | **Homing Sequence** | 10x - Start systému, osy v náhodných polohách | Robot najde 3 koncové spínače a vynuluje souřadnice | isHomed == True a rozptyl nalezených nulových bodů <0,05 mm| 
|TC-02 | **P2P Accuracy** | 5x - Příkaz pohybu na bod1, bod2, bod3  | Robot se zastaví na pozici | Max. odchylka mezi cílovou a skutečnou polohou v každém kroku <0.1 mm|
|TC-03a| **Pick Succes** | Polotovar v zásobníku, příkaz Pick | Koncový senzor sepne a změní stav na Gripped | is_gripped = True |
|TC-03b| **Pic Failure (empty)** | Zásobník prázdný, příkaz Pick | Po 2s timeoutu, systém nahlásí chybu a přejede do bezpečné polohy | Stav - Fault, zprává ROS2 operátorovi |
|TC-04| **Soft Limit Breach** | Pokus o pohyb na "přeslimitní" souřadnice| Software odmítne vykonat pohyb dřív, než se motory pohnou| Chybová hláška v konzoli|
|TC-05| **Emergency Stop**| Stisk E-stop tlačítka během pohybu | Okamžité zastavení všech os do 500 ms| Časový rozdíl v logu t<500 ms |
|TC-06| **24 hod - Zátěžový Test**| Skript s nekonečnou frontou náhodných, validních souřadnic v pracovním prostoru | Systém vykoná cykly bez pádu uzlů nebo kritického nárustu spotřeby | Systém běží minimálně 95 % testovaného času bez nutnosti restartu softwaru v simulovaném prostředí - SIF |
|TC-01 | **Homing Sequence** | 10x - Start systému, osy v náhodných polohách | Robot najde 3 koncové spínače a vynuluje souřadnice | isHomed == True a rozptyl nalezených nulových bodů <0,05 mm| 
|TC-02 | **P2P Accuracy** | 5x - Příkaz pohybu na bod1, bod2, bod3  | Robot se zastaví na pozici | Max. odchylka mezi cílovou a skutečnou polohou v každém kroku <0.1 mm|
|TC-03a| **Pick Succes** | Polotovar v zásobníku, příkaz Pick | Koncový senzor sepne a změní stav na Gripped | is_gripped = True |
|TC-03b| **Pic Failure (empty)** | Zásobník prázdný, příkaz Pick | Po 2s timeoutu, systém nahlásí chybu a přejede do bezpečné polohy | Stav - Fault, zprává ROS2 operátorovi |
|TC-04| **Soft Limit Breach** | Pokus o pohyb na "přeslimitní" souřadnice| Software odmítne vykonat pohyb dřív, než se motory pohnou| Chybová hláška v konzoli|
|TC-05| **Emergency Stop**| Stisk E-stop tlačítka během pohybu | Okamžité zastavení všech os do 500 ms| Časový rozdíl v logu t<500 ms |
|TC-06| **24 hod - Zátěžový Test**| Skript s nekonečnou frontou náhodných, validních souřadnic v pracovním prostoru | Systém vykoná cykly bez pádu uzlů nebo kritického nárustu spotřeby | Systém běží minimálně 95 % testovaného času bez nutnosti restartu softwaru v simulovaném prostředí - SIF |


<br>
<i>tab. 1.6 - Tabulka Test Cases </i>
</div>

<br>


**Plán záznamu výsledků**

Pro splnění požadavků na evidenci, použijeme tyto nástroje:

 - **ROS Bags** - Záznam všech dat protékajících systémem (témata, zprávy, časy)
 - **System Logs** - Textové záznamy o stavových přechodech
 - **Telemetry values** - CSV exporty z dashbordu pro porovnání přesnosti pohybu
 - **Screenshots** - Snímky z RViz vizualizace pro potvrzení shody modelu s realitou.
 - **ROS Bags** - Záznam všech dat protékajících systémem (témata, zprávy, časy)
 - **System Logs** - Textové záznamy o stavových přechodech
 - **Telemetry values** - CSV exporty z dashbordu pro porovnání přesnosti pohybu
 - **Screenshots** - Snímky z RViz vizualizace pro potvrzení shody modelu s realitou.

<div style="page-break-after: always;"></div>





<div align="center">
  <hr>
</div>

## 1.5. Prototype

<div align="center">
</div>
<div align="center">
  <hr>
</div>

V naprogramovaném prototypu je ukázán základní demonstrátor řídící logiky 3 osého gantry manipulátoru. Aplikace umožňuje inicializaci systému, provedení homingu, zadání cílové polohy TCP v osách X, Y, Z a postupné krokování pohybu po plánované trajektorii. Součástí je také kontrola pracovního prostoru, stavový model robota, nouzové zastavení, reset poruchového stavu a průběžný záznam událostí do logu.

Prototyp také simuluje základní pick and place scénář. Uživatel může nastavit přítomnost destičky v zásobníku, spustit sekvenci uchopení nebo položení a sledovat stav gripperu, uchopení destičky a aktuální polohu TCP. Vizualizace v aplikaci zobrazuje pracovní prostor manipulátoru, aktuální pozici, cílovou pozici, plánovanou i vykonanou trajektorii. 

Cílem simulace je ověření, že specifikované stavy, požadavky a chybové scénáře dávají smysl a jsou testovatelné.

<div align="center">
  <img src="images/img_1.10.png" alt="Prototyp stavového automatu Gantry robotu" width="700">
  <br>
  <i>obr. 1.9 - Prototyp stavového automatu Gantry robotu</i>
</div>