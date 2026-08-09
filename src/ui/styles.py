"""Sistema visual de Asistente ONG: claro, limpio, moderno y accesible."""
COLORS={
 "background":"#FFFFFF","surface":"#FFFFFF","surface_alt":"#F5FAFD","surface_blue":"#EEF8FC",
 "primary":"#0e98d6","primary_dark":"#0879ad","primary_soft":"#DFF3FB","primary_pale":"#F5FBFE",
 "text":"#111111","text_muted":"#65727B","text_soft":"#89949B","border":"#D9E5EA","border_strong":"#C4D6DE",
 "success":"#168A4A","success_soft":"#E9F7EF","warning":"#B86A00","warning_soft":"#FFF4E5","danger":"#C62828","danger_soft":"#FDECEC",
}
FONTS={
 "display":("Helvetica",28,"bold"),"title":("Helvetica",21,"bold"),"heading":("Helvetica",15,"bold"),
 "subheading":("Helvetica",12,"bold"),"body":("Helvetica",11),"body_bold":("Helvetica",11,"bold"),
 "small":("Helvetica",9),"small_bold":("Helvetica",9,"bold"),"tiny":("Helvetica",8),
}
SPACING={"xs":5,"sm":9,"md":14,"lg":20,"xl":28,"xxl":36}
CARD_RADIUS=16
BUTTON_HEIGHT=38


def switch_theme(theme:str):
    """Compatibilidad: el producto utiliza exclusivamente modo claro."""
    return COLORS
