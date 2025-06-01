# GRPC - MenuService

Este documento explica cómo interactuar con el servicio `MenuService` utilizando [grpcurl](https://github.com/fullstorydev/grpcurl).

---

## 🧭 Exploración del servicio

### 🔹 Listar todos los servicios disponibles

```bash
grpcurl -import-path protos -proto menu.proto -plaintext localhost:50051 list
```

### 🔹 Describir un servicio

```bash
grpcurl -import-path protos -proto menu.proto -plaintext localhost:50051 describe MenuService
```

### 🔹 Describir un mensaje

```bash
grpcurl -import-path protos -proto menu.proto -plaintext localhost:50051 describe MenuItem
```

---

## 🧪 Operaciones CRUD del menú

### ✅ Crear un ítem del menú

```bash
grpcurl -import-path protos -proto menu.proto -plaintext -d '{
  "name": "Pizza Margherita",
  "category": "MAIN",
  "price": 12.99,
  "available": true,
  "description": "Classic pizza"
}' localhost:50051 MenuService/CreateMenuItem
```

### 📋 Listar todos los ítems del menú

```bash
grpcurl -import-path protos -proto menu.proto -plaintext localhost:50051 MenuService/ListMenuItems
```

### 🔍 Obtener un ítem del menú por ID

```bash
grpcurl -import-path protos -proto menu.proto -plaintext -d '{"id": 1}' localhost:50051 MenuService/GetMenuItem
```

### ✏️ Actualizar un ítem del menú

```bash
grpcurl -import-path protos -proto menu.proto -plaintext -d '{
  "id": 1,
  "price": 6.50,
  "description": "Toasted bread with fresh tomatoes and basil"
}' localhost:50051 MenuService/UpdateMenuItem
```

### 🗑️ Eliminar un ítem del menú

```bash
grpcurl -import-path protos -proto menu.proto -plaintext -d '{"id": 2}' localhost:50051 MenuService/DeleteMenuItem
```

---

## 📌 Notas

- Asegúrate de que el servidor gRPC esté ejecutándose en `localhost:50051`.
- El parámetro `-import-path protos` asume que el archivo `menu.proto` se encuentra en el directorio `protos/`.
- Si usas HTTPS con certificados no válidos, puedes agregar la opción `--insecure`.
