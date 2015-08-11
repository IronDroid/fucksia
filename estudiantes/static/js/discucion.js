$(document).on('ready', main_discusiones);

function main_discusiones() {
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});

	$('.dropdown-menu a').on('click', enviar_comentario);
}

function enviar_comentario(data) {
	var input = $('#crear-comentario input:visible');

	if(input.val() != ''){
		$.post('guardar-comentario/', 
			{comentario: input.val(), 
				sigla: data.currentTarget.innerHTML }, 
			actualizar_comentarios);
	}
}

function actualizar_comentarios (data) {
	var ul = $('#comentarios #ul-comentarios');

	ul.html('');
	$('#crear-comentario input:visible').val('');

	$.each(data.comentarios, function(i, elemento){
		$(elemento).appendTo(ul);
	});
}

function cargar_respuestas(data) {
	console.log(data.currentTarget);
	var id = $(data.currentTarget).data('id');

	$.get('cargar-respuestas/' + id, mostrar_respuestas);
}

function mostrar_respuestas (data) {
	var respuestas = $('#respuestas');

	respuestas.html('');


	var comentario = $('#comentarios a[data-id="' + data.comentario + '"]').html();

	var div = $('<div>');

	$('<a class="regresar">').html('Regresar').appendTo(div);

	div.append('<p data-id="' + data.comentario + '">' + comentario + '</p>');

	$('<a class="responder">').html('Responder').appendTo(div).on('click', responder);

	div.appendTo(respuestas);

	
	var ul = $('<ul>')

	$.each(data.respuestas, function(i, elemento){
		$('<li>').html(elemento).appendTo(ul);
	});

	ul.appendTo(respuestas);

	$('#comentarios').css('right', '-110%');
	respuestas.css('right', '0');

	respuestas.on('click', '.regresar', function(){
		respuestas.css('right', '-110%');
		$('#comentarios').css('right', '0');
	});

}

function responder(data) {
	var div = $('<div id="responder">');

	$('<textarea placeholder="Escribe tu respuesta">').appendTo(div);
	$('<button>').html('Enviar Respuesta').appendTo(div).on('click', enviar_respuesta);

	$('#respuestas div:first').after(div);
}

function enviar_respuesta() {
	var respuesta = $('#responder textarea');

	if(respuesta.val() != ''){
		$.post(
			'guardar-respuesta/', 
			{ respuesta: respuesta.val(), comentario: $('#respuestas p').data('id') }, 
			actualizar_respuestas
		);
	}
}

function actualizar_respuestas(data) {
	var ul = $('#respuestas ul');

	ul.html('');

	$.each(data.respuestas, function(i, elemento){
		$('<li>').html(elemento).appendTo(ul);
	});

	$('#responder').remove();
}