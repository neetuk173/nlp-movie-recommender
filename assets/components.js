
/*
|------------------------------------------------------------------------------
| Splash Screen
|------------------------------------------------------------------------------
*/

myApp.onPageInit('splash-screen', function(page) {

	$( "#panel-container" ).hide();
	new Vivus('logo', {
		duration: 4,
		onReady: function(obj) {
			obj.el.classList.add('animation-begin');
		}
	},
	function(obj) {
		obj.el.classList.add('animation-finish');

		/* 10 milliseconds AFTER logo animation is completed, open login screen. */
		setTimeout(function(){
			
			mainView.router.load({
				url: 'movies.php'
			});
			
		}, 2000);
	});
});


myApp.onPageInit('movies', function(page) {
    
	$('#waitnotice').hide();
	$('#sigma-container').hide();
    $('#variant-name').text("Local datasets");
    
    var variant = "Local datasets";
    var title = "";

    $('#clear').on('click', function(e)
    {
        myApp.addNotification({
            message: 'Clearing page...',
            hold: 2500,
            button: {
            text: '<i class="material-icons">rotate_right</i>'
            }
        });
        setTimeout(function()
		{
			mainView.router.refreshPage();
		}, 500);
    });

    $('#asaprecommend').on('click', function(e)
    {
        $("input[name='radio']").prop('checked',false);
        title = encodeURIComponent($('#vertex').val().trim());
	    $('#moviename').text($('#vertex').val());

        
        //  Run FastAPI with the command:
        //     python -m uvicorn IMDB:app --host 0.0.0.0 --port 8000
        //
        //  by changing to directory with IMDB.py file first

        api_url = "http://127.0.0.1:8000/movies/"+title;



        if (title.length>1){
          let xmlHttpReq = new XMLHttpRequest();
          try {
            xmlHttpReq.open("GET", api_url, false); 
            xmlHttpReq.send(null)
            console.log(xmlHttpReq.responseText);

            {
                reco_obj = JSON.parse(xmlHttpReq.responseText);
                const valuesOnly = Object.values(reco_obj["title"]);
                var counter = 1;
                valuesOnly.forEach( movietitle => {
                    $('.title'+counter).text(movietitle);
                    $('.title'+counter).parents().eq(1).children('input[type=radio]').attr("value",movietitle);
                    counter++;
                    //console.log(movietitle);
                });
                $('#sigma-container').show();
                $('#vertex').val("");
            }    
          } 
          catch (text) {
            var l = xmlHttpReq.responseText.length;
            if (l == 0)
                {
                    var toast = myApp.toast('No such movie in the dataset!', '<i class="material-icons">motorcycle</i>');
			        toast.show();
                    $('#sigma-container').hide();
                }
          }

        }
        else
        $('#sigma-container').hide();
    });

    $("input[name='radio']").change(function(){
        $('#vertex').val($(this).val())
    });


});
