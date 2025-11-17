package com.Tarea4.Tarea4.models;


import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

@Entity
@Table
public class nota {
    
    @Id
    @SequenceGenerator(
        name = "nota_sequence",
        sequenceName = "nota_sequence",
        allocationSize = 1
    )
    @GeneratedValue(
        strategy = GenerationType.SEQUENCE,
        generator = "nota_sequence"
    )

    private long id;
    
    @NotNull
    private Integer aviso_id;

    @NotNull
    @Min(1)
    @Max(7)
    private Integer nota;

    public nota(){
    }

    public nota(Integer aviso_id,
                Integer nota){
    
        this.aviso_id = aviso_id;
        this.nota = nota;      
    }

    public long getId(){
        return id;
    }

    public long getAviso_id(){
        return aviso_id;
    }

    public Integer getNota(){
        return nota;
    }

    public static Boolean validateNota(int nota){
        if (nota >= 1 && nota <= 7){
            return true;
        }
        else{
            return false;
        }
    }
}
