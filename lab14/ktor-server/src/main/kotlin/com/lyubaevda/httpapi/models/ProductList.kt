package com.lyubaevda.httpapi.models

import com.lyubaevda.httpapi.models.UserDatabase.tokenExists

object ProductList {
    private const val STRING_LENGTH = 20
    private val CHAR_POOL = ('a'..'z').toList() + ('A'..'Z').toList() + ('0'..'9').toList()

    private val productMap = HashMap<String, Product>()
    private val productMapByTokens = HashMap<String?, MutableList<Product>>()

    fun getAllProducts(token: String?): List<Product>? {
        if (token == null) {
            return productMapByTokens[null]
        }
        if (!tokenExists(token)) {
            return null
        }
        if (productMapByTokens[token] == null) {
            return productMapByTokens[null]
        }

        if (productMapByTokens[null] == null) {
            return productMapByTokens[token]
        }

        return listOf(productMapByTokens[null]!!, productMapByTokens[token]!!).flatten()
    }

    fun getProduct(id: String, token: String?): Product? {
        val product = productMap[id] ?: return null
        val isAvailableForEveryone = productMapByTokens[null]?.contains(product)
        if (isAvailableForEveryone != null && isAvailableForEveryone) {
            return product
        }
        if (token == null || !tokenExists(token)) {
            return null
        }
        if (productMapByTokens[token]?.contains(product) ?: return null) {
            return product
        }

        return null
    }

    fun addNewProduct(product: Product, token: String?) {
        if (token != null && !tokenExists(token)) {
            return
        }
        while (true) {
            val randomId = (1..STRING_LENGTH)
                .map { kotlin.random.Random.nextInt(0, CHAR_POOL.size) }
                .map(CHAR_POOL::get)
                .joinToString("")

            productMap.putIfAbsent(randomId, product) ?: run {
                product.id = randomId
                productMapByTokens.putIfAbsent(token, mutableListOf(product))?.add(product)
                return
            }
        }
    }

    fun updateProduct(id: String, product: Product, token: String?): Product? {
        val oldProduct = productMap[id] ?: return null
        val isAvailableForEveryone = productMapByTokens[null]?.contains(product)
        if (isAvailableForEveryone != null && isAvailableForEveryone) {
            oldProduct.name = product.name
            oldProduct.description = product.description
            return oldProduct
        }
        if (token != null && !tokenExists(token)) {
            return null
        }
        if (productMapByTokens[token]?.contains(product) ?: return null) {
            oldProduct.name = product.name
            oldProduct.description = product.description
            return oldProduct
        }

        return null
    }

    fun deleteProduct(id: String, token: String?): Product? {
        val product = productMap[id] ?: return null
        val isAvailableForEveryone = productMapByTokens[null]?.contains(product)
        if (isAvailableForEveryone != null && isAvailableForEveryone) {
            productMap.remove(id)
            productMapByTokens[null]?.remove(product)
            return product
        }
        if (token != null && !tokenExists(token)) {
            return null
        }
        if (productMapByTokens[token]?.contains(product) ?: return null) {
            productMap.remove(id)
            productMapByTokens[token]?.remove(product)
            return product
        }

        return null
    }
}
