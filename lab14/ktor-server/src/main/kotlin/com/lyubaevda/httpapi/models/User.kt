package com.lyubaevda.httpapi.models

import kotlinx.serialization.EncodeDefault


@kotlinx.serialization.Serializable
class User(
    @EncodeDefault(EncodeDefault.Mode.NEVER) var accessToken: String = "",
    val email: String,
    val password: String
)