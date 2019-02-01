// jQuery
$(document).ready(function(){
	setTimeout(function() {
	var ds = {}
	var rows = $('tr')

	function indexOfColumnByName(name){
		var columns = $('tr').eq(0).find('th')
		var ind = ''
		$.each(columns, function( index, value ) {
			if (value.textContent === name) {
				ind = index

			}
		})
		return ind;
	}


	for (var i = 1; i < rows.length; i++){
		var domain = rows.eq(i).find('td').eq(indexOfColumnByName('domain_name')).text()
		var subdomain = rows.eq(i).find('td').eq(indexOfColumnByName('subdomain_name')).text()
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

	for (var key in ds){
			// Hide columns if there are subdomains
			if (ds[key].length > 1) {
				createToggle(ds[key][0], ds[key][1], ds[key].slice(-1)[0]+1);
		}
	}

	function addLinksToTitleId(i){
			var titleidcol = rows.eq(i).find('td').eq(indexOfColumnByName('title_id'))
			var link = "/archive/title_id=" + titleidcol.text()
			$(titleidcol).click(function(){
				window.open(link,'_blank')
			});
	}

	for (var i = 1; i < rows.length; i++){
		addLinksToTitleId(i)
	}


	function addAlerts(){
		var mainAlertCss = {'background-color': 'red',
							'color': 'white'};

		var subdomainAlertCss = {'background-color': 'pink',
								'color': 'black'};

		for (var key in ds){
		var domaincols = $('tr').eq(ds[key][0]).find('td')
		domaincols.removeAttr('style')
		var domain_status = domaincols.eq(indexOfColumnByName('status'))
		var domain_traffic = domaincols.eq(indexOfColumnByName('traffic'))
		var domain_fd = domaincols.eq(indexOfColumnByName('fd'))
		var domain_pkh = domaincols.eq(indexOfColumnByName('pkh'))

		if (domain_status.text() !== '200') {
			domain_status.css(mainAlertCss)
		}
		if (domain_traffic.text().indexOf('▼▼') > -1){
			domain_traffic.css(mainAlertCss)
		}
		if (domain_fd.text().indexOf('▼▼') > -1){
			domain_fd.css(mainAlertCss)
		}
		if (domain_pkh.text() !== 'ok'){
			domain_pkh.css(mainAlertCss)
		}

		$.each(ds[key].slice(1,), function( index, value ) {
			var subdomaincols = $('tr').eq(value).find('td')
			subdomaincols.removeAttr('style')
			subdomaincols.css('background-color', 'rgb(229, 229, 229)')
			var subdomain_status = subdomaincols.eq(indexOfColumnByName('status'))
			var subdomain_traffic = subdomaincols.eq(indexOfColumnByName('traffic'))
			var subdomain_fd = subdomaincols.eq(indexOfColumnByName('fd'))
			var subdomain_pkh = subdomaincols.eq(indexOfColumnByName('pkh'))


			// STATUS ALERT
			if (subdomain_status.text() !== '200') {
				domain_status.css(subdomainAlertCss)
				subdomain_status.css(mainAlertCss)
			}
			if (domain_status.text() !== '200') {
				domain_status.css(mainAlertCss)
			}

			// TRAFFIC DROP ALERT
			if (subdomain_traffic.text().indexOf('▼▼') > -1) {
				domain_traffic.css(subdomainAlertCss)
				subdomain_traffic.css(mainAlertCss)
			}
			if (domain_traffic.text().indexOf('▼▼') > -1){
				domain_traffic.css(mainAlertCss)
			}

			// FD DROP ALERT
			if (subdomain_fd.text().indexOf('▼▼') > -1){
				domain_fd.css(subdomainAlertCss)
				subdomain_fd.css(mainAlertCss)
			}
			if (domain_fd.text().indexOf('▼▼') > -1){
				domain_fd.css(mainAlertCss)
			}

			// PKH alert
			if (subdomain_pkh.text() !== 'ok'){
				domain_pkh.css(subdomainAlertCss)
				subdomain_pkh.css(mainAlertCss)
			}
			if (domain_pkh.text() !== 'ok'){
				domain_pkh.css(mainAlertCss)
			}


			// REPLACE TWO ARROWS WITH ONE ARROW DOESNT WORK
			// subdomain_traffic.text(subdomain_traffic.text().replace('▼▼', '▼'))
			// subdomain_fd.text(subdomain_fd.text().replace('▼▼', '▼'))

		})
		// domain_traffic.text(domain_traffic.text().replace('▼▼', '▼'))
		// domain_fd.text(domain_fd.text().replace('▼▼', '▼'))
	}}



	function getColumnName(index){
		return $('tr').eq(0).find('th').eq(index).text()
	}


	setInterval(addAlerts, 100);
	// makeInfo()
	// setInterval(makeInfo, 1000);

}, 1000);
});



// #jquery imitate link click
// $("#google_link_proxy").click(function(event){
//     window.open($("#google_link").attr('href'),'_blank')
// });

// $(goo).click(function(event){
//     window.open("htttp://google.com",'_blank')
// });

// $(goo).click(function(event){
//     window.open("/page1",'_blank')
// });


// // jquery create link
// var thelink = $('<a>',{
//     text: 'linktext',
//     title: 'some title',
//     href: 'somelink.html'
// }).appendTo('body');


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