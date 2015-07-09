function change_page(direction) {
    var item = document.getElementById('pager').innerHTML;
    var page_number = parseInt(item);
    var currentURL = window.location.href;

    if (direction === 'next') {
        page_number++;
    } else if (direction === 'prev') {
        page_number--;
    }

    var idx = currentURL.indexOf("page/");
    window.location.href = currentURL.substring(0, idx) + "page/" + page_number;
}
