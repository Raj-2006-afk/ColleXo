/**
 * ColleXo - Form Builder
 * Dynamic form field creation for society recruitment forms
 */

let formFields = [];
let fieldCounter = 0;

// Add new field
function addField(type) {
    const field = {
        id: ++fieldCounter,
        name: `field_${fieldCounter}`,
        type: type,
        label: '',
        placeholder: '',
        required: false,
        options: []
    };
    
    formFields.push(field);
    renderFields();
    
    // Scroll to new field
    setTimeout(() => {
        const newField = document.getElementById(`field_${field.id}`);
        if (newField) {
            newField.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }, 100);
}

// Remove field
function removeField(id) {
    formFields = formFields.filter(f => f.id !== id);
    renderFields();
}

// Update field property
function updateField(id, property, value) {
    const field = formFields.find(f => f.id === id);
    if (field) {
        field[property] = value;
        updateFormSchema();
    }
}

// Add option to select/radio/checkbox
function addOption(id) {
    const field = formFields.find(f => f.id === id);
    if (field) {
        const optionValue = prompt('Enter option value:');
        if (optionValue && optionValue.trim()) {
            field.options.push(optionValue.trim());
            renderFields();
        }
    }
}

// Remove option
function removeOption(fieldId, optionIndex) {
    const field = formFields.find(f => f.id === fieldId);
    if (field) {
        field.options.splice(optionIndex, 1);
        renderFields();
    }
}

// Render all fields
function renderFields() {
    const container = document.getElementById('formFieldsContainer');
    
    if (formFields.length === 0) {
        container.innerHTML = '<p class="text-muted" style="text-align: center; padding: 2rem 0;">No fields added yet. Click buttons above to add fields.</p>';
        updateFormSchema();
        return;
    }
    
    container.innerHTML = formFields.map(field => `
        <div id="field_${field.id}" class="form-field-preview">
            <div style="flex: 1;">
                <div style="display: flex; gap: 1rem; margin-bottom: 0.5rem;">
                    <input type="text" 
                           class="form-control" 
                           placeholder="Field Label *" 
                           value="${field.label}"
                           onchange="updateField(${field.id}, 'label', this.value)"
                           style="flex: 2;">
                    
                    <input type="text" 
                           class="form-control" 
                           placeholder="Field Name (internal)" 
                           value="${field.name}"
                           onchange="updateField(${field.id}, 'name', this.value)"
                           style="flex: 1;">
                    
                    <select class="form-control" 
                            onchange="updateField(${field.id}, 'type', this.value)"
                            style="flex: 1;">
                        <option value="text" ${field.type === 'text' ? 'selected' : ''}>Text</option>
                        <option value="email" ${field.type === 'email' ? 'selected' : ''}>Email</option>
                        <option value="phone" ${field.type === 'phone' ? 'selected' : ''}>Phone</option>
                        <option value="textarea" ${field.type === 'textarea' ? 'selected' : ''}>Textarea</option>
                        <option value="select" ${field.type === 'select' ? 'selected' : ''}>Dropdown</option>
                        <option value="radio" ${field.type === 'radio' ? 'selected' : ''}>Radio</option>
                        <option value="checkbox" ${field.type === 'checkbox' ? 'selected' : ''}>Checkbox</option>
                        <option value="file" ${field.type === 'file' ? 'selected' : ''}>File</option>
                    </select>
                </div>
                
                ${['text', 'email', 'phone', 'textarea'].includes(field.type) ? `
                    <input type="text" 
                           class="form-control" 
                           placeholder="Placeholder text (optional)" 
                           value="${field.placeholder}"
                           onchange="updateField(${field.id}, 'placeholder', this.value)"
                           style="font-size: 0.875rem; margin-top: 0.5rem;">
                ` : ''}
                
                ${['select', 'radio', 'checkbox'].includes(field.type) ? `
                    <div style="margin-top: 0.5rem;">
                        <strong style="font-size: 0.875rem;">Options:</strong>
                        <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.25rem;">
                            ${field.options.map((opt, idx) => `
                                <span class="badge badge-secondary" style="display: flex; align-items: center; gap: 0.25rem;">
                                    ${opt}
                                    <button type="button" 
                                            onclick="removeOption(${field.id}, ${idx})"
                                            style="background: none; border: none; color: white; cursor: pointer; padding: 0;">&times;</button>
                                </span>
                            `).join('')}
                            <button type="button" 
                                    class="btn btn-sm btn-outline-primary" 
                                    onclick="addOption(${field.id})"
                                    style="padding: 0.125rem 0.5rem;">+ Add Option</button>
                        </div>
                    </div>
                ` : ''}
                
                <label style="margin-top: 0.5rem; font-size: 0.875rem; display: flex; align-items: center; gap: 0.5rem;">
                    <input type="checkbox" 
                           ${field.required ? 'checked' : ''}
                           onchange="updateField(${field.id}, 'required', this.checked)">
                    Required field
                </label>
            </div>
            
            <div class="field-controls">
                <button type="button" 
                        class="btn btn-sm btn-danger" 
                        onclick="removeField(${field.id})">
                    Delete
                </button>
            </div>
        </div>
    `).join('');
    
    updateFormSchema();
}

// Update hidden form schema input
function updateFormSchema() {
    const schema = formFields.map(field => ({
        name: field.name,
        type: field.type,
        label: field.label,
        placeholder: field.placeholder,
        required: field.required,
        options: field.options
    }));
    
    document.getElementById('form_schema').value = JSON.stringify(schema);
}

// Form submission validation
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('formBuilderForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            if (formFields.length === 0) {
                e.preventDefault();
                alert('Please add at least one form field before creating the form.');
                return false;
            }
            
            // Validate all fields have labels
            for (const field of formFields) {
                if (!field.label.trim()) {
                    e.preventDefault();
                    alert('All fields must have a label. Please check your fields.');
                    return false;
                }
                
                // Validate options for select/radio/checkbox
                if (['select', 'radio', 'checkbox'].includes(field.type) && field.options.length === 0) {
                    e.preventDefault();
                    alert(`Field "${field.label}" needs at least one option.`);
                    return false;
                }
            }
        });
    }
});
