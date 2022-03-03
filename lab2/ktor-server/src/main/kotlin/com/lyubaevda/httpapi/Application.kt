package com.lyubaevda.httpapi

import com.lyubaevda.httpapi.routes.registerProductRoutes
import io.ktor.application.*
import io.ktor.features.*
import io.ktor.serialization.*
import io.ktor.server.engine.*
import io.ktor.server.netty.*

fun main() {
    embeddedServer(Netty, 9090) {
        install(ContentNegotiation) {
            json()
        }
        registerProductRoutes()
    }.start(wait = true)
}
