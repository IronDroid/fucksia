$(document).on('ready', main);

function main (data) {

	$('input').on('click', get_materia);

    $('#clean_horario').on('click', clean_horario);

    $('.periodo').hover(hover_on,hover_off);

    $.get('inscripcion/', show_materia);
};

function get_materia(data) {
	value = data.target.value;
	$.get('materia/', 
		{materia: value}, 
		show_materia);
}
function show_materia (data) {
    var per = data.periodos;
    if (data.mat != '') {
        limpiar_materia(data.mat);
    };
    $.each(per, function(i, elemento){
        var id_per = elemento.per;
        var tile = $('#'+id_per);
        var offset = tile.offset();
        create_popup(id_per);
        $('#info'+id_per+' h4').text(elemento.nombre_materia);
        $('#info'+id_per+' h6').text(elemento.nombre_docente);
        $('#info'+id_per+' h5').text(elemento.aula);
        var css = {
            'background': '#ffd740',
            'position': 'absolute',
            'display':'none',
            'left': offset.left,
            'top': offset.top - $('#info'+id_per).height(),
            'width': tile.width() + 16
        }
        $('#info'+id_per).css(css);

        if (tile.text().length > 1) {
            tile.text(tile.text() + ' ' + elemento.sigla);
            tile.css({'background': '#E74C3C'});
        } else{
            tile.text(elemento.sigla);
            tile.css({'background': '#2ECC71'});
        };
    })
}
function limpiar_materia (materia) {
    var per = $('.periodo');
    for (var i = 0; i < per.length; i++) {
        var mats = per[i].innerHTML.split(" ");
        if (mats[0] != "&nbsp;") {
            if (mats.length > 1) {
                var cad = "";
                for (var j = 0; j < mats.length; j++) {
                    if (materia != mats[j]) {
                        cad = cad + ' ' + mats[j];
                    };
                };
                per[i].innerHTML = cad.trim();
                if (per[i].innerHTML.split(" ").length == 1) {
                    per[i].setAttribute('style', 'background: #2ECC71;');
                }
            } else {
                if (materia == mats[0]) {
                    per[i].innerHTML = "&nbsp;";
                    per[i].removeAttribute("style");
                };
            };
        };
    };
}

function hover_on (data) {
    id_per = data.currentTarget.id
    var offset = $('#'+id_per).offset();
    var tile = $('#'+id_per);
    if (tile.text().length > 1) {
        var css = {
            'display':'inline',
            'left': offset.left,
            'top': offset.top - $('#info'+id_per).height(),
            'width': tile.width() + 16
        }
        $('#info'+id_per).css(css);
    }
}
function hover_off (data) {
    $('#info'+data.currentTarget.id).css("display","none");
}

function clean_horario () {
    var per = $('.periodo');
    $.each(per, function(i, elemento){
        per[i].innerHTML = '&nbsp;';
        per[i].removeAttribute("style");
    });
}

function create_popup (id) {
    if (document.getElementById('info'+id) == null) {
        var div = $(document.createElement('div'));
        var nombre = $(document.createElement('h4'));
        var docente = $(document.createElement('h6'));
        var aula = $(document.createElement('h5'));
        div.append(nombre);
        div.append(docente);
        div.append(aula);
        div.attr('id','info'+id);
        $('#info_popup').append(div);
    };
}
