package com.Tarea4.Tarea4.models;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface NotaRepository extends JpaRepository<nota, Long> {

    @Query("SELECT AVG(n.nota) FROM nota n WHERE n.aviso_id = :avisoId")
    Optional<Double> findAverageByAvisoId(Integer avisoId);

    @Query("SELECT n.aviso_id, AVG(n.nota) FROM nota n GROUP BY n.aviso_id")
    List<Object[]> findAveragePerAviso();
}