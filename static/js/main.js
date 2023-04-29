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
