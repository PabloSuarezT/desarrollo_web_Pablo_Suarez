package com.Tarea4.Tarea4.models;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;

@Entity
@Table
public class comuna {

    @Id
    @SequenceGenerator(
        name = "comuna_sequence",
        sequenceName = "comuna_sequence",
        allocationSize = 1
    )
    @GeneratedValue(
        strategy = GenerationType.SEQUENCE,
        generator = "comuna_sequence"
    )

    @NotNull
    private Integer id;

    @NotNull
    private String nombre;

    @NotNull
    private Integer region_id;

    public comuna(){
    }

    public comuna(String nombre,
                  Integer region_id){

        this.nombre = nombre;
        this.region_id = region_id;
    }

    public Integer getId(){
        return id;
    }

    public String getNombre(){
        return nombre;
    }

    public Integer getRegion_id(){
        return region_id;
    }

    



}