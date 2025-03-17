document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.getElementById('add-form');
    const formsetContainer = document.getElementById('formset-container');
    const totalForms = document.getElementById('id_line_items-TOTAL_FORMS');
    const formRegex = /line_items-(\d+)-/g; // Match line_items-0-, line_items-1-, etc.

    addButton.addEventListener('click', function() {
        const formNum = parseInt(totalForms.value);
        const newRow = formsetContainer.querySelector('.formset-row').cloneNode(true);

        // Update IDs and names
        newRow.innerHTML = newRow.innerHTML.replace(
            formRegex,
            `line_items-${formNum}-`
        );

        // Clear input values
        newRow.querySelectorAll('input, select').forEach(input => {
            input.value = '';
            if (input.type === 'checkbox') input.checked = false;
        });

        formsetContainer.appendChild(newRow);
        totalForms.value = formNum + 1; // Increment form count
    });
});