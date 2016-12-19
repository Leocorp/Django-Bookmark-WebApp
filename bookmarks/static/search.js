/**
 * Created by eph on 16/12/16.
 */
function search_submit()
{
    var query = $('#id_query').val();
    if (!query.empty)
    {
        //$('#search-results').load();
        $.get("?ajaxquery="+encodeURIComponent(query), function(data)
        {
            if ($(data).has("ul.bookmarks"))
            {
                var page = $(data).find("ul").prevObject[0];
                var output = page;
                //console.log(output);
                $('#search-results').html(output);
            }


        });
        //console.log(query);
        return false;
    }
}

$(document).ready(
    function(){
        /*$('#search-form').submit(search_submit);*/

        $('#id_query').keyup(function(){
            search_submit();
        });
    }
);
