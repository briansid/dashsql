// jQuery
$(document).ready(function(){
	setTimeout(function() {
	var ds = {}
	var rows = $('tr')

	for (var i = 1; i < rows.length; i++){
		var domain = rows.eq(i).find('td').eq(0).text()
		var subdomain = rows.eq(i).find('td').eq(1).text()
		if (subdomain == ''){
			ds[domain] = []
			ds[domain].push(i)
		}else{
			ds[domain].push(i)
		}
	}

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
			var subdomainrow = $('tr').eq(value)
			var subdomainstatuscol = subdomainrow.find('td').eq(3)

			var mainAlertCss = {'background-color': 'red',
								'color': 'white'
			};

			var subdomainAlertCss = {'background-color': 'pink',
									'color': 'black'}


			if (domainstatuscol.text() !== '200') {
				domainstatuscol.css(mainAlertCss)
			}
			else if (subdomainstatuscol.text() !== '200') {
				domainstatuscol.css(subdomainAlertCss)
				subdomainstatuscol.css(mainAlertCss)
			}
			else{
				domainstatuscol.removeAttr("style")
				subdomainstatuscol.removeAttr("style")
			}
		})
	}}

	function getColumnName(index){
		return $('tr').eq(0).find('th').eq(index).text()
	}

	for (var key in ds){
		// Hide columns if there are subdomains
		if (ds[key].length > 1) {
			createToggle(ds[key][0], ds[key][1], ds[key].slice(-1)[0]+1);
		}
	}
	setInterval(checkPageStatus, 1000);
	// makeInfo()
	// setInterval(makeInfo, 1000);

}, 1000);
});



	// function makeInfo(){
	// 	for (var key in ds){
	// 		var problems = []
	// 		var domainrow = $('tr').eq(ds[key][0])
	// 		var domaincols = $(domainrow).find('td')
	// 		$.each(domaincols, function( colindex, col ) {
	// 			var colcolor = $(col).css("background-color")
	// 				if (colcolor == "rgb(255, 0, 0)"){
	// 					var colname = getColumnName(colindex)
	// 					var coltex = $(col).text()
	// 					var problem = {
	// 						'level': 'domain',
	// 						'name': colname,
	// 						'problem': coltex,
	// 					}
	// 					problems.push(problem)
	// 					// $(domaincols).eq(7).append(JSON.stringify(problem))
	// 				}
	// 			})
	// 		if (ds[key].length > 1){
	// 		$.each(ds[key], function( index, value ) {
	// 			var subdomainrow = $('tr').eq(value)
	// 			var subdomaincols = $('tr').eq(value).find('td')
	// 			$.each(subdomaincols, function( colindex, col ) {
	// 				var colcolor = $(col).css("background-color")
	// 				if (colcolor == "rgb(255, 0, 0)"){
	// 					var colname = getColumnName(colindex)
	// 					var coltex = $(col).text()
	// 					var problem = {
	// 						'level': 'subdomain',
	// 						'name': colname,
	// 						'problem': coltex,
	// 					}
	// 					problems.push(problem)
	// 					// $(domaincols).eq(7).append(JSON.stringify(problem))
	// 				}
	// 		})


	// 	})}
	// 	if (problems.length){
	// 		var domainProblem = false
	// 		var infocol = $(domaincols).eq(7)
	// 		console.log(problems)
	// 		for (var problem in problems){
	// 			console.log(problem)
	// 			if (problem['level'] == 'domain')
	// 				domainProblem = true
	// 				break;
	// 		}
	// 		console.log(domainProblem)
	// 		infocol.text('')
	// 		infocol.append(JSON.stringify(problems))
	// 		if (domainProblem){
	// 			var mainAlertCss = {'background-color': 'red',
	// 								'color': 'white'}
	// 			var subdomainAlertCss = {'background-color': 'pink',
	// 								'color': 'black'}
	// 			infocol.css(mainAlertCss)
	// 		}else{
	// 			infocol.css(subdomainAlertCss);
	// 		}
	// 	}

	// 	}
	// }



// -----------------
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