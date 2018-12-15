# RHC Load accounts example

**Docker build:**
docker build -t data_loader data_loader/.

**Docker run:**
docker run --rm -v /*путь к репозиторию*/rhc-load-accounts-example/data.zip:/tmp/data/data.zip:ro -it data_loader

data.zip можно сделать самому из примера данных в папке data. Просто сжимаете ammo, answers, data в архив data.zip и будет ок.