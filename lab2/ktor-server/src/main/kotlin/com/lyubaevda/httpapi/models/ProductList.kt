package com.lyubaevda.httpapi.models

import java.util.concurrent.ConcurrentHashMap

object ProductList {
    private const val STRING_LENGTH = 20
    private val CHAR_POOL = ('a'..'z').toList() + ('A'..'Z').toList() + ('0'..'9').toList()

    private val productMap = ConcurrentHashMap<String, Product>()

    fun getAllProducts(): List<Product> = productMap.values.toList()

    fun getProduct(id: String): Product? = productMap[id]

    fun addNewProduct(product: Product) {
        while (true) {
            val randomId = (1..STRING_LENGTH)
                .map { kotlin.random.Random.nextInt(0, CHAR_POOL.size) }
                .map(CHAR_POOL::get)
                .joinToString("")

            productMap.putIfAbsent(randomId, product) ?: run {
                product.id = randomId
                return
            }
        }
    }

    fun updateProduct(id: String, product: Product): Product? = productMap.computeIfPresent(id) { _, _ -> product }

    fun deleteProduct(id: String): Product? = productMap.remove(id)
}
