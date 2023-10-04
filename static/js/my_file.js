function get_search(){
            var search=$('input[name=search_field]').val();
            if (search != '')
            {
                if(search=parseInt(search)){
                  window.location.href='http://127.0.0.1:8000/detail/'+search
                }
                else{
                    search=$('input[name=search_field]').val();
                 window.location.href='http://127.0.0.1:8000/search/'+search;
                }
            }
        }