const imageUpload = document.getElementById('imageUpload');
const uploadSection = document.getElementById('uploadSection');
const actionSection = document.getElementById('actionSection');
const embedBtn = document.getElementById('embedBtn');
const extractBtn = document.getElementById('extractBtn');
const embedForm = document.getElementById('embedForm');
const extractForm = document.getElementById('extractForm');
const resultSection = document.getElementById('resultSection');
const resultText = document.getElementById('resultText');

// Reset to landing page
function resetToMainPage() {
    uploadSection.classList.remove('hidden');
    actionSection.classList.add('hidden');
    resultSection.classList.add('hidden');
    embedForm.classList.add('hidden');
    extractForm.classList.add('hidden');
    imageUpload.value = ''; // Clear file input
}

// When an image is uploaded
imageUpload.addEventListener('change', function() {
    uploadSection.classList.add('hidden');
    actionSection.classList.remove('hidden');
});

// Toggle embed form
embedBtn.addEventListener('click', function() {
    embedForm.classList.remove('hidden');
    extractForm.classList.add('hidden');
});

// Toggle extract form
extractBtn.addEventListener('click', function() {
    extractForm.classList.remove('hidden');
    embedForm.classList.add('hidden');
});

// Embed data function
function embedData() {
    const formData = new FormData();
    formData.append('image', imageUpload.files[0]);
    formData.append('data', document.getElementById('dataToEmbed').value);

    fetch('/embed', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.blob();
        }
        throw new Error('Embedding failed');
    })
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = 'encoded_image.png';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);

        // Add back to main button
        resultSection.innerHTML = `
            <p class="text-lg font-semibold text-gray-800">Data embedded successfully!</p>
            <button 
                onclick="resetToMainPage()"
                class="mt-4 w-full py-3 text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition duration-300"
            >
                Back to Main Page
            </button>
        `;
        actionSection.classList.add('hidden');
        resultSection.classList.remove('hidden');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to embed data');
    });
}

// Extract data function
function extractData() {
    const formData = new FormData();
    formData.append('image', imageUpload.files[0]);

    fetch('/extract', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.text();
        }
        throw new Error('Extraction failed');
    })
    .then(text => {
        const extractedText = text.replace('Hidden Data: ', '');
        resultSection.innerHTML = `
            <p class="text-lg font-semibold text-green-500 font-orbitron"> 
                Your super secret extracted text from the definitely not troll image is <br> 
                <span class="text-green-400">${extractedText}</span>
            </p>
            <button 
                onclick="resetToMainPage()"
                class="mt-4 w-full py-3 text-white bg-cyan-600 rounded-lg hover:bg-cyan-700 transition duration-300 font-orbitron"
            >
                Back to Main Page
            </button>
        `;
        actionSection.classList.add('hidden');
        resultSection.classList.remove('hidden');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to extract data');
    });
}