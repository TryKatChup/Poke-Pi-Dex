# Documento di Progetto (ITA)

L'applicazione consiste in un'emulazione del pokèdex, che permette di riconoscere tipi diversi di pokèmon, fornendo le informazioni relative.
<br/>
<p align="center">
	<a href="https://github.com/TryKatChup/pokemon-cv-revival/blob/main/docs/Project%20Document.md">English</a>
	·
	<a href="https://github.com/TryKatChup/pokemon-cv-revival/">Home page</a>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
	<summary><h2 style="display: inline-block">Indice</h2></summary>
	<ol>
		<li><a href="#abstract">Abstract</a></li>
		<li><a href="#analisi-dei-requisiti">Analisi dei Requisiti</a>
			<ul>
				<li><a href="#raccolta-dei-requisiti">Raccolta dei Requisiti</a></li>
				<li><a href="#analisi-del-dominio">Analisi del Dominio</a></li>
				<li><a href="#use-case">Use Case</a></li>
				<li><a href="#user-story">User Story</a></li>
				<li><a href="#test-plan-informale">Test Plan Informale</a></li>
			</ul>
		</li>
		<li><a href="#analisi-del-problema">Analisi del Problema</a>
			<ul>
				<li><a href="#aspetti-rilevanti">Aspetti Rilevanti</a></li>
				<li><a href="#problemi-principali">Problemi Principali</a></li>
				<li><a href="#architettura-logica">Architettura Logica</a></li>
			</ul>
		</li>
		<li><a href="#progettazione">Progettazione</a></li>
		<li><a href="#testing">Testing</a></li>
		<li><a href="#deployment">Deployment</a></li>
		<li><a href="#manutenzione">Manutenzione</a></li>
	</ol>
</details>

## Abstract
Progettare e sviluppare un'applicazione che implementi le funzionalità di un [pokèdex](https://it.wikipedia.org/wiki/Pok%C3%A9dex). In particolare, l'applicazione dovrà:
- eseguire su un Raspberry Pi4 dotato di display da 3.5 pollici;
- caricare un dataset con i pokèmon della prima generazione;
- prendere in ingresso uno stream video, tramite una picamera collegata al Raspberry;
- rilevare che l'oggetto inquadrato sia un pokèmon;
- riconoscere il pokèmon inquadrato, restituendo il suo ID nel pokèdex;
- mostrare a schermo i dati di tale pokèmon.

## Analisi dei Requisiti
È necessario realizzare l'applicativo **pokèdex_app**.

### Raccolta dei Requisiti
##### Requisiti Hardware
- Raspberry Pi
- videocamera
- display
- batteria
- case fisico in cui inserire i vari componenti
- speaker
- joystick analogico
- canali di comunicazione (cavetti)
- comvertitore AD

##### Requisiti Software
- dataset con pokèmon di prima generazione (nome, id, tipi, evoluzioni, descrizione, immagini e verso)
- applicativo che implementi:
	- rete neurale per il riconoscimento
	- interfaccia grafica utente (GUI) che mostri i dettagli sui pokèmon riconosciuti
- ambiente virtuale di esecuzione

### Analisi del Dominio
Vocabolario (significato di nomi e verbi inclusi nei requisiti)
<table>
	<tr>
		<td width="10%">Termine</td>
		<td width="60%">Definizione</td>
		<td width="20%">Sinonimi</td>
	</tr>
	<tr>
		<td>PokèDex</td>
		<td>Strumento elettronico immaginario che appare nei videogiochi, nell'anime e nei manga dei PokèMon. Ha la funzione di un assistente digitale personale, progettato per catalogare e fornire informazioni sulle varie specie di Pokémon. È ciò che l'applicativo dovrà emulare.</td>
		<td></td>
	</tr>
	<tr>
		<td>Raspberry</td>
		<td>È l'architettura hardware su cui l'applicazione esegue.</td>
		<td>Elaboratore, Calcolatore</td>
	</tr>
	<tr>
		<td>Display</td>
		<td>Schermo LCD da 3.5 pollici (480x320), supportato dal Raspberry, che permetta di visualizzare ed interagire con l'interfaccia grafica dell'applicazione.</td>
		<td>Monitor</td>
	</tr>
	<tr>
		<td>Dataset</td>
		<td>Insieme di informazioni completo per ciascun pokèmon, che includa: ID, nome, tipi, descrizione, statistiche e almeno un'immagine.</td>
		<td></td>
	</tr>
	<tr>
		<td>PokèMon</td>
		<td>Il tipo di oggetto che l'applicazione dev'essere in grado di riconoscere e distinguere, ovvero una creatura fantastica, appunto un "mostro" (Mon-ster) "tascabile" (Pok-et) da cui prende il nome, dell'omonimo franchise.</td>
		<td></td>
	</tr>
	<tr>
		<td>Prima generazione</td>
		<td>I pokèmon si dividono in generazioni, ciascuna delle quali comprende specie originarie dalla stessa regione. I pokèmon di prima generazione provengono da Kanto e sono 151, ovvero ciascun tipo di pokèmon di questa generazione ha un identificativo compreso tra 1 (Charmander) e 151 (Mew), e sono quelli che l'applicazione dovrà essere in grado di riconoscere e catalogare.</td>
		<td></td>
	</tr>
	<tr>
		<td>Picamera</td>
		<td>Componente esterno, supportato dal Raspberry, che permette di registrare e inviare all'elaboratore un flusso continuo di immagini in tempo reale.</td>
		<td>Videocamera</td>
	</tr>
	<tr>
		<td>Rilevare</td>
		<td>L'applicazione dev'essere in grado di capire se l'oggetto inquadrato sia un pokèmon di prima generazione oppure no.</td>
		<td></td>
	</tr>
	<tr>
		<td>Riconoscere</td>
		<td>L'applicazione dev'essere in grado di capire quale pokèmon, dei 151 di prima generazione, esso sia.</td>
		<td>Catalogare</td>
	</tr>
</table>

### Componenti a Disposizione
- 1x [LABISTS Starter Kit for Raspberry Pi4](https://labists.com/products/labists-raspberry-pi-4g-ram-32gb-card)
	- 1x [Raspberry Pi4 Model B 4GB RAM](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/)
	- 1x Adattatore USB-C per l'Alimentatore
	- 1x 32GB MicroSD Card
	- 1x Mini Ventola Silenziosa
	- 3x Dissipatori in Rame
- 1x [Joystick Analogico](https://arduinomodules.info/ky-023-joystick-dual-axis-module/)

### Componenti da Comprare
- [x] 1x [Raspberry Pi Camera Rev 1.3 (5MP, 1080p)](https://www.amazon.it/dp/B08KZLVD36/ref=cm_sw_r_apan_glt_i_C1SA6N8GZESBFRTRQEFH?_encoding=UTF8&psc=1) - [specifiche](https://picamera.readthedocs.io/en/release-1.3/fov.html)
- [x] 1x [Display LCD 3.5 pollici, HDMI touch screen](https://www.amazon.it/dp/B08HVDLHRW/ref=cm_sw_r_apan_glt_i_P4JYG7RGEMVPB287BHZ1?_encoding=UTF8&psc=1)
- [x] 2x [Mini Speaker](https://www.amazon.it/dp/B07FT9CFY4/ref=cm_sw_r_apan_glt_i_Y86XG3MWY2A2D21EF8ZH?_encoding=UTF8&psc=1)
- [x] 1x [Powerbank](https://www.amazon.it/Auskang-compatibile-batteria-Caricabatterie-Portatile/dp/B096FX9226/ref=sr_1_1?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=auskang&qid=1634322262&qsid=258-6802503-2920908&sr=8-1&sres=B096FX9226%2CB08RDTRWHY%2CB096B29B6G%2CB08RDTR7F7%2CB08R8J1D19%2CB08R8CKQJT%2CB08SHFYHSR%2CB08SJ5K3LR%2CB096JXNZ17%2CB08R8HCWRT%2CB09715272M%2CB091CGG33P%2CB08NTHCNB8%2CB08DTP9LZ8%2CB096B9TV8C%2CB0972SQQS7%2CB0932PZ857%2CB094J428L5%2CB082PPPWXY%2CB019GJLER8)
- [ ] 1x [Case Pokèdex](https://github.com/TryKatChup/pokemon-cv-revival/tree/main/3D%20models/pok%C3%A8dex%20case)
- [ ] 1x [Adafruit MCP3008 Convertitore A/D](https://www.adafruit.com/product/856) - [guida](https://grantwinney.com/connecting-an-analog-joystick-to-the-raspberry-pi-and-using-it-with-an-rgb-led-to-simulate-a-color-wheel/)
- [ ] 1x Interruttore Switch per Alimentazione

### Use Case
Modello\
<img src="https://github.com/TryKatChup/pokemon-cv-revival/blob/main/docs/diagrams/use_cases.png"/>

### User Story
<table>
	<tr>
		<td>Come utente accendo il dispositivo ed eseguo l'applicazione (o viene eseguita in automatico all'avvio). Dunque mi aspetto di vedere un'interfaccia grafica che comprende una sezione relativa all'output video di una videocamera, ed una sezione relativa ai dati.
Quando inquadrerò un Pokémon (che può essere una carta, un peluche o una figure) l'applicazione dev'essere in grado di riconoscerlo e mostrare nella sezione dedicata ai dati le informazioni ed i dettagli relativi a tale Pokémon.</td>
		<td width="40%"><img src="https://github.com/TryKatChup/pokemon-cv-revival/blob/main/docs/example.png"/></td>
	</tr>
</table>

### Test Plan Informale
Poiché l'obbiettivo principale del progetto è il riconoscimento di un pokèmon, il Test Plan deve innanzitutto verificare che l'oggetto relativo ad esso, il quale potrebbe essere una carta da gioco o una figure, venga riconosciuto correttamente. Ad esempio, avendo a disposizione una carta da gioco di Squirtle (Pokèdex ID = 7), è possibile inquadrarla utilizzando il dispositivo su cui esegue l'applicativo, per ottenere i dati relativi a tale pokèmon: la rete neurale dovrà quindi riconoscere che il pokèmon inquadrato sia Squirtle, e restituire 7.\
Come test secondari è necessario verificare il funzionamento dei componenti hardware (speaker audio, joystick analogico) e dei canali di comunicazione tra questi ed il Raspberry (cavo aux, cavetti e convertitore AD).

## Analisi del Problema

### Aspetti Rilevanti
- rilevazione e riconoscimento di oggetti;
- utilizzo dell'hardware sottostante;
- grafica.

Phyton è il linguaggio più utilizzato, documentato e flessibile per quanto riguarda data science, machine learning e computer vision. Inoltre, esistono diversi framework e librerie utili, tra cui tensorflow, keras, opencv e molti altri, la maggior parte dei quali sono open source. In aggiunta, python dispone di API specifiche che rendono semplice l'interazione con l'hardware del raspberry, fra cui picamera, bottoni e joystick.
tkinter
conda(?)

<!--
Identificare i problemi principali dati dai requisiti e le tecnologie (software) più appropriate da adottare (motivare scelta Python - per API tensorflow, probabilmente possiamo prendere qualcosa dalle slide, conda, tkinter, keras, ecc.)
WARNING: expressions like 'we have chosen to ...', 'I decided ...', etc. are forbidden here.
Rather, this section should include sentences like 'this (aspect of the) problem implies that ...' or 'the usage of this (legacy) component requires that ...', etc.
-->

### Problemi Principali
Tutta la parte sulla definizione del modello per la rete neurale, il codice per il riconoscimento, l'allenamento della rete.
Riconoscere tipi di oggetto differenti.

### Architettura Logica

##### Struttura Applicativo
<img src="https://github.com/TryKatChup/pokemon-cv-revival/blob/main/docs/diagrams/class_diagram.png"/>

##### Funzionamento Classificatore
- schema non UML
- diagrammi generici (modello dell'architettura logica del sistema)
modificare il diagramma aggiungendo la parte di riconoscimento

## Test Plan
Facendo riferimento all'architettura logica del sistema, predisporre dei test che devono essere soddisfatti

NB: Qui proporre librerie e API diverse, in Testing spiegare che sono state provate diverse librerie per le quali sono stati riscontrati problemi con le dipendenze e alla fine si è optato per pygame ed il suo modulo "mixer".

+ aggiungere programmino di test audio che avevo fatto sul rapberry (+ passaggi per attivare alzare il volume(?))

## Progettazione
Partendo dall'architettura logica del sistema, definire l'architettura concreta del sistema ed il comportamento di ciascun componente.
- diagrammi nel dettaglio (con tipi delle variabili e nomi effettivi)
- diagrammi di dominio, di interfacce, di flusso e di sequenza.

## Testing
Completare i test in base al codice del progetto ed eseguirli (aggiungere video)
- [ ] componenti gui - risposta della gui senza delay, cambio di interfaccia in tempistiche accettabili
- [ ] load dati pokèmon
- [ ] stream video
- [ ] audio
- [ ] riconoscimento (restituzione id giusto, con una certa percentuale di accuratezza)

## Deployment
Preparare virtual env?
Container docker(?)

## Manutenzione
L'ambiente di esecuzione (hardware e software) rimarrà il medesimo e l'applicazione, una volta effettuato il deployment, non verrà modificata né aggiornata. Dunque, salvo bug applicativi trovati a posteriori, o eventuali ottimizzazioni, non sarà necessario alcun tipo di manutenzione.
