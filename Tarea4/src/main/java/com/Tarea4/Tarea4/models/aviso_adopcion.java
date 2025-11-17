package com.Tarea4.Tarea4.models;

import java.time.LocalDateTime;



import jakarta.persistence.Entity;
import jakarta.persistence.Enumerated;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.SequenceGenerator;
import jakarta.persistence.Table;
import jakarta.validation.constraints.NotNull;
import jakarta.persistence.EnumType;





@Entity
@Table
public class aviso_adopcion {

    public enum tiposDeMascota{
        perro, gato
    }

    public enum MoA{
        a,m
    }

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
    private LocalDateTime fecha_ingreso;

    @NotNull
    private Integer comuna_id;

    
    private String sector;

    @NotNull
    private String nombre;

    @NotNull
    private String email;

    private String celular;

    @NotNull
    @Enumerated(EnumType.STRING)
    private tiposDeMascota tipo;

    @NotNull
    private Integer cantidad;

    @NotNull
    private Integer edad;

    @NotNull
    @Enumerated(EnumType.STRING)
    private MoA unidad_medida;

    @NotNull
    private LocalDateTime fecha_entrega;

    private String descripcion;

    public aviso_adopcion(){
    }

    public aviso_adopcion(LocalDateTime fecha_ingreso,
                          Integer comuna_id,
                          String sector,
                          String nombre,
                          String email,
                          String celular,
                          tiposDeMascota tipo,
                          Integer cantidad,
                          Integer edad,
                          MoA unidad_medida,
                          LocalDateTime fecha_entrega,
                          String descripcion){
        
        this.fecha_ingreso = fecha_ingreso;
        this.comuna_id = comuna_id;
        this.sector = sector;
        this.nombre = nombre;
        this.email = email;
        this.celular = celular;
        this.tipo = tipo;
        this.cantidad = cantidad;
        this.edad = edad;
        this.unidad_medida = unidad_medida;
        this.fecha_entrega = fecha_entrega;
        this.descripcion = descripcion;
        }

        public long getId(){
            return  id;
        }

        public LocalDateTime getFecha_ingreso(){
            return fecha_ingreso;
        }

        public Integer getComuna_id(){
            return comuna_id;
        }

        public String getSector(){
            return sector;
        }

        public String getNombre(){
            return nombre;
        }

        public String getEmail(){
            return email;
        }

        public String getCelular(){
            return celular;
        }

        public tiposDeMascota getTipo(){
            return tipo;
        }

        public Integer getCantidad(){
            return cantidad;
        }

        public Integer getEdad(){
            return edad;
        }

        public MoA getUnidad_medida(){
            return unidad_medida;
        }

        public LocalDateTime getFecha_entrega(){
            return fecha_entrega;
        }

        public String getDescripcion(){
            return descripcion;
        }


}
