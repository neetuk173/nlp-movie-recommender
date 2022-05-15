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
    
    var variant = "IMDB";
    var title = "";

	$('#waitnotice').hide();
	$('#sigma-container').hide();
    $('#variant-name').text(variant);

    $('#IMDB').on('click', function(e)
    {
        variant = "IMDB";
        $('#variant-name').text(variant);
    });
    $('#Hulu').on('click', function(e)
    {
        variant = "Hulu";
        $('#variant-name').text(variant);
    });

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

        api_url = "http://localhost:8000/"+variant.toLowerCase()+"/"+title;

        if (title.length>1){
          let xmlHttpReq = new XMLHttpRequest();
          var listhtml = " ";
          try {
            xmlHttpReq.open("GET", api_url, false); 
            xmlHttpReq.send(null)
            console.log(xmlHttpReq.responseText);
            var titles = JSON.parse(xmlHttpReq.responseText);
            for (let title in titles) {
                listhtml += '<li><label class="label-radio item-content"><input type="radio" name="radio" value="'+titles[title]+'"><span class="item-media"><i class="icon icon-form-radio"></i></span><span class="item-inner"><span class="item-title">'+titles[title]+'</span></span></label></li>';
            }
            
            $('#titlelist').html(listhtml);
            $('#sigma-container').show();
            $('#vertex').val("");
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

    $('#titlelist').delegate("input[name='radio']", "click", function(){
        $('#vertex').val($(this).val())
    });

});
