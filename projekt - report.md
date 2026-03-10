
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
  <img src="Images/Img_1.3.png" alt="Robotický manipulátor" width="200">
  <br>
  <i>obr. 1.1 - Robotický manipulátor</i>
</div>



<div align="center">
  <img src="Images/Img_1.2.png" alt="CAD model robotického manipulátoru" width="300">
  <br>
  <i>obr. 1.2 - CAD model robotického manipulátoru"</i>
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


## 1.2. Requirements Specification


## 1.3. Model system

## 1.4. Verification and Validation 

## 1.5. Prototype
