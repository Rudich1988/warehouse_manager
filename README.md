## Warehouse_manager
Warehouse_manager - сервис с REST API на основе HTTP для управления процессами на складе, позволяющий управлять товарами, складскими запасами и заказами.
Сервис дает возможность создавать, удалять товары, смотреть и изменять информацию о них, а также создавать заказы с товарами, просматривать актуальную информацию о них и их товарах, а также изменять статус заказа.
### Как развернуть проект:
- Создайте в корне проекта файл .env
- Изучите содержимое файла .env.example. В нем содержатся примеры переменных, которые Вы должны создать в файле .env
- Экспортируйте переменные, например:
```bash
export SECRET_KEY=your_secret_key
```
- Запуск:
```bash
poetry install
poetry shell
make dev
```

- Docker:
```bash
cp env.example .env
```
- Docker build and run:
```bash
docker-compose build
docker-compose up
```
