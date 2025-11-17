package com.Tarea4.Tarea4.models;


public class AvisoEvaluacionDto {
    
    private long id;
    private String fechaPublicacion; 
    private String sector;
    private String descripcionMascota; 
    private String comunaNombre; 
    private String notaPromedio; 

    
    public AvisoEvaluacionDto(aviso_adopcion aviso, String comunaNombre ,Double promedio) {
        this.id = aviso.getId();
        this.fechaPublicacion = aviso.getFecha_ingreso().toLocalDate().toString(); 
        this.sector = aviso.getSector();
        
        
        this.descripcionMascota = aviso.getCantidad() + " " + 
                                  aviso.getTipo().name() + " " + 
                                  aviso.getEdad() + " " + 
                                  aviso.getUnidad_medida().name();
        
        this.comunaNombre = comunaNombre;
        
        
        if (promedio == null) {
            this.notaPromedio = "-";
        } else {
            this.notaPromedio = String.format("%.2f", promedio);
        }
    }

    
    public long getId() { return id; }
    public String getFechaPublicacion() { return fechaPublicacion; }
    public String getSector() { return sector; }
    public String getDescripcionMascota() { return descripcionMascota; }
    public String getComunaNombre() { return comunaNombre; }
    public String getNotaPromedio() { return notaPromedio; }

}
