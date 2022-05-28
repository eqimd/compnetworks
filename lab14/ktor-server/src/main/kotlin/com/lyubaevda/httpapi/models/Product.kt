package com.lyubaevda.httpapi.models

import kotlinx.serialization.EncodeDefault

@kotlinx.serialization.Serializable
class Product(
    @EncodeDefault(EncodeDefault.Mode.NEVER) var id: String? = null,
    var name: String,
    var description: String
)
