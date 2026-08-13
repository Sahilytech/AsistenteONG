"""Sistema visual único, adaptativo y orientado a una interfaz moderna."""
COLORS={
 "background":("#F7FBFD","#080D12"),"surface":("#FFFFFF","#0E171E"),"surface_alt":("#EEF6F9","#111E26"),"surface_blue":("#E7F6FC","#102B38"),
 "primary":("#0E98D6","#36B7ED"),"primary_dark":("#0879AD","#1689BA"),"primary_soft":("#DDF2FB","#173B4C"),"primary_pale":("#F3FAFD","#0D202A"),
 "text":("#101820","#F4F8FA"),"text_muted":("#657780","#91A5AF"),"text_soft":("#87969E","#71858F"),"border":("#D6E6EC","#213640"),"border_strong":("#BDD3DC","#34505D"),
 "success":("#168A4A","#49C58A"),"success_soft":("#E9F7EF","#123629"),"warning":("#B86A00","#F0B35A"),"warning_soft":("#FFF4E5","#3D2E19"),"danger":("#C62828","#FF7373"),"danger_soft":("#FDECEC","#432020")}
FONTS={"display":("Helvetica",28,"bold"),"title":("Helvetica",21,"bold"),"heading":("Helvetica",15,"bold"),"subheading":("Helvetica",12,"bold"),"body":("Helvetica",11),"body_bold":("Helvetica",11,"bold"),"small":("Helvetica",9),"small_bold":("Helvetica",9,"bold"),"tiny":("Helvetica",8)}
SPACING={"xs":5,"sm":9,"md":14,"lg":20,"xl":28,"xxl":36}; CARD_RADIUS=16; BUTTON_HEIGHT=38

def switch_theme(theme:str):
    """Mantiene compatibilidad: CustomTkinter resuelve los pares claro/oscuro."""
    return COLORS
