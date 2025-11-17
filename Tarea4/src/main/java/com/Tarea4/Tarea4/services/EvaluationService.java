package com.Tarea4.Tarea4.services;

import com.Tarea4.Tarea4.models.AvisoEvaluacionDto;
import com.Tarea4.Tarea4.models.AvisoRepository;
import com.Tarea4.Tarea4.models.ComunaRepository;
import com.Tarea4.Tarea4.models.NotaRepository;
import com.Tarea4.Tarea4.models.aviso_adopcion;
import com.Tarea4.Tarea4.models.nota;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class EvaluationService {

    private final AvisoRepository avisoRepository; 
    private final NotaRepository notaRepository;
    private final ComunaRepository comunaRepository;
    

    public EvaluationService(AvisoRepository avisoRepository, NotaRepository notaRepository,ComunaRepository comunaRepository) {
        this.avisoRepository = avisoRepository;
        this.notaRepository = notaRepository;
        this.comunaRepository = comunaRepository;
    }

    // Lógica para la vista inicial 
    public List<AvisoEvaluacionDto> getAvisosConEvaluacion() {
        // 1. Obtener todos los avisos
        List<aviso_adopcion> avisos = avisoRepository.findAll();
        
        // 2. Obtener todos los promedios de la DB
        List<Object[]> averages = notaRepository.findAveragePerAviso();

        List<Object[]> comunaData = comunaRepository.findAllComunaIdAndName();
        Map<Integer, String> comunaMap = comunaData.stream()
            .collect(Collectors.toMap(
                arr -> (Integer) arr[0], 
                arr -> (String) arr[1]
            ));
        
        // 3. Convertir la lista de promedios a un mapa (aviso_id -> promedio)
        Map<Long, Double> averageMap = averages.stream()
            .collect(Collectors.toMap(
                // La consulta de JPQL devuelve Long, Double
                arr -> ((Integer) arr[0]).longValue(), 
                arr -> (Double) arr[1]
            ));

        
        List<AvisoEvaluacionDto> dtoList = new ArrayList<>();
        for (aviso_adopcion aviso : avisos) {
            Double promedio = averageMap.get(aviso.getId()); 
            String comunaNombre = comunaMap.getOrDefault(aviso.getComuna_id(), "Comuna Desconocida");
            dtoList.add(new AvisoEvaluacionDto(aviso,comunaNombre,promedio));
        }
        
        return dtoList;
    }


    // Lógica para el endpoint API 
    @Transactional
    public Double saveAndRecalculate(Integer avisoId, Integer valorNota) {
        // 1. Validación (usando el método estático del modelo nota)
        if (!nota.validateNota(valorNota)) {
            throw new IllegalArgumentException("La nota debe ser un número entero entre 1 y 7.");
        }

        // 2. Crear y guardar la nueva nota en la DB
        nota nuevaNota = new nota(avisoId, valorNota);
        notaRepository.save(nuevaNota);

        // 3. Recalcular y devolver el nuevo promedio
        return notaRepository.findAverageByAvisoId(avisoId).orElse(null);
    }
}