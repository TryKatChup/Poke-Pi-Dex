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
				<li><a href="#user-story">User Story</a></li>
			</ul>
		</li>
		<li><a href="#analisi-del-problema">Analisi del Problema</a></li>
		<li><a href="#progettazione">Progettazione</a></li>
		<li><a href="#testing">Testing</a></li>
		<li><a href="#deployment">Deployment</a></li>
		<li><a href="#manutenzione">Manutenzione</a></li>
	</ol>
</details>

## Abstract
L'obbiettivo è progettare e sviluppare un'applicazione che implementi le funzionalità di un pokèdex. In particolare, l'applicazione dovrà:
- eseguire su un Raspberry Pi4 dotato di display da 3.5 pollici;
- caricare un dataset con i pokèmon della prima generazione (ID da 1 a 151);
- prendere in ingresso uno stream video da Picamera;
- riconoscere il pokèmon inquadrato, restituendo il suo ID nel pokèdex;
- mostrare a schermo i dati di tale pokèmon.

componenti a disposizione:
- 1x [LABISTS Starter Kit for Raspberry Pi4](https://labists.com/products/labists-raspberry-pi-4g-ram-32gb-card)
	- 1x [Raspberry Pi4 Model B 4GB RAM](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/)
	- 1x USB-C Power Adapter
	- 1x 32GB MicroSD card
	- 1x Mini Silent Fan
	- [...]
- 1x [Raspberry Pi Camera Rev 1.3 (5MP, 1080p)]() - [specs](https://picamera.readthedocs.io/en/release-1.3/fov.html) <- aggiungere link
- 1x [Display 3.5 pollici]() <- aggiungere link
- 2x [Mini Speaker](https://www.amazon.it/dp/B07FT9CFY4/ref=cm_sw_r_apan_glt_i_Y86XG3MWY2A2D21EF8ZH?_encoding=UTF8&psc=1)
- 1x [Powerbank](https://www.amazon.it/Auskang-compatibile-batteria-Caricabatterie-Portatile/dp/B096FX9226/ref=sr_1_1?__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dchild=1&keywords=auskang&qid=1634322262&qsid=258-6802503-2920908&sr=8-1&sres=B096FX9226%2CB08RDTRWHY%2CB096B29B6G%2CB08RDTR7F7%2CB08R8J1D19%2CB08R8CKQJT%2CB08SHFYHSR%2CB08SJ5K3LR%2CB096JXNZ17%2CB08R8HCWRT%2CB09715272M%2CB091CGG33P%2CB08NTHCNB8%2CB08DTP9LZ8%2CB096B9TV8C%2CB0972SQQS7%2CB0932PZ857%2CB094J428L5%2CB082PPPWXY%2CB019GJLER8)
- 1x [Case Pokèdex](https://github.com/TryKatChup/pokemon-cv-revival/tree/main/3D%20models/pok%C3%A8dex%20case)
- joystick analogico, convertitore A/D, bottoni, switch per 

## Analisi dei Requisiti

### User Story
<table>
	<tr>
		<td>Come utente accendo il dispositivo ed eseguo l'applicazione (o viene eseguita in automatico all'avvio). Dunque mi aspetto di vedere un'interfaccia grafica che comprende una sezione relativa all'output video di una videocamera, ed una sezione relativa ai dati.
Quando inquadrerò un Pokémon (che può essere una carta, un peluche o una figure) l'applicazione dev'essere in grado di riconoscerlo e mostrare nella sezione dedicata ai dati le informazioni ed i dettagli relativi a tale Pokémon.</td>
		<td width="40%"><img src="https://github.com/TryKatChup/pokemon-cv-revival/blob/main/docs/example.png"/></td>
	</tr>
</table>

+ foto editata con prototipo GUI

### Test Plan Informale
Test sull'accuratezza del riconoscimento del Pokémon;
Test hardware e software dell'audio (con gli speaker)
NB: spiegare che sono state provate diverse librerie per le quali sono stati riscontrati problemi con le dipendenze e alla fine si è optato per pygame ed il suo modulo "mixer".

## Analisi del Problema

### Aspetti Fondamentali

### Architettura Logica
- diagrammi generici

## Test Plan
Facendo riferimento all'architettura logica del sistema, predisporre dei test che devono essere soddisfatti

## Progettazione
- diagrammi nel dettaglio (con tipi delle variabili e nomi effettivi)

## Testing
Completare i test
- [ ] componenti gui - risposta della gui senza delay, cambio di interfaccia in tempistiche accettabili
- [ ] load dati pokèmon
- [ ] stream video
- [ ] audio
- [ ] riconoscimento (restituzione id giusto, con una certa percentuale di accuratezza)

## Deployment
Preparare virtual env?
Container docker(?)

## Manutenzione
L'ambiente di esecuzione (hardware e software) rimarrà il medesimo e l'applicazione, una volta effettuato il deployment, non verrà modificata né aggiornata. Dunque, salvo bug applicativi trovati a posteriori, o eventuali ottimizzazioni, non è necessario alcun tipo di manutenzione.
