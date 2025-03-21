document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.getElementById('add-form');
    const formsetContainer = document.getElementById('formset-container');
    const totalForms = document.getElementById('id_line_items-TOTAL_FORMS');
    const emptyForm = document.getElementById('empty-form');

    addButton.addEventListener('click', function() {
        const formNum = parseInt(totalForms.value);
        const newRow = emptyForm.cloneNode(true);
        
        // Make the new row visible and remove its id to avoid duplicates
        newRow.style.display = '';
        newRow.id = '';
        
        // Replace __prefix__ with the new form number in field names/IDs
        newRow.innerHTML = newRow.innerHTML.replace(
            /__prefix__/g,
            formNum
        );
        
        // Append the new row to the container
        formsetContainer.appendChild(newRow);
        
        // Increment the total forms count
        totalForms.value = formNum + 1;
    });
});