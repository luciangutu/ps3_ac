# ps3_ac
This script is searching for "Autorizatii de construire" and "Certificate urbanism" from Primaria sector 3 website

### Setup
Create and activate the new virtual environment

```shell
virtualenv venv
. venv/bin/activate
```

Add the requirements
```shell
cat > requirements.in
requests
PyPDF2
```

Generate the `requirements.txt`
```shell
pip install -r requirements.in
pip freeze --all > requirements.txt
```

### How to run
`config.py` should look like:
```
search_terms = {
    "236157": "test"
}
years = ["2022", "2023"]
```

Activate the virtual environment and run
```
. venv/bin/activate
python ./search_ps3_ac.py
Looking inside AC_2023_1.pdf for 236157: Test
['27.02.Bucurestiamplasare container prefabricat pentru colectare deșeuri reciclabile, modificări la fațadă și organizare de șantier236157']
```

