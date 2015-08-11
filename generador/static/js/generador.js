$(document).on('ready', main);

function main() {
    $('.materia .sigla').on('click', div_materia);
}

function div_materia (data) {
    var paralelos = $('.'+data.currentTarget.innerHTML);
    paralelos.each(function (i, e) {
        if (e.checked) {
            e.checked = false;
        } else{
            e.checked = true;
        };
    })
}

function getMateriasP() {
    var simbolos = new Array();
    var checkbox = $('#materias input');
    checkbox.each(function (index, domEle) {
        if ($(domEle)[0].checked) {
            simbolos.push($(domEle)[0].value)
        }
    });
    console.log($('.loader'));
    $('.loader').css({'display':'block'});
    console.log('GET');
    $.get('generar/', 
        {lista: simbolos.join(";")}, 
        resCombi);
}

function resCombi(data) {
    if (data.null) {
        $('.loader').css({'display':'none'});
        return;
    };
    var lists = data.listgen;
    $(".wrap .wrap_gen").remove()
    $(".wrap .div_res").remove()
    var wrap = $(".wrap");
    var divRes = $(document.createElement("div"));
    divRes.text("Horarios Generados: " + lists.length +" en "+ data.runtime + " segs");
    divRes.attr('class', 'div_res');
    wrap.append(divRes);
    var sectionM = $(document.createElement("section"));
    sectionM.attr("class", "wrap_gen");

    
    // lista de horarios combinados
    for (var i = 0; i < lists.length; i++) {
        // horarios
        var sectionH = $(document.createElement("section"));
        sectionH.css('box-shadow', '');
        var horario = lists[i];
        // cada item es un dia del horario
        var header = $(document.createElement("article"));
        header.attr("class", "rowgen");
        var div = $(document.createElement("div"));
        div.attr("class", "header");
        div.text(" ");
        header.append(div);
        div = $(document.createElement("div"));
        div.attr("class", "header");
        div.text("Lunes");
        header.append(div);
        div = $(document.createElement("div"));
        div.attr("class", "header");
        div.text("Martes");
        header.append(div);
        div = $(document.createElement("div"));
        div.attr("class", "header");
        div.text("Miércoles");
        header.append(div);
        div = $(document.createElement("div"));
        div.attr("class", "header");
        div.text("Jueves");
        header.append(div);
        div = $(document.createElement("div"));
        div.attr("class", "header");
        div.text("Viernes");
        header.append(div);
        div = $(document.createElement("div"));
        div.attr("class", "header");
        div.text("Sábado");
        header.append(div);
        sectionH.append(header);
        for (var j = 0; j < horario.length; j++) {
            var article = $(document.createElement("article"));
            article.attr("class", "rowgen");
            var dia = horario[j];
            var div_hora = $(document.createElement("div"));
            div_hora.attr("class", "header");
            div_hora.text((8 + (j * 2)) + " - " + (10 + (j * 2)));
            article.append(div_hora);
            // cada item es una hora de clase
            for (var k = 0; k < dia.length; k++) {
                var div = $(document.createElement("div"));
                div.attr("class", "dia");
                hora = dia[k];
                if (hora.length > 1) {
                    div.attr("class", "hora");
                };
                div.text(hora);
                article.append(div);
            };
            sectionH.append(article);
        };
        sectionM.append(sectionH);
    };
    wrap.append(sectionM);
    $('.loader').css({'display':'none'});
}