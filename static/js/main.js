function TooManyAlert() {
    // Get the modal
    var modal = document.getElementById("tooManyModal");
    // Get the <span> element that closes the modal
    var span = document.querySelector("#tooManyModal .close");

    modal.style.display = "block";

    // When the user clicks on <span> (x), close the modal
    span.onclick = function (event) {
        modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}


function add_to_read_later_list(article, selected_style) {

    console.log("selected style = ", selected_style)

    //"article" contains an object with "id,aid,style" to be sent to the user profile in the backend
    //in addition, it contains the url and the title of the article to be added to the read later dropdown list
    // console.log("article = ", article);

    //split "article" into article's info ("id,aid,style"), article's url url, and article's title
    article_info = article.split("|")[0];
    article_title = article.split("|")[1];

    // getItems read_later_articles, read_later_titles from the local storgae

    if (typeof localStorage.getItem("read_later_articles") !== 'undefined' && localStorage.getItem("read_later_articles") != null
        && typeof localStorage.getItem("read_later_titles") !== 'undefined' && localStorage.getItem("read_later_titles") != null) {

        var read_later_articles = localStorage.getItem("read_later_articles");
        var read_later_titles = localStorage.getItem("read_later_titles");
        var read_later_button_list = localStorage.getItem("read_later_button_list")
    }

    
    //Check if the article was already in the read_later list
    if (!read_later_articles.includes(article_info)) {
        // Check the number of articles currently in the Read Later list
        var currentArticleCount = read_later_articles.split("||").filter(Boolean).length;
        
        //if you are in the article.html, this will return null coz I removed the dropdown menu from the article.html
        var dropdown_readLater = document.querySelector(".dropdown-content");

        //if the reading list is empty and this is the first article to be added, remove the first element from the dropdown "---Empty---""
        if (read_later_titles == '' && dropdown_readLater != null){
            dropdown_readLater.removeChild(dropdown_readLater.firstElementChild);
        }

        //if the article is new to the read_later list, add it to the localStorage
        read_later_articles = read_later_articles + article_info + "||";
        localStorage.setItem("read_later_articles", read_later_articles);


        read_later_titles = read_later_titles + article_title + "||";
        localStorage.setItem("read_later_titles", read_later_titles);

       ////// correct selections are in green and false selections are in red //////
        
        article_info = article_info.replaceAll("\'", "\"")
        console.log(article_info)

        let article_info_obj = JSON.parse(article_info);
        let article_style = article_info_obj.style;

        // var article_style = article_info.match(/'style':'(.*?)'/);
        console.log("article's style = ", article_style)


        if (article_style == selected_style){
            document.getElementById(article).classList.add("selected");
            document.getElementById(article).classList.add("selected_green");
        }
        else{
            document.getElementById(article).classList.add("selected");
            document.getElementById(article).classList.add("selected_red");
        }

        read_later_button_list = read_later_button_list + article + "||"
        localStorage.setItem("read_later_button_list", read_later_button_list)

        if (dropdown_readLater != null) {

            //Now add the article to the dropdown menu (this will be applied in the front page only)
            var a = document.createElement('a');
            var linkText = document.createTextNode(article_title);
            a.appendChild(linkText);
            a.title = article_title;
            // a.href = article_url;
            dropdown_readLater.appendChild(a);

            //increase the counter of read later dropdown title
            let readlater_arr = read_later_titles.split("||");
            let length = readlater_arr.length - 1;
            document.querySelector(".dropbtn").innerHTML = "Selected articles (" + length + ")" + "<i class=\"caret\"></i>";
        }

        //Then send the article's info to the backend(read_later view)
        data = JSON.stringify({
            headline: "read_later_articles",
            article_info: article_info,
            background_image: "Testing",
        })

        //get the url for read_later view "basic_app:read_later"
        var readLaterUrl = document.querySelector("#readLaterURL").getAttribute("data-url");

        let csrftoken = getCookie('csrftoken');
        let response = fetch(readLaterUrl, {
            method: 'POST',
            body: data,
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json',
                'Access-Control-Allow-Headers': '*',
                'Access-Control-Allow-Credentials': true,
                'Access-Control-Allow-Origin': '*',
                "X-CSRFToken": csrftoken
            },
        }).catch((err) => {
            if (typeof err === 'string') err = new Error(err)
            console.error("error=", err)
        })
    }
    else {
        remove_from_read_later(article);
        var articleElement = document.getElementById(article);
        if (articleElement) {
            articleElement.classList.remove("selected");
            articleElement.classList.remove("selected_green");
            articleElement.classList.remove("selected_red");
            
        }
        var read_later_button_list = localStorage.getItem("read_later_button_list") || "";
        read_later_button_list = removeItemFromString(read_later_button_list, article, "||");
        localStorage.setItem("read_later_button_list", read_later_button_list);


    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}


function loadReadLaterList() {
    // Retrieve read later articles from localStorage
    const articles = localStorage.getItem("read_later_button_list");

    if (articles) {
        const articleIds = articles.split("||");
        // Iterate over each article ID
        articleIds.forEach(articleId => {
            // Trim any leading or trailing whitespace from the ID
            articleId = articleId.trim();
            
            // Apply selected class to buttons corresponding to read later articles
            const button = document.getElementById(articleId);
            if (button) {
                button.classList.add("selected");
            }
        });
    }

}

function loadDropdownList() {

    // getItems read_later_articles, read_later_titles from the local storgae

    if (typeof localStorage.getItem("read_later_titles") !== 'undefined' && localStorage.getItem("read_later_titles") != null)
         {
        var read_later_titles = localStorage.getItem("read_later_titles");
    }

    // get the dropdown menu
    var dropdown_readLater = document.querySelector(".dropdown-content");


    //first load: titles_arr = ''
    //after adding some items: titles_arr = title1||title2||title3||''
    titles_arr = read_later_titles.split("||");

    let arr_lenth = 0;

    if (titles_arr.length == 1 && titles_arr[0] == '') {

        //the list is empty
        titles_arr[0] = '--- Empty ---';
        console.log("empty list");

        var a = document.createElement('a');
        var linkText = document.createTextNode('--- Empty ---');
        a.appendChild(linkText);
        a.href = '#';
        a.classList.add("inactiveLink");

        dropdown_readLater.appendChild(a);

    } else {
        //When splitting this string, the last element will be an empty cell in the array, remove it.
        popped = titles_arr.pop();
        arr_lenth = titles_arr.length;
        console.log(" list = ", arr_lenth);
    }

    document.querySelector(".dropbtn").innerHTML = "Selected articles (" + arr_lenth + ")" + "<i class=\"caret\"></i>";

    for (let i = 0; i < arr_lenth; i++) {

        // Create new node for each article and push it to read later dropdown menu
        var a = document.createElement('a');
        var linkText = document.createTextNode(titles_arr[i]);
        a.appendChild(linkText);
        a.title = titles_arr[i];
        dropdown_readLater.appendChild(a);

    }
}

function remove_from_read_later(article) {

    article_info = article.split("|")[0];
    article_title = article.split("|")[1];

    // getItems read_later_articles, read_later_titles from the local storgae

    if (typeof localStorage.getItem("read_later_articles") !== 'undefined' && localStorage.getItem("read_later_articles") != null
        && typeof localStorage.getItem("read_later_titles") !== 'undefined' && localStorage.getItem("read_later_titles") != null)
         {

        var read_later_articles = localStorage.getItem("read_later_articles");
        var read_later_titles = localStorage.getItem("read_later_titles");
    }

    // Remove the article details from the localStorage strings
    read_later_articles = removeItemFromString(read_later_articles, article_info, "||");
    read_later_titles = removeItemFromString(read_later_titles, article_title, "||");

    
    // Update the localStorage with the new strings
    localStorage.setItem("read_later_articles", read_later_articles);
    localStorage.setItem("read_later_titles", read_later_titles);

    //if you are in the article.html, this will return null coz I removed the dropdown menu from the article.html
    var dropdown_read_later_articles = document.querySelector(".dropdown-content");
    var index = findArticleIndexInDropdown(dropdown_read_later_articles, article_title);
    if (index !== -1) {
        removeNthArticle(dropdown_read_later_articles, index);
    }

    updateArticleCountDisplay();


    console.log("back-end");
    //Then send the article's info to the backend(selected view)
    data = JSON.stringify({
        headline: "read_later_articles",
        article_info: article_info,
        background_image: "Testing",
    })

    //get the url for read_later view "basic_app:read_later"
    var removeReadLaterUrl = document.querySelector("#removeReadLaterUrl").getAttribute("data-url");

    let csrftoken = getCookie('csrftoken');
    let response = fetch(removeReadLaterUrl, {
        method: 'POST',
        body: data,
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json',
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Credentials': true,
            'Access-Control-Allow-Origin': '*',
            "X-CSRFToken": csrftoken
        },
    }).catch((err) => {
        if (typeof err === 'string') err = new Error(err)
        console.error("error=", err)
    })

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

}



function removeItemFromString(string, item, separator) {
    var items = string.split(separator);
    var index = items.indexOf(item);
    console.log(items)
    console.log(index)
    if (index !== -1) {
        items.splice(index, 1); // Remove the item
    }
    return items.join(separator); // Recreate the string without the item
}

function findArticleIndexInDropdown(dropdown, article_title) {
    var links = dropdown.getElementsByTagName("a");
    for (var i = 0; i < links.length; i++) {
        if (links[i].textContent === article_title) {
            return i; // Return the index of the article
        }
    }
    return -1; // Article not found
}

function removeNthArticle(dropdown, index) {
    console.log(`Removing article at index: ${index}`);
    if (dropdown && index >= 0 && index < dropdown.children.length) {
        dropdown.removeChild(dropdown.children[index]);
    }
}

function updateArticleCountDisplay() {
    var read_later_titles = localStorage.getItem("read_later_titles") || "";
    var read_later_arr = read_later_titles.split("||").filter(title => title.trim() !== '');
    var length = read_later_arr.length;

    document.querySelector(".dropbtn").innerHTML = "Selected articles (" + length + ")" + "<i class=\"caret\"></i>";

    var dropdown_read_later_articles = document.querySelector(".dropdown-content");
    if (length === 0) {
        dropdown_read_later_articles.innerHTML = '<a href="#" class="inactiveLink">--- Empty ---</a>';
    }
}


function loadCounter() {
    //Set localstorage counter to count down the time spent on every page of the website
    //and end the experiment after an exact number of minutes (set the number of minutes in start_page.html and personal_info.html (else if), also down here in the "ëlse"scope)

    if (typeof localStorage.getItem("min") !== 'undefined' && typeof localStorage.getItem("sec") !== 'undefined' && localStorage.getItem("min") != null && localStorage.getItem("sec") != null) {
        var min = localStorage.getItem("min");
        var sec = localStorage.getItem("sec");
    }
    else {

        //Change the counter end time here

        var min = "0" + 1;
        var sec = "0" + 0;
    }
    var time;

    console.log ("inside loadcounter ")
    console.log ("min = ", min, " sec = ", sec)

    /////////// ----- ----- ///////////
    //this block of code is repeated in setInterval function.
    //but it also exists here to prevent the one sec delay in the first load of the page
    
    localStorage.setItem("min", min);
    localStorage.setItem("sec", sec);
    time = min + " : " + sec;
    document.getElementById("timer").innerHTML = time;
    if (sec == '00') {
        if (min != 0) {
            min--;
            sec = 59;
            if (min < 10) {
                min = "0" + min;
            }
        } else {
            localStorage.setItem("min", 0);
            localStorage.setItem("sec", 0);

            ////////////////////// End the experiment //////////////////////
            var thanksUrl = document.querySelector("#thanksURL").getAttribute("data-url");
            window.location.replace(thanksUrl);
            ////////////////////// End the experiment //////////////////////

        }
    }
    else {
        sec--;
        if (sec < 10) {
            sec = "0" + sec;
        }
    }
    /////////// --------- ///////////

    setInterval(function () {

        //repeat the above code block every second

        localStorage.setItem("min", min);
        localStorage.setItem("sec", sec);
        time = min + " : " + sec;
        document.getElementById("timer").innerHTML = time;
        if (sec == '00') {
            if (min != 0) {
                min--;
                sec = 59;
                if (min < 10) {
                    min = "0" + min;
                }
            } else {
                localStorage.setItem("min", 0);
                localStorage.setItem("sec", 0);

                ////////////////////// End the experiment //////////////////////
                var thanksUrl = document.querySelector("#thanksURL").getAttribute("data-url");
                window.location.replace(thanksUrl);
                ////////////////////// End the experiment //////////////////////

            }
        }
        else {
            sec--;
            if (sec < 10) {
                sec = "0" + sec;
            }
        }
    }, 1000);

}

// // Function to get the selected radio button value from the pre-survey page. used in personal_info.html
// function getSelectedRadioValue() {
//     // Get all radio buttons with the name 'preferred_headline3'
//     const radios = document.querySelectorAll('input[name="preferred_headline3"]');
    
//     let selectedValue;
    
//     // Loop through the radio buttons to find the checked one
//     radios.forEach(radio => {
//         if (radio.checked) {
//             selectedValue = radio.value;  // Get the value of the checked radio button
//         }
//     });

//     // Display or use the selected value
//     console.log("Selected headline:", selectedValue);
//     return selectedValue;
// }

// // Call the function when needed (e.g., when a button is clicked)
// getSelectedRadioValue();




// Function to display the selected radio button value inside the <p> tag
function displaySelectedValue() {
    // Get all the radio buttons with the name 'preferred_headline3'
    const radios = document.querySelectorAll('input[name="preferred_headline3"]');
    console.log ("inside displaySelectedVal");
    console.log (radios);
    
    let selectedValue;
    
    // Loop through the radio buttons to find the checked one
    radios.forEach(radio => {
        print( "for each = ", radio.value )
        if (radio.checked) {
            print ("Checked !!!!!!!!!!!!")
            selectedValue = radio.value;  // Get the value of the checked radio button
            console.log("value = ", value)
        }
    });

    // Display the selected value inside the <p> tag with id "selectedValue"
    document.getElementById('selectedValue').textContent = "Selected headline: " + selectedValue;
}

