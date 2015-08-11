$(document).on('ready', main_discusiones);

function main_discusiones() {
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "POST"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});

	$('#buttonconfig').on('click', waiting);
	$('#buttonconfig').on('click', sia_scrap)

	$('#buttonupdate').on('click', waiting);
	$('#buttonupdate').on('click', update_scrap)
}

function sia_scrap() {
	var sia_frame = $('#sia_frame');
	var sia_url = sia_frame.attr('src');
	$.post('scraper/', 
		{siaurl: sia_url}, 
		scraperjs);
}

function update_scrap() {
	var sia_frame = $('#sia_frame');
	var sia_url = sia_frame.attr('src');
	$.post('scraper/', 
		{siaurl: sia_url}, 
		update_scraperjs);
}

function waiting () {
	$('.loader').css({'display':'block'});
	console.log($('.loader'));
	var h5 = $('#config h5');
	h5.text('Extrayendo información.\nEsto puede tardar varios minutos, espera ;)');
	$("#buttonconfig").attr("disabled", true);
}

function scraperjs (data) {
    console.log(data);
    if (data.save) {
        $('#config h5').html('');
        $('#config h4').html('');
        $('#config h3').html('');
        var cambio = {
            display: "none"
        }
        // $("iframe").css(cambio);
        // $("#buttonconfig").css(cambio);
        var subtitle = $("#config");
        subtitle.append('<h3>Felicidades eres un genio.</h3>');
        subtitle.append('<h3>Ya estas listo para disfrutar de esta nueva  plataforma.</h3>');
        subtitle.append('<h3>Dale F5!! FuckSIA!!!</h3>');
    } else {
        $("#buttonconfig").attr("disabled", false);
        var h5 = $('#config h5');
		h5.text('Al parecer hay problemas con el SIA. Vuelve a intentarlo ;)');
    };
	$('.loader').css({'display':'none'});
}

function update_scraperjs (data) {
    console.log(data);
    if (data.save) {
        $('#config h5').html('');
        $('#config h4').html('');
        $('#config h3').html('');
        var cambio = {
            display: "none"
        }
        $("iframe").css(cambio);
        $("p").css(cambio);
        $("#buttonupdate").css(cambio);
        var subtitle = $("#config");
        subtitle.append('<h3>Imprecionante! Ya tienes todos tus datos actualizados.</h3>');
        subtitle.append('<h3>Puedes continuar disfrutando esta plataforma. FuckSIA!!!</h3>');
    } else {
        $("#buttonconfig").attr("disabled", false);
        var h5 = $('#config h5');
		h5.text('Al parecer hay problemas con el SIA. Vuelve a intentarlo ;)');
    };
	$('.loader').css({'display':'none'});
}