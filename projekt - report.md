
# 1. Řídící systém robotického manipulátoru
Autor: Jan Matouš 

Předmět: Softwarové inženýrství

Akademický rok 2025/2026

Vedoucí předmětu: Ing. Pavel Steinbauer, Ph.D. a Ing. Jan Pelikán, Ph.D.


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

1. **Inicializace a homing** - robot zaručeně a bezpečně najde referenční polohy všech 3 os
2. **Pick and place cyklus** - přesun materiálu ze zásobníku do konkrétního slotu v chemické lázni
3. **Výměna lázně** - přesun robota do bezpečné polohy umožňující servis lázní
4. **Krizové zastavení** - Okamžité zastavení motorů při narušení pracovního prostoru nebo stistku STOP tlačítka
5. **Detekce chyby úchopu** - rozpoznání nesprávného úchopu výrobního materiálu a přerušení cyklu


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

- **Hardware** - Tří osá kontruskce s pohonem přes krokové motory, odolný gripper vůči chemické korozi 
  
- **Rozhraní** - Komunikace mezi moduly probíhá přes standarty ROS2
  
- **Standardy a normy** - Systém musí splňovat normy **ISO 10218** - průmyslové roboty - bezpečnost a směrnice pro práci v chemickém prostředí
  
- **Bezpečností limity** - Maximální rychlost pohybu v blízkosti okraje lázní omezena na 200 mm/s, zároveň okamžíté zastavení při detekci vniknutí do klece
  
- **Reálný čas** - Řídící smyčka pro plánování trajektorie běží s pevnou periodou pro zaručení stability pohybu 


### Plán práce týmu a rozdělení rolí
| Fáze projektu | Odpovědná role | Výstup (Artefakt) |
| :--- | :--- | :--- |
| **Analýza a vize** | Systémový architekt | Vision & Scope dokumentace, C4 diagram |
| **Specifikace požadavků** | Requirements Engineer | Seznam FR a NFR, Use-case model |
| **Návrh a modelování** | SW Inženýr | Doménový model, stavové automaty |
| **Ověřování a testy** | V&V Specialista | Testovací případy, V&V matice |
| **Prototypování** | Vývojář | ROS2 simulace, kód klíčové funkce |



## 1.2. Requirements Specification

Cílem je definování systému tak, aby byl jednoznačný a testovatelný

### Usecase model
Popis interakce mezi aktéry a systémem pro manipulaci s polotovarem

**Pick and Place cyklus**

- *Hlavní scénář* -  Pick and place
- *Alternativní tok* - Robot čeká, dokud není v zásobníku nová destička
- *Chybová tok* - Detekce neuchopeného polotovaru, přerušení hlavního toku

<div align="center">
  <img src="images/img_1.5.png" alt="Usecase diagram" width="680">
  <br>
  <i>obr. 1.4 - Usecase diagram</i>
</div>




#### Seznam požadavků (FR & NFR)
| ID | Požadavek | Priorita | Zdroj | Verifikace |
| :--- | :--- | :--- | :--- |:--- |
| **FR-01** | Systém musí umožnit automatickou kalibraci všech 3 os (Homing) | Vysoká | Servisní technik | Test |
| **FR-02** | Robot musí provést kompletní manipulační cyklus na základě souřadnic z ROS2. | Vysoká | Provozní scénář | Demonstrace|
| **FR-03** | Systém musí detekovat úspěšný úchop destičky pomocí koncového senzoru | Vysoká |Provozní scénář| Test |
| **FR-04** | Systém musí umožnit posuv os v servisním režimu | Nízka |Servisní technik| Test |
| **FR-05** | Systémově implementované softwarově mechanické limity | Vysoká | Bezpečnostní technik | Test |
| **FR-06** | Ukládání systémových dat o dokončených cyklech, chybových hlášení a stavu senzorů do logu a odesílat přes ROS2 v realtimu | Střední | Záznám výsledků | Analýza logu |
| **NFR-01** | Systém musí přejít do bezpečného stop-stavu při detekci poruchy/červeného tlačítka  do 500 ms (Failsafe). | Kritická | Bezpečnostní technik | Měření |
| **NFR-02** | Odolnost senzorů proti korozivním výparům  | Střední | Provozní prostředí  | Inspekce|
| **NFR-03** | Provozuschopnost systému víc než 95 % plánované výrobní doby  | Vysoká | Koordnitánor výroby | Analýza logu |
| **NFR-04** | Síťová komunikace ROS2 izolována od veřejné sítě a ochráněna od neoprávných příkazů | Vysoká | Vývojář | Inspekce sítě |


**Požadavky na rozhraní**

- **SW rozhraní** - ROS2 API
- **HW rozhraníí** - Signál z koncového senzoru, řízení přes USB/CAN
- **Časování** - Perioda řídící smyčky 10 ms


**Stop stavy a chování při poruchách**

- **Failsafe režim** - při ztrátě komunika s nadřazeným systémem musí robot dokončit pohyb do neutrální polohy nebo okamžitě zastavit
- **Emergency STOP** - Fyzické odpojení napájení motorů při narušení klece


**Akceptační kritéria rozhraní**


||Úspěšný manipulační cyklus - navázáno na FR-02|
| :--- | :--- | 
| **Given** | Robot ve stavu ready, polotovar v zásovníku a systém přijal souřadnice cílového slotu přes ROS2
| **When** | Nadřazený systém odešle příkaz ke spuštění cyklu
| **Then** | Robot proveje nájezd, úchop polotovaru, přesun do slotu lázně, uvolnění úchopu a návrat do poč. polohy


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


## 1.4. Verification and Validation 

## 1.5. Prototype
