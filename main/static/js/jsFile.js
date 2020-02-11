window.onload = function() {
	document.getElementById('belgium').style.display = 'block';
	if(localStorage.getItem('popState') != 'shown'){
		document.getElementById('popupID').style.display = 'block';
		load()
		localStorage.setItem('popState','shown')
	}
	setTimeout(fade, 3000)
	changeDisp()
};

function load() {
	document.getElementById('country').onclick = function() {
		this.style.display = 'none';
	};
};

function fade() {
  $('#appear.textBlock').fadeIn();
};

function changeDisp() {
     $(".country").hover( 
     	function() {
        	$(".upperBar").css("height", "auto");
    	},
        function() {
        	$(".upperBar").css("height", "50px");
     	}
     );
};



