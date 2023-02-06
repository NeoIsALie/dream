# Изменения
* оптимизация Dockerfile
* сервис перенесен на fastapi
* тесты на pytest

## запуск тестов из контейнера
    docker exec -it <container-id> bash
    pytest tests/
