$(document).ready(function() {
	var table = $('.webscaleMongo').DataTable()
	table.destroy()
	$.ajax({
		url: '/webscaleMongo',
		data: $('form').serialize(),
		type: 'POST',
		dataType: 'json',
		success: function(data){
			$('.webscaleMongo').remove()
			$("<table class='webscaleMongo' class='display' cellspacing='0' width='100%'>"
		    +"<thead>"
		    +"<tr>"
		    +"<th>ScreenName</th>"
		    +"</tr>"
		    +"</thead>"
		    +"<tbody>").appendTo('#webscaleMongoTable');		
		    table = $('.webscaleMongo').DataTable({
		    	"data": data.success,
	    		"columns": [
			        { "data": "ScreenName" }
	    		]
			});
			console.log(data);
		},
		error: function(error){
			console.log(error);
		}
	});
});
