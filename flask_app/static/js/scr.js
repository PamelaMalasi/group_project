var searchButton = document.getElementById('search-button');
searchButton.addEventListener('click', function () {
  var inputText = document.getElementById('search-input').value.toLowerCase();
  var tableRows = document.getElementsByClassName('table-row-position');

  for (var i = 0; i < tableRows.length; i++) {
    var concernText = tableRows[i].innerText.toLowerCase();

    if (concernText.includes(inputText)) {
      tableRows[i].parentNode.style.display = '';
    } else {
      tableRows[i].parentNode.style.display = 'none';
    }
  }
});
