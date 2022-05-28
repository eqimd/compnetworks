package com.lyubaevda.httpapi.routes

import com.lyubaevda.httpapi.models.User
import com.lyubaevda.httpapi.models.UserDatabase
import io.ktor.application.*
import io.ktor.http.*
import io.ktor.request.*
import io.ktor.response.*
import io.ktor.routing.*

fun Route.userRouting() {
    post("/register") {
        val user = call.receive<User>()
        UserDatabase.registerUser(user)
        call.respondText(
            "Success",
            status = HttpStatusCode.OK
        )
    }

    get("/signin") {
        val user = call.receive<User>()
        val token = UserDatabase.signUser(user)
        if (token == null ) {
            call.respondText(
                "Wrong user info",
                status = HttpStatusCode.BadRequest
            )
        }
        call.respondText(token!!, status = HttpStatusCode.OK)
    }
}

fun Application.registerUserRoutes() {
    routing {
        userRouting()
    }
}