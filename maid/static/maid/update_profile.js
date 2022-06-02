$(document).ready(function () {
  $(".button_edit").click(function (event) {
	console.log("Clicked On Edit Button")
	var id;
	id = $(this).attr("current_maid_id");
	$.ajax({
		type : "GET",
		url: 'update_maid_profile/'+id,
		success :function(response){
			$("#card-body").html(response);
		}
	})
  });

  $('#submit').click(function(){
	const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
	var maid_id =$("#update_profile_form").data("id"); 
	var form = $("form");
	$.ajax({
		type : "POST",
		url: 'update_maid_profile/'+maid_id,
		headers:{'X-CSRFToken':csrftoken},
		data:form.serialize(),
		success:function(data){
			location.reload();
		}
	})
  });
});