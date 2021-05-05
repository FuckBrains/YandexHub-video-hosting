async function search() {
    var input = document.getElementById("search-input");
    var button = document.getElementById("search-button");
    if (String(input.value).length != 0) {
        //window.location = `${location.protocol}//${location.hostname + (location.port ? ':' + location.port : '')}/results/search_query=${input.value}`;
        transition_link(`${location.protocol}//${location.hostname + (location.port ? ':' + location.port : '')}/results/search_query=${input.value}`);
        
    }
}