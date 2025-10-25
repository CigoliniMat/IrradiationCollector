# IrradiationCollector
    
## Descrizione
L'obbiettivo di questo progetto è di semplificare lo scaricaggio dei dati di **irraggimento solare** per diverse località dal sito [Copernicus Atmosphere Data Store](https://ads.atmosphere.copernicus.eu/datasets/cams-solar-radiation-timeseries) che attualmente faccio a mano.
Per farlo userò l'API disponibile sul sito [CDS API](https://ads.atmosphere.copernicus.eu/api).

Il progetto è sviluppato usando **Python** per la parte backend e **HTML/CSS/Javascript** per l'interfaccia grafica (usando **Flask**).
I dati verranno salvati in un database **SQLite** locale.
    
## Componenti utilizzati:
* Flask:   interfaccia utente
* SQlite:  gestione database
* CDSAPI:  uso dell'[API](https://ads.atmosphere.copernicus.eu/api)

## Cose da fare:
- [x] aggiunta e rimozione località
- [x] filtro per località con ricerca
- [ ] guida per registrarsi e salvare l'API di *copernicus.eu*
- [ ] download di un determinato periodo di tempo scelto dall'utente
- [ ] visualizzazione dei dati direttamente sul sito tramite dei grafici
- [ ] cambio lingua nella pagine (IT-EN)
- [ ] cambio tema (chiaro/scuro)
