// $("h1").click(function(){
//   $("h1").hide();
// });

// $(document).ready(function(){
//   $("h1").click(function(){
//     $(this).hide();
//   });
// });


// WORKING
// $(document).ready(function(){
//   $(document).on("click", "#table", function(){
//     $(this).hide();
//   });
// });

// $(document).ready( function () {
//     $('#table').DataTable();
// } );


// $(function(){
//     $('#table').DataTable();
// });

// $(document).ready(function(){
// 	$(document).on("click", "tbody tr:first", function(){
// 		$("*").show();
// 	});
// });


// WORKING
// $(document).ready(function(){
// 	$(document).on("click", "tbody tr:eq(1)", function(){
// 		$("tbody tr:nth-child(1n+3)").slideToggle(1000);
// 	});
// });


// $('tbody tr').eq(0).click(function(){
//     $(this).next().slideToggle(1000);
// });


// alert('If you see this alert, then your custom JavaScript script has run!')

// function changeMarker(){
// 	if(this.textContent === ''){
// 		this.textContent = 'X';
// 	}else if (this.textContent === 'X'){
// 		this.textContent = 'O'
// 	}esle {
// 		this.textContent = ''
// 	}
// }

// for (var i = 0; i <  squares.length; i++) {
// 	 squares[i].addEventLIstener('click', changeMarker)
// }


// -----
// JavaScript
// var rows = document.querySelectorAll('tr')
// var ds = {}

// for (var i = 1; i < rows.length; i++) {
// 	var domain = rows[i].querySelectorAll('td')[0].textContent
// 	var subdomain = rows[i].querySelectorAll('td')[1].textContent
// }

// jQuery
$(document).ready(function(){  
	setTimeout(function() {
	console.log('Loaded')
	var ds = {}
	var rows = $('tr')
	console.log(rows)

	for (var i = 1; i < rows.length; i++){
		var domain = rows.eq(i).find('td').eq(0).text()
		var subdomain = rows.eq(i).find('td').eq(1).text()
		if (subdomain == ''){
			ds[domain] = []
		}esle:{
			ds[domain].push(i)
		}
	}
	console.log(ds)

	function createToggle(domain, start, end){
		// Add + to domain rows
		$('tr').eq(domain).append('<td>+</td>');
		// Hide all subdomains
		$("tr").slice(start, end).addClass('hidden');
		// Toggle hide show/hide on click
		$('tr').eq(domain).find('td').slice(-1).click(function(){

		// Switch + to - on click
			if ($(this).text() == '+') {
				$(this).text('-')
			}else{
				$(this).text('+')
			}
			
			$("tr").slice(start, end).css('background-color', 'rgb(229, 229, 229)')
			$("tr").slice(start, end).toggleClass('hidden');
	})};

	function checkPageStatus(){
		for (var key in ds){
		var domainrow = $('tr').eq(ds[key][0])
		var domainstatuscol = domainrow.find('td').eq(3)
		$.each(ds[key], function( index, value ) {
			console.log( index + ": " + value )
			var subdomainrow = $('tr').eq(value)
			var subdomainstatuscol = subdomainrow.find('td').eq(3)

			var mainAlertCss = {'background-color': 'red',
								'color': 'white'
			};

			if (domainstatuscol.text() !== '200') {
				domainstatuscol.css(mainAlertCss)
			}
			if (subdomainstatuscol.text() !== '200') {
				domainstatuscol.css('background-color', 'pink')
				subdomainstatuscol.css(mainAlertCss)
			}
		})
	}}

	for (var key in ds){
		// Hide columns if there are subdomains
		if (ds[key].length > 1) {
			createToggle(ds[key][0], ds[key][1], ds[key].slice(-1)[0]+1);
		}
	}
	setInterval(checkPageStatus, 1000);

}, 1000);
});
