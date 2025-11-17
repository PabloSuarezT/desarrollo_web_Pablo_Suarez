package com.Tarea4.Tarea4.controllers;

import com.Tarea4.Tarea4.services.EvaluationService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ApiController {

    private final EvaluationService evaluationService;

    public ApiController(EvaluationService evaluationService) {
        this.evaluationService = evaluationService;
    }

    @PostMapping("/api/evaluar")
    public ResponseEntity<Double> evaluateAviso(
            @RequestParam Integer avisoId,
            @RequestParam Integer valorNota) {
        
        try {
            Double nuevoPromedio = evaluationService.saveAndRecalculate(avisoId, valorNota);
            return ResponseEntity.ok(nuevoPromedio);
            
        } catch (IllegalArgumentException e) {
            // Retorna un error 400 con el mensaje de validación de la nota
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).build();
        }
    }
}