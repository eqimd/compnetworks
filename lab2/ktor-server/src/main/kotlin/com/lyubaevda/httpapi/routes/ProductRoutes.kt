package com.lyubaevda.httpapi.routes

import com.lyubaevda.httpapi.models.Product
import com.lyubaevda.httpapi.models.ProductList
import io.ktor.application.*
import io.ktor.http.*
import io.ktor.request.*
import io.ktor.response.*
import io.ktor.routing.*

fun Route.productRouting() {
    route("/product") {
        get {
            val allProducts = ProductList.getAllProducts()
            if (allProducts.isNotEmpty()) {
                call.respond(allProducts)
            } else {
                call.respondText("No products found", status = HttpStatusCode.NotFound)
            }
        }

        get("{id}") {
            val id = call.parameters["id"] ?: return@get call.respondText(
                "Missing or malformed id",
                status = HttpStatusCode.BadRequest
            )
            val product =
                ProductList.getProduct(id) ?: return@get call.respondText(
                    "No product with id $id",
                    status = HttpStatusCode.NotFound
                )
            call.respond(Pair(id, product))
        }

        post {
            val product = call.receive<Product>()
            ProductList.addNewProduct(product)
            call.respondText("Product stored correctly", status = HttpStatusCode.Created)
        }

        put("{id}") {
            val id = call.parameters["id"] ?: return@put call.respondText(
                "Missing or malformed id",
                status = HttpStatusCode.BadRequest
            )

            val product = call.receive<Product>()
            ProductList.updateProduct(id, product) ?: return@put call.respondText(
                "No product with id $id",
                status = HttpStatusCode.NotModified
            )
            call.respond(Pair(id, product))
        }

        delete("{id}") {
            val id = call.parameters["id"] ?: return@delete call.respond(HttpStatusCode.BadRequest)
            if (ProductList.deleteProduct(id) != null) {
                call.respondText("Customer removed correctly", status = HttpStatusCode.Accepted)
            } else {
                call.respondText("Not Found", status = HttpStatusCode.NotFound)
            }
        }
    }
}


fun Application.registerProductRoutes() {
    routing {
        productRouting()
    }
}
