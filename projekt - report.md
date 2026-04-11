
# 1. Řídící systém robotického manipulátoru
Autor: Jan Matouš 

Předmět: Softwarové inženýrství

Akademický rok 2025/2026

Vedoucí předmětu: Ing. Pavel Steinbauer, Ph.D. a Ing. Jan Pelikán, Ph.D.
----------------------------------------------------


## 1.1.Vision and Scope


  ### Vision

<div align="justify">
Cílem projektu je návrh řídícího systému pro 3-osý pick and place manipulátor typu Gantry, který automatizuje manipulaci s výrobním materiálem v prostředí poloautonomní výrobní linky. Systém zajistí nepřetržitost výroby, vysokou opakovatelnost a eliminaci rizika práce s agresivní chemií. 
</div>


<div align="center">
  <img src="images/img_1.3.png" alt="Robotický manipulátor" width="280">
  <br>
  <i>obr. 1.1 - Robotický manipulátor</i>
</div>



<div align="center">
  <img src="images/img_1.2.png" alt="CAD model robotického manipulátoru" width="400">
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
| Fáze projektu | Odpovědná role | Výstup (Artefakt) |
| :--- | :--- | :--- |
| **Analýza a vize** | Systémový architekt | Vision & Scope dokumentace, C4 diagram |
| **Specifikace požadavků** | Requirements Engineer | Seznam FR a NFR, Use-case model |
| **Návrh a modelování** | SW Inženýr | Doménový model, stavové automaty |
| **Ověřování a testy** | V&V Specialista | Testovací případy, V&V matice |
| **Prototypování** | Vývojář | ROS2 simulace, kód klíčové funkce |



## 1.2. Requirements Specification

Cílem je definování systému tak, aby byl jednoznačný, testovatelný a zaměřený na softwarové řízení 3-osého manipulátoru.

### Usecase model
Model se zaměřuje na elementární (atomické) operace systému, ze kterých se skládají komplexní procesy.

**Seznam elementárních případů užití:**

  - **UC_01**: Inicializace (Homing) – kalibrace os.

- **UC_02**: Pohyb na souřadnice – nízkoúrovňové řízení trajektorie.

- **UC_03**: Úchop polotovaru (Pick) – aktivace a kontrola vakua.

- **UC_04**: Uvolnění polotovaru (Place) – deaktivace vakua a potvrzení.

- **UC_05**: Nouzové zastavení – prioritní přerušení SW smyčky.

 
<div align="center">
  <img src="images/img_1.5.png" alt="Usecase diagram" width="680">
  <br>
  <i>obr. 1.4 - Usecase diagram</i>
</div>




#### Seznam požadavků (FR & NFR)
| ID | Požadavek | Priorita | Zdroj | Verifikace | Evidence |
| :--- | :--- | :--- | :--- |:--- | :--- |
| **FR-01** | Systém musí umožnit automatickou kalibraci všech 3 os (Homing) | Vysoká | Servisní technik | Test | Konzole ROS2 (zpráva)
| **FR-02** | Pohyb (P2P): Systém musí umožnit přesun TCP na definované souřadnice X, Y, Z s přesností $\pm$ 0.1 mm. |Vysoká | Provozní scénář | Demonstrace| Porovnání cílových a aktuálních souřadnic
| **FR-03** | Systém musí aktivovat a  detekovat úspěšný úchop destičky pomocí koncového senzoru | Vysoká |Provozní scénář| Test | Změna v provozním logu u gripper_status
| **FR-04** | Systém musí deaktivovat gripper a potvrdit uvolnění gripperu před odjezdem osy Z. | Vysoká |Provozní scénář| Test | Log událostí a následná změna Z souřadnic
| **FR-05** | Systém musí umožnit posuv os v servisním režimu | Nízka |Servisní technik| Test | Záznam o přijetí příkazu z ovladače (panel)
| **FR-06** | Systémově implementované softwarově mechanické limity | Vysoká | Bezpečnostní technik | Test | Chybová hláška v terminálu při pohybu mimo rozsah
| **FR-07** | Ukládání systémových dat o dokončených cyklech, chybových hlášení a stavu senzorů do logu a odesílat přes ROS2 v realtimu | Střední | Záznám výsledků | Analýza logu | soubor .log na disku s historií dat
| **NFR-01** | Systém musí přejít do bezpečného stop-stavu při detekci poruchy/červeného tlačítka   do 500 ms (Failsafe). | Kritická | Bezpečnostní technik | Měření | Časový rozdíl v logu mezi chybou a zastavením motoru
| **NFR-02** | Provozuschopnost systému víc než 95 % plánované výrobní doby  | Vysoká | Koordnitánor výroby | Analýza logu |Report z diagnostického modulu
| **NFR-03** | Síťová komunikace ROS2 izolována od veřejné sítě a ochráněna od neoprávných příkazů | Vysoká | Vývojář | Inspekce sítě | Konfigurační soubor firewallu


**Požadavky na rozhraní**

- **SW rozhraní** - ROS2 API
- **HW rozhraníí** - Signál z koncového senzoru, řízení přes USB/CAN
- **Časování** - Perioda řídící smyčky 10 ms


**Stop stavy a chování při poruchách**

- **Failsafe režim** - při ztrátě komunika s nadřazeným systémem musí robot dokončit pohyb do neutrální polohy nebo okamžitě zastavit
- **Emergency STOP** - Fyzické odpojení napájení motorů při narušení klece


**Akceptační kritéria rozhraní**



||Detekce neúspěšného úchopu - navázáno na FR-03|
| :--- | :--- | 
| **Given** | Robot se nachází na zásobníkem a spustil uchopovací cyklus
| **When** | Koncový senzor nahlásí zmáčknutí koncového spínače indikující chybějící polotovar
| **Then** | Robot přeruší cyklus, zvedne osu Z do bezpečné výšky a aktivuje alarm

||Reakce na nouzové zastavení - navázáno na NRF-01|
| :--- | :--- | 
| **Given** | Robot provádí pohyb v libovolné ose
| **When** | Dojde k rozpojení bezpečnostního okruhu (tlačítko, otevření klece)
| **Then** | Systém odpojí pohony a veškerý pohyb se zastaví do 500 ms 




## 1.3. Model system

**Doménový model**

Tento model definuje, jaká data a objekty v systému existují a jak spolu souvisí. V našem případě jde o softwarovou reprezentaci robota.

<div align="center">
  <img src="images/img_1.6.png" alt="Doménový model" width="730">
  <br>
  <i>obr. 1.5 - Doménový model</i>
</div>

**Dynamický model: Stavový autommat**
Model definující v jakém stavu se software nachází a co ho nutí stav měnit.

Na zákaldě požadavků, digram vypadá

<div align="center">
  <img src="images/img_1.7.png" alt="Doménový model" width="700">
  <br>
  <i>obr. 1.7 - Dynamický model </i>
</div>

** Procesní model - Data Flow Diagram**
Vytvořen pro klíčová proces - Úchop polotovaru

## 1.4. Verification and Validation 

## 1.5. Prototype
