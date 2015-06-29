function change_page(direction) {
    var item = document.getElementById('pagenr').innerHTML;
    var pagenumber = parseInt(item);
    var currentURL = window.location.href;

    if (direction === 'next') {
        pagenumber++;
    } else if (direction === 'prev') {
        pagenumber--;
    }

    var idx = currentURL.indexOf("page/");
    var url = currentURL.substring(0, idx) + "page/" + pagenumber;
    window.location.href = url;
}
