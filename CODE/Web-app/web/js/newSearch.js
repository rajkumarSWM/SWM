let selectedValue = 'Diseases';
$(document).ready(function () {

    $('.drugResults').css('display', 'none');
    $("#related_symptoms").css('visibility', 'hidden');

    // add event listener for Enter button to invoke search
    var input = document.getElementById("search_box");
    input.addEventListener("keyup", function(event) {
        // Number 13 is the "Enter" key on the keyboard
        if (event.keyCode === 13) {
            event.preventDefault();
            // Trigger the button element with a click
            sendSearchRequest();
        }
    });

})

function sendSearchRequest() {


    let searchQuery = $('#search_box').val();
    searchQuery = searchQuery.trim();
    // empty search is not allowed, show alert
    let selectedSearchOption = '';
    if(selectedValue==='Diseases'){
        selectedSearchOption = 'disease_search';

    }else{
        selectedSearchOption = 'drug_search';

    }

    if (searchQuery === '') {
        if (selectedValue === 'Diseases') {
            swal( "Empty Search Query" ,  "Please type the symptoms you want to search." ,  "error" );
            return;
        }
        else if (selectedValue === 'Drugs') {
            swal("Empty Search Query", "Please type the disease name you want to search.", "error");
            return;
        }
    }
    ajaxGetRequest('http://localhost:8080/healthcare_mining/' + '/search?query=' + searchQuery + '&type=' + selectedSearchOption, handleSearchResponse)
}


function handleSearchResponse(response) {

    const res = JSON.parse(response);
    if (res != '') {

        if(res.hasOwnProperty('related_symptoms') && res.related_symptoms.length > 0) {
            var newLabel = '<b style="color: white;">Related Symptoms: </b>';
            for (var i = 0; i < res.related_symptoms.length; i++) {
                if (i != 0) {
                    newLabel += ', ';
                }
                newLabel += res.related_symptoms[i];
            }
            $("#related_symptoms").html(newLabel);
             $("#related_symptoms").css('visibility', 'visible');
        }
        else {
             $("#related_symptoms").css('visibility', 'hidden');
        }


        if(selectedValue==='Diseases') {

            $('#forums').empty();
            $('#diseases').empty();

            if(res.results.hasOwnProperty('mayo_clinic')){
                if (res.results.mayo_clinic.length > 0) {
                    var list = "";
                    var displaysize = 10;
                    if (res.results.mayo_clinic.length < displaysize) {
                        displaysize = res.results.mayo_clinic.length
                    }
                    for (var i = 0; i < displaysize; i++) {
                        var item = res.results.mayo_clinic[i];

                        var symptoms = "<b>Symptoms: </b>";
                        if(item.hasOwnProperty('other_symptoms')){
                            console.log("Hello");
                            for (var j = 0; j < item.other_symptoms.length; j++) {
                                if (j != 0) {
                                    symptoms += ", "
                                }
                                const ss = item.other_symptoms[j];
                                var found = false;
                                for (var k = 0; k < res.tagged_symptoms.length; k++) {
                                    console.log(ss)
                                    console.log(res.tagged_symptoms[k])
                                    if (res.tagged_symptoms[k] === ss) {
                                        found = true;
                                        break;
                                    }
                                }
                                if (found) {
                                    symptoms += "<span style='background-color: red'>" + ss + "</span>"
                                }
                                else {
                                    symptoms += ss;
                                }
                            }
                        }

                        list += "<div class='card'>";
                        list += "<h3><a style='text-decoration: none; color: black;' href='" + item.url + "' target='_blank'>" + item.title + "</a></h3>";
                        list += "<br/>";
                        list += "<p>" + item.summary.substring(0, 200) + "...</p>";
                        list += "<br/>";
                        list += "<p>" + symptoms + "</p>";

                        list += "</div>";
                        // list += "<ul>";
                        // list += "<li class='title_li'><a href='" + item.url + "' target='_blank'>" + item.title + "</a></li>";
                        // list += "<ul>";
                        // list += "<li class = 'description'>" + item.summary.substring(0, 200) + "...</li>";
                        // list += "<li class = 'description'>" + symptoms + "</li>";
                        // list += "</ul>";
                        // list += "</ul>";
                        // list += "<hr class='hr_line'>";
                    }
                    setTimeout(function () {
                        $("#diseases").append(list);
                    });
                }
            }

            var list_posts = "";
            if(res.results.hasOwnProperty('web_md_mb')) {
                if (res.results.web_md_mb.length > 0) {
                    var displaysize = 5;
                    if (res.results.web_md_mb.length < displaysize) {
                        displaysize = res.results.web_md_mb.length
                    }
                    for (var i = 0; i < displaysize; i++) {
                        var item = res.results.web_md_mb[i];

                        var symptoms = "<b>Symptoms: </b>";
                        if(item.hasOwnProperty('other_symptoms')){
                            for (var j = 0; j < item.other_symptoms.length; j++) {
                                if (j != 0) {
                                    symptoms += ", "
                                }
                                const ss = item.other_symptoms[j];
                                var found = false;
                                for (var k = 0; k < res.tagged_symptoms.length; k++) {
                                    console.log(ss)
                                    console.log(res.tagged_symptoms[k])
                                    if (res.tagged_symptoms[k] === ss) {
                                        found = true;
                                        break;
                                    }
                                }
                                if (found) {
                                    symptoms += "<span style='background-color: red'>" + ss + "</span>"
                                }
                                else {
                                    symptoms += ss;
                                }
                            }
                        }

                        list_posts += "<div class='card' style='background-color: #888788; color: #E2E2E2;'>";
                        list_posts += "<h3><a style='text-decoration: none; color: white;' href='" + item.url + "' target='_blank'>" + item.title + "</a></h3>";
                        list_posts += "<br/>";
                        list_posts += "<p>" + item.summary.substring(0, 200) + "...</p>";
                        list_posts += "<br/>";
                        list_posts += "<p>" + symptoms + "</p>";
                        list_posts += "</div>";
                        // list_posts += "<ul>";
                        // list_posts += "<li class='title_li'><a href='" + item.url + "' target='_blank'>" + item.title + "</a></li>";
                        // list_posts += "<ul>";
                        // // list_posts += "<li class='description'>" + item.summary.substring(0, 200) + " (<a href = '" + item.url + "' " + "target='_blank'" + "color ='blue'" + " >" + item.url + "</a>) </li>";
                        // list_posts += "<li class='description'>" + item.summary.substring(0, 200) + "...</li>";
                        // list_posts += "<li class = 'description'>" + symptoms + "</li>";
                        // list_posts += "</ul>";
                        // list_posts += "</ul>";
                        // list_posts += "<hr class='hr_line'>"
                    }
                }
            }

            if(res.results.hasOwnProperty('patient_info')) {
                if (res.results.patient_info.length > 0) {
                    var displaysize = 5;
                    if (res.results.patient_info.length < displaysize) {
                        displaysize = res.results.patient_info.length
                    }

                    for (var i = 0; i < displaysize; i++) {
                        var item = res.results.patient_info[i];
                        var symptoms = "<b>Symptoms: </b>";
                        if(item.hasOwnProperty('other_symptoms')){
                            for (var j = 0; j < item.other_symptoms.length; j++) {
                                if (j != 0) {
                                    symptoms += ", "
                                }
                                const ss = item.other_symptoms[j];
                                var found = false;
                                for (var k = 0; k < res.tagged_symptoms.length; k++) {
                                    console.log(ss)
                                    console.log(res.tagged_symptoms[k])
                                    if (res.tagged_symptoms[k] === ss) {
                                        found = true;
                                        break;
                                    }
                                }
                                if (found) {
                                    symptoms += "<span style='background-color: red'>" + ss + "</span>"
                                }
                                else {
                                    symptoms += ss;
                                }
                            }
                        }
                        list_posts += "<div class='card' style='background-color: #888788; color: #E2E2E2;'>";
                        list_posts += "<h3><a style='text-decoration: none; color: white;' href='" + item.url + "' target='_blank'>" + item.title + "</a></h3>";
                        list_posts += "<br/>";
                        list_posts += "<p>" + item.summary.substring(0, 200) + "...</p>";
                        list_posts += "<br/>";
                        list_posts += "<p>" + symptoms + "</p>";
                        list_posts += "</div>";
                        // list_posts += "<ul>";
                        // list_posts += "<li class='title_li'><a href='" + item.url + "' target='_blank'>" + item.title + "</a></li>";
                        // list_posts += "<ul>";
                        // // list_posts += "<li class='description'>" + item.summary.substring(0, 100) + " (<a href = '" + item.url + "' " + "target='_blank'" + "color ='blue'" + " >" + item.url + "</a>) </li>";
                        // list_posts += "<li class='description'>" + item.summary.substring(0, 200) + "...</li>";
                        // list_posts += "<li class = 'description'>" + symptoms + "</li>";
                        // list_posts += "</ul>";
                        // list_posts += "</ul>";
                        // list_posts += "<hr class='hr_line'>"
                    }
                }
            }

            setTimeout(function () {
                $("#forums").append(list_posts);
            });
        }
        else
        if(selectedValue==='Drugs') {
            $('#drugs').empty();

            var drug_list = "";
            if(res.results.length != 0){
                for (var i = 0; i < 5; i++) {
                    var item = res.results[i];

                    drug_list += "<div class='drugContainer'>";
                    drug_list += "<p class=''><a href='" + item.drug_detail_page + "' target='_blank' style='text-decoration: none; color: white'>" + item.drug_name + "</a></p>";
                    //drug_list += "<p>" + item.drug_name + "</p>";
                    drug_list += "<p class=''>" + " (<a href = '" + item.drug_review_page + "' " + "target='_blank' style='text-decoration: none; color: white'"  + " > Check user reviews" + "</a>) </p>";
                    drug_list += "</div>";
                    drug_list += "<br/>"

                    // drug_list += "<ul>";
                    // // drug_list += "<li class='title_li'>" + item.drug_name + "</li>";
                    // drug_list += "<li class='title_li'><a href='" + item.drug_detail_page + "' target='_blank'>" + item.drug_name + "</a></li>";
                    // drug_list += "<ul>";
                    // // drug_list += "<li class='description'>" + " (<a href = '" + item.drug_review_page + "' " + "target='_blank'" + "color ='blue'" + " >" + item.drug_review_page + "</a>) </li>";
                    // drug_list += "<li class='description'>" + " (<a href = '" + item.drug_review_page + "' " + "target='_blank'" + "color ='blue'" + " > Check user reviews" + "</a>) </li>";
                    // drug_list += "</ul>";
                    // drug_list += "</ul>";
                    // drug_list += "<hr class='hr_line'>"
                }
                setTimeout(function () {
                    console.log(drug_list);
                    $("#drugs").append(drug_list);
                });
            }
            else {
                $("#drugs").append("<h4>No Matching Drugs Found.</h4>");
            }
        }
    } else {
        swal("Don't Worry! It doesn't seem like any disease as per the results!");
    }
}

function searchOptionChange() {
    if (selectedValue === 'Diseases') {
        selectedValue = 'Drugs';
        $("#related_symptoms").css('visibility', 'hidden');
        $('.results').css('display', 'none');
        $('.drugResults').css('display', 'block');
        //reset the value to avoid unwanted search
        document.getElementById('search_box').value = '';
        document.getElementById("search_box").placeholder = "Type the disease name here...";
    }
    else {
        selectedValue = 'Diseases';
        $("#related_symptoms").css('visibility', 'visible');
        $('.drugResults').css('display', 'none');
        $('.results').css('display', 'flex');
        //reset the value to avoid unwanted search
        document.getElementById('search_box').value = '';
        document.getElementById("search_box").placeholder = "Type the symptoms here...";
    }
}