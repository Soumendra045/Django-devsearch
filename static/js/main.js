  // Get search form and page links
  let searchForm = document.getElementById('searchForm');
  let pageLinks = document.getElementsByClassName('page-link');

  // Ensure search form exists
  if (searchForm) {
    for (let i = 0; i < pageLinks.length; i++) {
      pageLinks[i].addEventListener('click', function (e) {
        e.preventDefault();

        // Get page number from data attribute
        let page = this.dataset.page;

        // Add hidden input to form
        searchForm.innerHTML += `<input type="hidden" value="${page}" name="page" />`;

        // Submit form
        searchForm.submit();
      });
    }
  }
