package com.Tarea4.Tarea4.controllers;

import com.Tarea4.Tarea4.models.AvisoEvaluacionDto;
import com.Tarea4.Tarea4.services.EvaluationService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.List;

@Controller
public class AppController {

    private final EvaluationService evaluationService;

    // Inyección de dependencia
    public AppController(EvaluationService evaluationService) {
        this.evaluationService = evaluationService;
    }

    @GetMapping("/nota")
    public String evaluationListRoute(Model model) {
        
        // Llama al servicio para obtener la lista de DTOs
        List<AvisoEvaluacionDto> avisos = evaluationService.getAvisosConEvaluacion();
        
        model.addAttribute("avisos", avisos);
        
        return "evaluation"; 
    }
}