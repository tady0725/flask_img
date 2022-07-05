function showImg(thisimg) {
	var file = thisimg.files[0];
	if(window.FileReader) {
		var fr = new FileReader();
		
		var showimg = document.getElementById('showimg');
		fr.onloadend = function(e) {
		showimg.src = e.target.result;
	};
	fr.readAsDataURL(file);
	showimg.style.display = 'block';
	}
}
function showImg2(thisimg) {
	var file = thisimg.files[0];
	if(window.FileReader) {
		var fr = new FileReader();
		
		var showimg = document.getElementById('showimg2');
		fr.onloadend = function(e) {
		showimg2.src = e.target.result;
	};
	fr.readAsDataURL(file);
	showimg2.style.display = 'block';
	}
}
// function sub() {  
// 	$.ajax({  
// 			cache: true,  
// 			type: "POST",  
// 			url:"http://210.70.175.13:5000/processes",  
// 			data:$('#formId').serialize(),// 你的formid  
// 			async: false,  
// 			error: function(request) {  
// 				alert("Connection error:"+request.error);  
// 			},  
// 			success: function(response) {  
			  
// 			  $("#q1").html(response);
// 				 $("#q3").html(response);
// 				 $( "#q2" ).html(response);
			
				 
			   

// 				//alert("SUCCESS!");  
// 			}  
		   
// 		});   
// 	}