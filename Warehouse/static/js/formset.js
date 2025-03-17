document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('add-form').addEventListener('click', function() {
        const formsetContainer = document.getElementById('formset-container');
        const totalForms = document.getElementById('id_form-TOTAL_FORMS');
        const formNum = parseInt(totalForms.value);
        
        // Clone first formset row
        const newRow = formsetContainer.querySelector('.formset-row').cloneNode(true);
        
        // Update all names/ids in the cloned row
        newRow.innerHTML = newRow.innerHTML.replace(/form-(\d+)/g, `form-${formNum}`);
        
        // Clear input values
        newRow.querySelectorAll('input, select').forEach(input => {
            if(input.type !== 'hidden') input.value = '';
            if(input.name) input.name = input.name.replace(/form-(\d+)/, `form-${formNum}`);
            if(input.id) input.id = input.id.replace(/form-(\d+)/, `form-${formNum}`);
        });
        
        formsetContainer.appendChild(newRow);
        totalForms.value = formNum + 1;
    });
});