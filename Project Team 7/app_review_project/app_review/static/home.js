$(document).ready(function () {

        // to submit the form
        $("#submit-form").click(function(){
            if($("#exampleDataList").val() == ''){
                alert("Please Select One App!")
                return
            }

            $("#app_data_form").submit();
            // alert("DONE")
        })
        $("#submit-category-form").click(function(){

            if($("#exampleCategoryList").val() == ''){
                alert("Please Select One Category!")
                return
            }

            $("#category_data_form").submit();
        })  


});


    // Make an Ajax call to a URL with the selected option value as a parameter
function ajaxCall(app_name){
    data1 = [
        {"username": "ajay", "date":"22", "review":"eeeeee"}
    ]
    $('#app_datatable').DataTable({
        "info": false,

        /* Set pagination as false or 
        true as per need */
        "paging": false,
        "datesrc":"data",
          
        /* Name of the file source 
        for data retrieval */
        "ajax": "/get_app_review_data",
        "columns": [

            /* Name of the keys from 
            data file source */
            { "data": "username" },
            { "data": "date" },
            { "data": "review" },
  
        ]
    });
}

