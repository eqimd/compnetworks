package com.lyubaevda.httpapi.models

import java.util.concurrent.ConcurrentHashMap

object UserDatabase {
    private val emailsMap = ConcurrentHashMap<String, User>()
    private val tokensMap = ConcurrentHashMap<String, User>()
    private const val TOKEN_LENGTH = 10
    private val CHAR_POOL = ('a'..'z').toList() + ('A'..'Z').toList() + ('0'..'9').toList()

    fun registerUser(user: User) {
        emailsMap.putIfAbsent(user.email, user)
    }

    fun signUser(user: User): String? {
        if (!emailsMap.containsKey(user.email) || emailsMap[user.email]?.password != user.password) {
            return null
        }
        while (true) {
            val randomToken = (1..TOKEN_LENGTH)
                .map { kotlin.random.Random.nextInt(0, CHAR_POOL.size) }
                .map(CHAR_POOL::get)
                .joinToString("")

            tokensMap.putIfAbsent(randomToken, user) ?: run {
                user.accessToken = randomToken
                return randomToken
            }
        }
    }

    fun tokenExists(token: String) = tokensMap.containsKey(token)
}