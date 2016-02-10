$(document).on('ready', main_record);

function main_record() {
	// $(".mat-a").on("mouseover", function () {
 //    	$.get('recorrido/', {sigla: $(this).data("sigla")}, callback_grafo);
	// });

	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if(settings.type == "GET"){
				xhr.setRequestHeader("X-CSRFToken", $('[name="csrfmiddlewaretoken"]').val());
			}
		}
	});
}

function callback_grafo (data) {
	console.log($(data).attr("sigla_mat"));
	var grafo = $(data).attr("sigla_mat");
	$.each(grafo, function () {
		console.log($(this).text());
	});
}