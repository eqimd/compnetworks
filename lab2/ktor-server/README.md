### Running

Execute this command to start the server:

```bash
./gradlew run
```

### API

Address: `localhost:9090`

Routes:

- `/product`
  + `GET` -- get all the products
  + `GET /$id` -- get a product with id
  + `POST {$name, $description}` -- post a product with name and description
  + `PUT /$id {$name, $description}` -- put new name and description for a product with id
  + `DELETE /$id` -- delete a product with id
