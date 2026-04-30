package com.example.hello;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/hello")
public class HelloController {

    @GetMapping
    public String hello(@RequestParam(required = false) String name) {
        if (name == null || name.isBlank()) {
            return "Hello World!";
        }
        return "Hello " + name + "!";
    }
}
