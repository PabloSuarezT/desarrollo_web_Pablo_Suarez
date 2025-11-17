package com.Tarea4.Tarea4.models;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


@Repository
public interface AvisoRepository extends JpaRepository<aviso_adopcion, Long> {
    Page<aviso_adopcion> findAllByOrderByIdDesc(Pageable pageable);
}
