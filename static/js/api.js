const loadChildActivity = (pk) => {
    // API for child activities history
    let url = `/api/childactivity/${pk}`;
    fetch(url)
        .then(response => {

            return response.json();
        })
        .then(res => {
            $('#right-panel-data').empty();
            $.each(res, function (index, value) {
                $('#right-panel-data').append(`<h3>History Child Activities</h3><br><div><h5>${index + 1}) Title - ${value.Title}, Status -${value.status}</h5></div>`);
            });

        });


}


const addTask = (pk, csrf_token) => {
    // API for child activities history
    let url = `/api/project-task/?id=${pk}`;
   

    fetch(url,
        {
            headers: {
                'Content-Type':  "application/json",
                "X-CSRFToken": csrf_token
            },
            method: "GET",
           
        })
        .then(response => {
           console.log(response.json());
            return response.json();
          
        })
        .then(res => {
           

        });


}


const addFav = (pk, type, csrf_token) => {
    // API for child activities history
    let url = `/api/fav-items/`;
    var payload = { item_id: pk, type: type };
    

    fetch(url,
        {
            headers: {
                'Content-Type':  "application/json",
                "X-CSRFToken": csrf_token
            },
            method: "POST",
            body: JSON.stringify( payload )
        })
        .then(response => {
           
            return response.json();
          
        })
        .then(res => {
           

        });


}

const loadRevisionItem = () => {
    let url = '/api/revision/';
    fetch(url)
        .then(response => {

            return response.json();
        })
        .then(res => {
            $('#tags').empty();
            let tags = res['tags'];
            if (tags.length) {
                $('#tags').empty();
                $.each(tags, function (index, value) {
                    $('#tags').append(`<div><h5><span class="badge badge-info mr-2" >${value}</span><h5></div>`);
                });
            }
            $(".modal-body-revision").html(res["content"]);
            $("#model_id").html(res["pk"]);
            upd = res["updated"]
            $("#last_upd").html(upd.split("T")[0]);

        });


}
const NextRevisionItem = () => {
    let id = $("#model_id").html();
    let url = `/api/revision/${id}/`;

    fetch(url)
        .then(response => {
            return response.json();
        })
        .then(res => {

        });
    loadRevisionItem(); // load new questions
}

const EditRevisionItem = () => {
    let id = $("#model_id").html();
    let url = `/comments/update/${id}/`;
    window.open(url, "_blank");
}

const updateActivityStatu = (pk) => {
    fetch(`/api/activities/done/${pk}/`)
        .then(response => {
            return response.json();
        })
        .then(res => {
            if (res == 'Done') {
                /** redirect to Activity list */
                window.location = "/activity/";
            }
            else {
                console.log(res);
            }

        });
}