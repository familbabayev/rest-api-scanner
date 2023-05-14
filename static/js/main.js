document.addEventListener('DOMContentLoaded', () => {
  const deleteLinks = document.querySelectorAll('.delete-link');
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  deleteLinks.forEach((link) => {
    link.addEventListener('click', async (e) => {
      e.preventDefault();
      const collectionId = e.target.dataset.id;
      const url = `/collections/${collectionId}/delete`;

      try {
        const response = await fetch(url, {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({ id: collectionId }),
        });

        if (response.ok) {
          // Optionally, remove the row from the table or refresh the page
          e.target.closest('tr').remove();
        } else {
          console.error('Error deleting collection:', response.statusText);
        }
      } catch (error) {
        console.error('Error:', error);
      }
    });
  });
});

document.addEventListener('DOMContentLoaded', function () {
  const sidebar = document.getElementById('sidenav-collapse-main');
  const links = sidebar.querySelectorAll('.nav-link');

  const breadcrumb = document.querySelector(
    '.breadcrumb-item.text-sm.text-dark.active'
  );
  const breadcrumbHeading = document.querySelector(
    'h6.font-weight-bolder.mb-0'
  );

  // Check local storage for the previously active link
  const activeLinkHref = localStorage.getItem('activeLinkHref');
  const activeLinkText = localStorage.getItem('activeLinkText');

  if (breadcrumb && breadcrumbHeading && activeLinkText) {
    breadcrumb.textContent = activeLinkText;
    breadcrumbHeading.textContent = activeLinkText;
  }

  links.forEach((link) => {
    // If this link was the previously active one, add the active classes
    if (link.href === activeLinkHref) {
      link.classList.add('active');
      link.classList.add('bg-gradient-primary');
    }

    link.addEventListener('click', (event) => {
      // Remove active classes from all links
      links.forEach((l) => {
        l.classList.remove('active');
        l.classList.remove('bg-gradient-primary');
      });

      // Add active classes to clicked link
      event.currentTarget.classList.add('active');
      event.currentTarget.classList.add('bg-gradient-primary');

      // Extract the text from the nav-link-text span
      const linkText = event.currentTarget.querySelector(
        '.nav-link-text.ms-1'
      ).textContent;

      // Store the href and text of the clicked link in local storage
      localStorage.setItem('activeLinkHref', event.currentTarget.href);
      localStorage.setItem('activeLinkText', linkText);

      if (breadcrumb && breadcrumbHeading) {
        breadcrumb.textContent = linkText;
        breadcrumbHeading.textContent = linkText;
      }
    });
  });
});

var pieData = {
  labels: ['Label 1', 'Label 2', 'Label 3'],
  datasets: [
    {
      data: [30, 40, 30],
      backgroundColor: ['#ff6384', '#36a2eb', '#ffce56'],
    },
  ],
};

// Get the canvas element
var ctx = document.getElementById('myChart').getContext('2d');

// Create the pie chart
var myChart = new Chart(ctx, {
  type: 'pie',
  data: pieData,
});
