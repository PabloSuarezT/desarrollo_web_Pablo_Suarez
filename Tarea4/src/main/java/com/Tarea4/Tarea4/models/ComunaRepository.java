// src/main/java/com/Tarea4/Tarea4/models/ComunaRepository.java
package com.Tarea4.Tarea4.models;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import java.util.List;

public interface ComunaRepository extends JpaRepository<comuna, Integer> {
    
    @Query("SELECT c.id, c.nombre FROM comuna c")
    List<Object[]> findAllComunaIdAndName();
}