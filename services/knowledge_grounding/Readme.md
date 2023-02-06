# Изменения
* оптимизация Dockerfile
* сервис перенесен на fastapi
* тесты на pytest
* код, модели и конфигурация вынесены в отдельные файлы

## запуск тестов из контейнера
    docker exec -it <container-id> bash
    pytest tests/
