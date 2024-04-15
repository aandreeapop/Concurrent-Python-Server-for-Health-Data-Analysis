# Le Stats Sportif
## Pop Andreea


### Descriere
Proiectul reprezinta un sistem bazat pe server, care proceseaza date dintrun fisier csv despre nutritie, activitate fizica si obezitate in SUA si furnizeaza diferite statistici bazate pe aceste date. Acest proiect este format dintr-un server web Flask si o aplicatie de gestionare a sarcinilor care ruleaza în fire de executie separate.


### Componente

1. In folderul app/, unde se afla solutia mea:
  * **__init__.py** - Initializeaza elementele necesare acestui program, cum ar fi: un server Flask, o instanta a clasei ThreadPool si un counter al job-urilor.
  * **data_ingestor.py** - Acest fisier este responsabil pentru procesarea de date csv, rand pe rand si pentru furnizarea de metode, corespondente fiecarei rute definite in solutie (calcularea mediei valorilor, cele mai bune si cele mai rele state etc.), valori ce sunt puse in format json (cu doi parametri: 'status' si 'data') in folderul results/, in fisierul corespunzator job ID-ului.
  * **routes.py** - Defineste rutele pentru endpoint-urile API-ului Flask și contine logica de procesare a solicitarilor HTTP primite de la client. La fiecare cerere de tip 'POST', job ID-ul (counter-ul actual) este pus intr-un dictionar de job-uri, alturi de statusul "running", se pune jobul in queue, se apeleaza metoda corespunzatoare din DataIngestor si se incrementeaza counter-ul de job-uri. Toate tipurile de cereri returneaza job ID-ul respectiv.
  * **task_runner.py** - Se ocupa cu gestionarea sarcinilor si executia lor in fire de executie separate, fiecare thread (din TaskRunner), ocupandu-se de cate un job ID din queue-ul din ThreadPool, si modificand valoarea din dictionar al cheii corespunzatoare job ID-ului in "done"
.

